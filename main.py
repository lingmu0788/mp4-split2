#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MP4 Split Application - シンプル版
講義動画から無音部分を検出して自動分割するアプリケーション
（ダイアログなし、コマンドライン版）
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv
import librosa
import numpy as np
from datetime import datetime

# Load environment variables
load_dotenv()

class VideoSplitter:
    """動画分割クラス"""
    
    def __init__(self, input_file, output_dir, silence_threshold=0.01, min_silence_duration=15):
        """
        初期化
        
        Args:
            input_file: 入力動画ファイルパス
            output_dir: 出力ディレクトリ
            silence_threshold: 無音判定の閾値（0-1）
            min_silence_duration: 無音と判定する最小秒数
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.silence_threshold = silence_threshold
        self.min_silence_duration = min_silence_duration
        self.log_file = None
        
    def setup_logging(self):
        """ログファイルのセットアップ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # ログをプロジェクトディレクトリに出力
        log_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(log_dir, f"split_{timestamp}.log")
        
    def log(self, message):
        """ログメッセージを出力してログファイルに記録"""
        print(message)
        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
    
    def get_video_info(self):
        """動画の情報を取得"""
        try:
            # 方法 1: ffprobe で duration を取得（新しいバージョン）
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                self.input_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                import json
                try:
                    data = json.loads(result.stdout)
                    if "format" in data and "duration" in data["format"]:
                        duration = float(data["format"]["duration"])
                        return duration
                except:
                    pass
            
            # 方法 2: ffmpeg で情報を取得（フォールバック）
            cmd = ["ffmpeg", "-i", self.input_file]
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
            output = result.stdout + result.stderr
            
            # "Duration: HH:MM:SS.ms" から時間を抽出
            import re
            match = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", output)
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                seconds = float(match.group(3))
                duration = hours * 3600 + minutes * 60 + seconds
                return duration
            
            self.log("Warning: 動画の時間情報が取得できませんでした")
            return None
            
        except Exception as e:
            self.log(f"Error: 動画情報取得エラー: {e}")
            return None
    
    def extract_audio(self, temp_audio_path):
        """動画から音声を抽出"""
        self.log("音声を抽出中...")
        try:
            cmd = [
                "ffmpeg", "-i", self.input_file,
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",  # 既存ファイルを上書き
                temp_audio_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                self.log(f"Error: 音声抽出エラー")
                self.log(f"詳細: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"Error: 音声抽出エラー: {e}")
            return False
    
    def detect_silence_points(self, audio_path):
        """無音部分を検出してカット点を取得"""
        self.log("無音部分を検出中...")
        try:
            # 音声をロード（16kHz にリサンプリング）
            y, sr = librosa.load(audio_path, sr=16000)
            self.log(f"  サンプルレート: {sr} Hz")
            self.log(f"  音声長: {len(y) / sr:.2f} 秒")
            
            # RMS エネルギーを計算
            frame_length = 2048
            hop_length = 512
            
            # STFT で周波数領域に変換してから RMS を計算
            S = librosa.stft(y, n_fft=frame_length, hop_length=hop_length)
            rms = np.sqrt(np.mean(np.abs(S) ** 2, axis=0))
            
            # フレムの時間長（秒）
            times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
            frame_time = times[1] - times[0] if len(times) > 1 else 1.0 / sr * hop_length
            
            # 無音フレームを検出
            is_silent = rms < self.silence_threshold
            
            # 無音がmin_silence_duration秒以上続く部分を検出
            silence_duration = 0
            silence_start_idx = 0
            candidate_points = []
            
            for i, silent in enumerate(is_silent):
                if silent:
                    if silence_duration == 0:
                        silence_start_idx = i
                    silence_duration += frame_time
                    
                    # 無音がmin_silence_duration秒以上続いた
                    if silence_duration >= self.min_silence_duration:
                        # 無音区間の開始地点をカット点として記録
                        cut_time = times[silence_start_idx]
                        
                        # 同じ無音区間内の重複を避ける
                        if cut_time > 0 and (not candidate_points or candidate_points[-1][0] < cut_time - 5):
                            candidate_points.append((cut_time, silence_duration))
                            silence_duration = 0  # 次の無音区間のため初期化
                else:
                    silence_duration = 0
            
            # 近すぎるカット点を統合（10秒以内なら1つに統合）
            split_points = []
            for cut_time, duration in candidate_points:
                if not split_points or (cut_time - split_points[-1]) > 10:
                    split_points.append(cut_time)
            
            self.log(f"  検出された無音区間: {len(split_points)} 個")
            for i, point in enumerate(split_points):
                self.log(f"    カット点 {i+1}: {self._format_time(point)}")
            
            return split_points
        except Exception as e:
            self.log(f"Error: 無音検出エラー: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _format_time(self, seconds):
        """秒を HH:MM:SS 形式に変換"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def split_video(self, split_points):
        """カット点に基づいて動画を分割"""
        if not split_points:
            self.log("Warning: カット点が検出されませんでした。元のファイルをコピーします。")
            input_name = Path(self.input_file).stem
            input_ext = Path(self.input_file).suffix
            output_file = os.path.join(self.output_dir, f"{input_name}_001{input_ext}")
            
            cmd = ["cp", self.input_file, output_file]
            subprocess.run(cmd, check=True)
            self.log(f"✓ 出力: {output_file}")
            return [output_file]
        
        # ビデオの総時間を取得
        duration = self.get_video_info()
        if not duration:
            return []
        
        # カット点を含めて開始と終了を追加
        timestamps = [0] + split_points + [duration]
        
        output_files = []
        input_name = Path(self.input_file).stem
        input_ext = Path(self.input_file).suffix
        
        self.log(f"\n動画を分割中... ({len(timestamps)-1} 個のセグメント)")
        
        for i in range(len(timestamps) - 1):
            start_time = timestamps[i]
            end_time = timestamps[i + 1]
            duration_seg = end_time - start_time
            
            output_file = os.path.join(
                self.output_dir,
                f"{input_name}_{i+1:03d}{input_ext}"
            )
            
            self.log(f"\n[{i+1}/{len(timestamps)-1}] セグメント分割中...")
            self.log(f"  入力: {self._format_time(start_time)} → {self._format_time(end_time)}")
            self.log(f"  長さ: {self._format_time(duration_seg)}")
            self.log(f"  出力: {output_file}")
            
            try:
                cmd = [
                    "ffmpeg", "-i", self.input_file,
                    "-ss", str(start_time),
                    "-t", str(duration_seg),
                    "-c", "copy",
                    "-y",
                    output_file
                ]
                subprocess.run(cmd, capture_output=True, check=True)
                output_files.append(output_file)
                self.log(f"  ✓ 完了")
            except subprocess.CalledProcessError as e:
                self.log(f"  Error: {e}")
        
        return output_files
    
    def run(self):
        """メイン処理を実行"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
        self.log("=" * 60)
        self.log("MP4 Split Application - 無音検出動画分割")
        self.log("=" * 60)
        self.log(f"入力ファイル: {self.input_file}")
        self.log(f"出力ディレクトリ: {self.output_dir}")
        self.log(f"無音判定閾値: {self.silence_threshold}")
        self.log(f"最小無音時間: {self.min_silence_duration} 秒")
        self.log("=" * 60)
        
        # 入力ファイル検証
        if not os.path.exists(self.input_file):
            self.log(f"Error: 入力ファイルが見つかりません: {self.input_file}")
            return False
        
        # 動画情報を取得
        duration = self.get_video_info()
        if not duration:
            return False
        
        self.log(f"動画時間: {self._format_time(duration)}")
        
        # 一時的な音声ファイル（/tmp に出力して権限問題を回避）
        import tempfile
        temp_audio = os.path.join(tempfile.gettempdir(), "temp_audio.wav")
        
        try:
            # 音声を抽出
            if not self.extract_audio(temp_audio):
                return False
            
            # 無音部分を検出
            split_points = self.detect_silence_points(temp_audio)
            
            # 動画を分割
            output_files = self.split_video(split_points)
            
            # 結果をログに記録
            self.log("\n" + "=" * 60)
            self.log(f"処理完了: {len(output_files)} 個のファイルを生成しました")
            self.log("=" * 60)
            
            # ファイル一覧をコンパクト表示
            self.log("\n【生成ファイル一覧】")
            self.log(f"{'ファイル名':<40} {'サイズ':>10}")
            self.log("-" * 52)
            
            total_size = 0
            for output_file in output_files:
                if os.path.exists(output_file):
                    size_mb = os.path.getsize(output_file) / (1024 * 1024)
                    total_size += size_mb
                    filename = os.path.basename(output_file)
                    self.log(f"{filename:<40} {size_mb:>9.1f}M")
            
            self.log("-" * 52)
            self.log(f"{'合計':<40} {total_size:>9.1f}M")
            self.log("=" * 60)
            
            return True
        
        finally:
            # 一時ファイルをクリーンアップ
            if os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except Exception as e:
                    self.log(f"一時ファイルの削除に失敗: {e}")


def main():
    """Main function"""
    
    # Get environment variables
    input_file = os.getenv("INPUT_FILE")
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    silence_threshold = float(os.getenv("SILENCE_THRESHOLD", "0.01"))
    min_silence_duration = float(os.getenv("MIN_SILENCE_DURATION", "15"))
    
    # Validate inputs
    if not input_file:
        print("Error: INPUT_FILE が .env に設定されていません")
        sys.exit(1)
    
    # Splitter を実行
    splitter = VideoSplitter(
        input_file=input_file,
        output_dir=output_dir,
        silence_threshold=silence_threshold,
        min_silence_duration=min_silence_duration
    )
    
    success = splitter.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




