# 📘 MP4 Split 2 - 操作手順ガイド

**作成日**: 2025-12-27  
**バージョン**: 1.0  
**環境**: macOS

---

## 🎯 目次

1. [セットアップ](#-セットアップ)
2. [操作手順](#-操作手順)
3. [保存ファイルの場所](#-保存ファイルの場所)
4. [設定パラメータ](#-設定パラメータ)
5. [実行例](#-実行例)
6. [トラブルシューティング](#-トラブルシューティング)

---

## ✅ セットアップ

### **1️⃣ プロジェクトディレクトリに移動**

```bash
cd /Users/suzukishinji/projects/mp4-split2
```

### **2️⃣ 仮想環境を確認**

```bash
ls -la venv/
```

すでに `venv/` フォルダが存在します。

### **3️⃣ 依存パッケージをインストール（初回のみ）**

```bash
source venv/bin/activate
pip install -r requirements.txt
brew install ffmpeg  # macOS の場合
```

---

## 🚀 操作手順

### **ステップ 1️⃣: .env ファイルを編集**

```bash
cat > /Users/suzukishinji/projects/mp4-split2/.env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data
SILENCE_THRESHOLD=0.01
MIN_SILENCE_DURATION=30
EOF
```

**各パラメータの説明:**

| パラメータ | 値 | 説明 |
|-----------|-----|------|
| `INPUT_FILE` | `/Users/suzukishinji/Downloads/data/lecture.mp4` | 分割する動画ファイルのパス |
| `OUTPUT_DIR` | `/Users/suzukishinji/Downloads/data` | 分割ファイルの出力先 |
| `SILENCE_THRESHOLD` | 0.01 | 無音判定の感度（低いほど敏感） |
| `MIN_SILENCE_DURATION` | 30 | 最小無音時間（秒）：30秒以上の無音で分割 |

---

### **ステップ 2️⃣: スクリプトを実行**

```bash
# 仮想環境を有効化
source venv/bin/activate

# main.py を実行
python main.py
```

または、`run.sh` スクリプトで一括実行：

```bash
./run.sh
```

---

### **ステップ 3️⃣: 処理完了を確認**

出力例：

```
============================================================
MP4 Split Application - 無音検出動画分割
============================================================
入力ファイル: /Users/suzukishinji/Downloads/data/lecture.mp4
出力ディレクトリ: /Users/suzukishinji/Downloads/data
無音判定閾値: 0.01
最小無音時間: 30.0 秒
============================================================
動画時間: 02:18:37
...
処理完了: 7 個のファイルを生成しました
============================================================
```

---

### **ステップ 4️⃣: 出力ファイルを確認**

```bash
ls -lh /Users/suzukishinji/Downloads/data/
```

出力例：

```
lecture.mp4                   1.2G
lecture_001.mp4              39.9M
lecture_002.mp4             110.1M
lecture_003.mp4             249.3M
lecture_004.mp4              97.4M
lecture_005.mp4             207.1M
lecture_006.mp4             111.8M
lecture_007.mp4             398.2M
```

---

## 📁 保存ファイルの場所

### **入力ファイル**

```
/Users/suzukishinji/Downloads/data/lecture.mp4
```

### **出力ファイル（分割されたビデオ）**

```
/Users/suzukishinji/Downloads/data/
├── lecture_001.mp4   ← 分割ファイル #1
├── lecture_002.mp4   ← 分割ファイル #2
├── lecture_003.mp4   ← 分割ファイル #3
├── lecture_004.mp4   ← 分割ファイル #4
├── lecture_005.mp4   ← 分割ファイル #5
├── lecture_006.mp4   ← 分割ファイル #6
└── lecture_007.mp4   ← 分割ファイル #7
```

### **ログファイル**

```
/Users/suzukishinji/projects/mp4-split2/split_YYYYMMDD_HHMMSS.log

例: split_20251227_175300.log
```

ログファイルの場所：

```bash
ls -lh /Users/suzukishinji/projects/mp4-split2/split_*.log
```

### **一時ファイル**

```
/tmp/temp_audio.wav
```

> **注**: 一時ファイルは処理完了後に自動削除されます。

---

## ⚙️ 設定パラメータ

### **SILENCE_THRESHOLD（無音判定の感度）**

| 値 | 説明 | 推奨用途 |
|-----|------|---------|
| 0.005 | 非常に敏感 | ノイズが少ない環境 |
| 0.01 | **推奨** | 標準的な講義動画 |
| 0.02 | 鈍感 | ノイズが多い環境 |

### **MIN_SILENCE_DURATION（最小無音時間）**

| 値（秒） | 説明 | 推奨用途 |
|---------|------|---------|
| 10 | 短い | 話が頻繁に止まる場合 |
| 15 | 標準 | 通常の講義 |
| 20-30 | 長い | ゆっくりした講義 |
| 30 | **推奨** | 長めの無音部分で分割 |

---

## 📝 実行例

### **例 1: 基本的な分割（デフォルト）**

```bash
# .env を設定
cat > .env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data
SILENCE_THRESHOLD=0.01
MIN_SILENCE_DURATION=30
EOF

# 実行
source venv/bin/activate
python main.py

# 結果確認
ls -lh /Users/suzukishinji/Downloads/data/lecture_*.mp4
```

### **例 2: 敏感な設定（短い無音も検出）**

```bash
cat > .env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data
SILENCE_THRESHOLD=0.005
MIN_SILENCE_DURATION=10
EOF

source venv/bin/activate
python main.py
```

> **結果**: より多くのファイルに分割されます（例: 10～15ファイル）

### **例 3: 鈍感な設定（明確な無音のみ）**

```bash
cat > .env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data
SILENCE_THRESHOLD=0.02
MIN_SILENCE_DURATION=60
EOF

source venv/bin/activate
python main.py
```

> **結果**: より少ないファイルに分割されます（例: 3～5ファイル）

---

## 🔍 ファイル上書き動作

**新しい分割を実行すると、既存のファイルが上書きされます**

```bash
# 1回目実行
python main.py
# → lecture_001.mp4, lecture_002.mp4, ... が生成される

# 2回目実行
python main.py
# → 既存ファイルが上書きされる ⚠️
```

前の結果を保存したい場合は、出力ディレクトリを変更してください：

```bash
# 日付別に出力
cat > .env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data/2025_12_27
SILENCE_THRESHOLD=0.01
MIN_SILENCE_DURATION=30
EOF

python main.py
```

---

## 🐛 トラブルシューティング

### **Q: ffmpeg が見つからない**

**エラー:**
```
Error: ffmpeg command not found
```

**解決:**
```bash
brew install ffmpeg
```

### **Q: INPUT_FILE が見つからない**

**エラー:**
```
Error: 入力ファイルが見つかりません
```

**解決:**
```bash
# ファイルが存在するか確認
ls -l /Users/suzukishinji/Downloads/data/lecture.mp4

# .env を確認
cat .env
```

### **Q: 無音部分が検出されない**

**原因**: SILENCE_THRESHOLD が高すぎる可能性

**解決:**
```bash
cat > .env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data
SILENCE_THRESHOLD=0.005    # ← 低くする
MIN_SILENCE_DURATION=10    # ← 短くする
EOF

python main.py
```

### **Q: 処理が非常に遅い**

**確認項目:**
```bash
# ディスク容量
df -h

# CPU使用率
top

# ファイルサイズ
ls -lh /Users/suzukishinji/Downloads/data/lecture.mp4
```

### **Q: 出力ファイルが生成されない**

**確認:**
```bash
# ログを確認
tail -50 /Users/suzukishinji/projects/mp4-split2/split_*.log

# 出力ディレクトリを確認
ls -la /Users/suzukishinji/Downloads/data/
```

---

## 📊 処理時間の目安

| 動画長 | 無音部分数 | 処理時間 |
|--------|-----------|---------|
| 02:18:37 | 6個 | 約3～5分 |
| 01:00:00 | 5個 | 約2～3分 |
| 30:00 | 3個 | 約1～2分 |

---

## 🎯 推奨設定

**ほとんどの講義動画に最適：**

```bash
cat > .env << 'EOF'
INPUT_FILE=/Users/suzukishinji/Downloads/data/lecture.mp4
OUTPUT_DIR=/Users/suzukishinji/Downloads/data
SILENCE_THRESHOLD=0.01
MIN_SILENCE_DURATION=30
EOF
```

この設定で：
- ✅ 自然な無音部分で分割
- ✅ 誤検出が少ない
- ✅ 処理が高速

---

## 📞 サポート

### **スクリプトの場所**

```
/Users/suzukishinji/projects/mp4-split2/
├── main.py           # メインプログラム
├── run.sh            # 実行スクリプト
├── .env              # 設定ファイル
└── README.md         # 技術仕様書
```

### **よくある疑問**

**Q: 複数の動画を一度に処理したい**

A: ループを追加するか、複数回実行してください。

**Q: 他の形式（MOV, AVI など）に対応している？**

A: ffmpeg がサポートしている形式なら対応可能です。

**Q: 出力形式を変更したい**

A: `main.py` の `split_video()` メソッドを修正してください。

---

## ✨ 最終確認チェックリスト

実行前に以下を確認してください：

- [ ] `/Users/suzukishinji/Downloads/data/lecture.mp4` が存在する
- [ ] `.env` ファイルが正しく編集されている
- [ ] 仮想環境が有効化されている: `source venv/bin/activate`
- [ ] `ffmpeg` がインストールされている: `which ffmpeg`
- [ ] `/Users/suzukishinji/Downloads/data/` に書き込み権限がある

---

**作成日**: 2025-12-27  
**最終更新**: 2025-12-27  
**ステータス**: ✅ 本番運用可能  

🎉 MP4 Split 2 を使用してくださり、ありがとうございます！

