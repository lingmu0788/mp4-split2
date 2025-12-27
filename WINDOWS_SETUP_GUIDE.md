# 🪟 Windows 11 セットアップガイド

**MP4 Split 2** を Windows 11 で使用するための完全セットアップ手順

**作成日**: 2025-12-27  
**対応OS**: Windows 11  
**Python**: 3.7 以上

---

## 📋 目次

1. [必要な環境](#-必要な環境)
2. [セットアップ手順](#-セットアップ手順)
3. [実行方法](#-実行方法)
4. [ファイル構成](#-windows-でのファイル構成)
5. [トラブルシューティング](#-トラブルシューティング)
6. [実行スクリプト（オプション）](#-実行スクリプト作成オプション)

---

## ✅ 必要な環境

Windows 11 でセットアップする前に、以下をインストールしてください：

- ✅ **Git** (バージョン管理)
- ✅ **Python 3.7 以上** (プログラム実行)
- ✅ **ffmpeg** (動画処理)

---

## 🚀 セットアップ手順

### **ステップ 1️⃣: Git をインストール**

1. [https://git-scm.com/download/win](https://git-scm.com/download/win) にアクセス
2. 自動的にダウンロードが始まります
3. ダウンロード完了後、インストーラを実行
4. インストーラウィザード：
   - 「Next」をクリック（デフォルト設定でOK）
   - 最後に「Finish」をクリック

**確認:**

PowerShell または Command Prompt で：

```powershell
git --version
```

出力例：
```
git version 2.43.0.windows.1
```

---

### **ステップ 2️⃣: Python をインストール**

1. [https://www.python.org/downloads/](https://www.python.org/downloads/) にアクセス
2. 「Download Python 3.13」（最新版）をクリック
3. インストーラを実行
4. **⚠️ 重要: 「Add Python to PATH」に ✅ チェック**
5. 「Install Now」をクリック
6. インストール完了

**確認:**

PowerShell で：

```powershell
python --version
```

出力例：
```
Python 3.13.0
```

> PATH に追加されないと後で問題が発生します！

---

### **ステップ 3️⃣: ffmpeg をインストール**

#### **方法 A: Chocolatey を使用（推奨・簡単）**

**1. PowerShell を管理者として実行**

- スタートメニューで「PowerShell」と検索
- 「Windows PowerShell」を**右クリック** → 「管理者として実行」

**2. Chocolatey をインストール（初回のみ）**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

「Y」を選択してEnter

次に：

```powershell
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

コピー・ペースト・Enter

**3. ffmpeg をインストール**

```powershell
choco install ffmpeg -y
```

**確認:**

```powershell
ffmpeg -version
```

出力例：
```
ffmpeg version ... Copyright (c) 2000-2024
```

---

#### **方法 B: 手動インストール（Chocolatey なし）**

1. [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) にアクセス
2. Windows セクションで **「Windows builds from gyan.dev」** をクリック
3. **full build** をダウンロード
4. ダウンロード後、ZIP を解凍
5. `ffmpeg-xxxxx-full_build` フォルダを `C:\ffmpeg\` に移動

**システム環境変数に追加:**

1. Windows キー + X → 「システム」を選択
2. 「システムの詳細設定」をクリック
3. 「環境変数」ボタン
4. **システム環境変数**で「Path」を選択 → 「編集」
5. 「新規」をクリック
6. `C:\ffmpeg\bin` を入力
7. 「OK」を3回クリック

**PowerShell を再起動して確認:**

```powershell
ffmpeg -version
```

---

### **ステップ 4️⃣: mp4-split2 をクローン**

任意のフォルダで PowerShell を開く（またはスタートメニューで「PowerShell」）：

```powershell
git clone https://github.com/lingmu0788/mp4-split2.git
cd mp4-split2
```

出力例：
```
Cloning into 'mp4-split2'...
remote: Enumerating objects: 20, done.
...
Receiving objects: 100% (20/20), done.
```

---

### **ステップ 5️⃣: 仮想環境を作成**

`mp4-split2` フォルダ内で：

```powershell
python -m venv venv
```

実行後、`venv` フォルダが生成されます。

**仮想環境を有効化:**

```powershell
venv\Scripts\activate
```

成功すると、プロンプトの前に `(venv)` と表示されます：

```
(venv) C:\Users\YourName\mp4-split2>
```

> **重要:** 以降のコマンドはすべて仮想環境が有効な状態で実行してください。

---

### **ステップ 6️⃣: 依存パッケージをインストール**

仮想環境が有効な状態で：

```powershell
pip install -r requirements.txt
```

出力例：
```
Collecting librosa==0.10.0
...
Successfully installed librosa-0.10.0 numpy-1.26.0 ...
```

処理完了まで待ちます（2～3分）。

---

### **ステップ 7️⃣: .env ファイルを作成**

#### **方法 A: PowerShell で作成（推奨）**

仮想環境が有効な状態で：

```powershell
$content = @"
INPUT_FILE=C:\Users\YourName\Downloads\lecture.mp4
OUTPUT_DIR=C:\Users\YourName\Downloads\output
SILENCE_THRESHOLD=0.01
MIN_SILENCE_DURATION=30
"@
$content | Out-File -FilePath .env -Encoding UTF8 -NoNewline
```

> **YourName** をあなたの Windows ユーザー名に変更してください。

確認：

```powershell
type .env
```

#### **方法 B: メモ帳で作成**

1. メモ帳を開く
2. 以下をコピー・ペースト：

```
INPUT_FILE=C:\Users\YourName\Downloads\lecture.mp4
OUTPUT_DIR=C:\Users\YourName\Downloads\output
SILENCE_THRESHOLD=0.01
MIN_SILENCE_DURATION=30
```

3. **YourName** をあなたのユーザー名に変更
4. ファイル → 名前をつけて保存
5. ファイル名: `.env`
6. 形式: **すべてのファイル**を選択
7. `mp4-split2` フォルダに保存

---

### **ステップ 8️⃣: ユーザー名の確認**

自分の Windows ユーザー名がわからない場合：

```powershell
echo $env:USERNAME
```

出力例：
```
suzukishinji
```

このユーザー名を `.env` に使用してください：

```
C:\Users\suzukishinji\Downloads\lecture.mp4
```

---

## 🎬 実行方法

### **最初の実行**

`mp4-split2` フォルダ内で PowerShell を開き：

```powershell
# 仮想環境を有効化（初回のみ）
venv\Scripts\activate

# プログラムを実行
python main.py
```

### **2回目以降**

仮想環境が有効な状態なら：

```powershell
python main.py
```

仮想環境を閉じていた場合は：

```powershell
venv\Scripts\activate
python main.py
```

### **出力例**

```
============================================================
MP4 Split Application - 無音検出動画分割
============================================================
入力ファイル: C:\Users\suzukishinji\Downloads\lecture.mp4
出力ディレクトリ: C:\Users\suzukishinji\Downloads\output
無音判定閾値: 0.01
最小無音時間: 30.0 秒
============================================================
動画時間: 02:18:37
音声を抽出中...
...
処理完了: 7 個のファイルを生成しました
============================================================
```

---

## 📁 Windows でのファイル構成

```
C:\Users\YourName\mp4-split2\
│
├── main.py                      # メインプログラム
├── run.sh                       # Linux/Mac 用実行スクリプト
├── .env                         # 設定ファイル ← 作成が必要
├── README.md                    # 技術仕様書
├── OPERATION_GUIDE.md           # macOS 用操作手順
├── WINDOWS_SETUP_GUIDE.md       # このファイル
├── requirements.txt             # Python 依存パッケージ
├── .gitignore                   # Git 除外ファイル
├── .git\                        # Git リポジトリ（自動作成）
└── venv\                        # Python 仮想環境（自動作成）
    ├── Scripts\
    │   ├── activate.bat         # 仮想環境有効化（Windows）
    │   ├── python.exe
    │   └── ...
    ├── Lib\
    └── ...
```

---

## ⚙️ .env ファイルの設定

### **パラメータの説明**

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `INPUT_FILE` | 分割する MP4 ファイルのパス | `C:\Users\suzukishinji\Downloads\lecture.mp4` |
| `OUTPUT_DIR` | 分割ファイルの出力先 | `C:\Users\suzukishinji\Downloads\output` |
| `SILENCE_THRESHOLD` | 無音判定の感度（0～1） | `0.01` |
| `MIN_SILENCE_DURATION` | 最小無音時間（秒） | `30` |

### **SILENCE_THRESHOLD の選択**

| 値 | 説明 | 推奨 |
|----|------|-----|
| 0.005 | 非常に敏感 | ノイズが少ない場合 |
| **0.01** | **標準（推奨）** | **通常の講義** |
| 0.02 | 鈍感 | ノイズが多い場合 |

### **MIN_SILENCE_DURATION の選択**

| 値（秒） | 説明 | 推奨 |
|---------|------|-----|
| 10 | 短い | 話が頻繁に止まる |
| 15 | 標準 | 通常の講義 |
| **30** | **長い（推奨）** | **ゆっくり・沈黙が長い** |
| 60 | 非常に長い | 長い沈黙のみ |

---

## 📝 実行例

### **例 1: 基本的な分割**

```powershell
# 1. 仮想環境を有効化
venv\Scripts\activate

# 2. 実行
python main.py

# 3. 結果確認
dir C:\Users\YourName\Downloads\output\

# 4. 仮想環境を無効化（終了時）
deactivate
```

### **例 2: 敏感な設定（短い無音も検出）**

`.env` を以下に変更：

```
INPUT_FILE=C:\Users\YourName\Downloads\lecture.mp4
OUTPUT_DIR=C:\Users\YourName\Downloads\output
SILENCE_THRESHOLD=0.005
MIN_SILENCE_DURATION=10
```

実行：

```powershell
python main.py
```

> **結果**: より多くのファイルに分割（10～15ファイル）

### **例 3: 鈍感な設定（明確な無音のみ）**

`.env` を以下に変更：

```
INPUT_FILE=C:\Users\YourName\Downloads\lecture.mp4
OUTPUT_DIR=C:\Users\YourName\Downloads\output
SILENCE_THRESHOLD=0.02
MIN_SILENCE_DURATION=60
```

実行：

```powershell
python main.py
```

> **結果**: 少ないファイルに分割（3～5ファイル）

---

## 🐛 トラブルシューティング

### **❌ "python: コマンドが見つかりません"**

**原因**: Python が PATH に追加されていない

**解決:**
1. Python をアンインストール
2. 再インストール時に「Add Python to PATH」に ✅ チェック
3. PowerShell を再起動

確認：
```powershell
python --version
```

---

### **❌ "ffmpeg: コマンドが見つかりません"**

**原因**: ffmpeg がインストールされていない

**解決:**
```powershell
choco install ffmpeg -y
```

PowerShell を**管理者として実行**する必要があります。

確認：
```powershell
ffmpeg -version
```

---

### **❌ "このシステムではスクリプトの実行が無効になっています"**

**エラー:**
```
.\venv\Scripts\activate : このシステムではスクリプトの実行が無効になっています
```

**解決:**

PowerShell を**管理者として実行**：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

「Y」を入力して Enter

その後、仮想環境を有効化：

```powershell
venv\Scripts\activate
```

---

### **❌ ".env ファイルが見つかりません"**

**エラー:**
```
Error: [Errno 2] No such file or directory: '.env'
```

**解決:**

1. `mp4-split2` フォルダに `.env` ファイルが存在するか確認：

```powershell
dir /a .env
```

2. 存在しない場合は [ステップ 7️⃣](#ステップ-7️⃣-env-ファイルを作成) を参照して作成

3. ファイル名が正しいか確認（`.env` であって `.env.txt` ではない）

---

### **❌ "INPUT_FILE が見つかりません"**

**エラー:**
```
Error: 入力ファイルが見つかりません
```

**解決:**

1. ファイルが実際に存在するか確認：

```powershell
dir "C:\Users\YourName\Downloads\lecture.mp4"
```

2. 存在しない場合は、正しいパスに変更

**ファイルパスの確認方法:**
- ファイルを右クリック → 「プロパティ」
- 「詳細」タブで「場所」を確認
- そのパスを `.env` に使用

---

### **❌ "OUTPUT_DIR に書き込み権限がありません"**

**エラー:**
```
Error: [Errno 13] Permission denied
```

**解決:**

1. 別のフォルダに出力：

```
OUTPUT_DIR=C:\Users\YourName\Desktop\output
```

2. または、フォルダのプロパティで権限を確認

---

### **❌ "処理が非常に遅い"**

**原因**: ディスク容量不足、または大きなファイル

**確認:**

1. ディスク容量：

```powershell
Get-Volume
```

2. ファイルサイズ：

```powershell
(Get-Item "C:\Users\YourName\Downloads\lecture.mp4").Length / 1GB
```

**解決**: ディスク容量を確保

---

### **❌ 仮想環境が有効化できない**

**エラー:**
```
cannot be loaded because running scripts is disabled
```

**解決:**

PowerShell を**管理者として実行**：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

「Y」を入力

---

## ⚡ 実行スクリプト作成（オプション）

毎回コマンドを入力するのが面倒な場合、実行スクリプトを作成できます。

### **run.bat を作成**

1. メモ帳を開く
2. 以下をコピー・ペースト：

```batch
@echo off
REM mp4-split2 実行スクリプト (Windows)
cd /d "%~dp0"
echo mp4-split2 を起動します...
call venv\Scripts\activate
python main.py
pause
```

3. ファイル → 名前をつけて保存
4. ファイル名: `run.bat`
5. 形式: **すべてのファイル**
6. `mp4-split2` フォルダに保存

### **使用方法**

`mp4-split2` フォルダ内の `run.bat` をダブルクリック！

```
mp4-split2 を起動します...
(venv) C:\Users\...\mp4-split2>
```

---

## ✨ 最終確認チェックリスト

すべてにチェック ✅ を付けてから実行：

- [ ] Git がインストールされている
  ```powershell
  git --version
  ```

- [ ] Python がインストールされている
  ```powershell
  python --version
  ```

- [ ] ffmpeg がインストールされている
  ```powershell
  ffmpeg -version
  ```

- [ ] mp4-split2 がクローンされている
  ```powershell
  cd C:\Users\YourName\mp4-split2
  ```

- [ ] 仮想環境が作成されている
  ```powershell
  dir venv
  ```

- [ ] 仮想環境が有効化できる
  ```powershell
  venv\Scripts\activate
  ```

- [ ] 依存パッケージがインストールされている
  ```powershell
  pip list | findstr librosa
  ```

- [ ] .env ファイルが存在する
  ```powershell
  type .env
  ```

- [ ] INPUT_FILE が存在する
  ```powershell
  dir "C:\Users\YourName\Downloads\lecture.mp4"
  ```

- [ ] OUTPUT_DIR が存在する（またはフォルダを作成）
  ```powershell
  mkdir "C:\Users\YourName\Downloads\output"
  ```

すべて確認できたら実行！

```powershell
python main.py
```

---

## 📞 サポート

### **参考リンク**

- **Python**: https://www.python.org/
- **Git**: https://git-scm.com/
- **ffmpeg**: https://ffmpeg.org/download.html
- **Chocolatey**: https://chocolatey.org/
- **GitHub リポジトリ**: https://github.com/lingmu0788/mp4-split2

### **よくある質問**

**Q: 複数の動画を処理したい**

A: 複数回実行するか、`.env` でファイルを変更して実行してください。

**Q: 他の形式（MOV, AVI など）に対応している？**

A: ffmpeg がサポートしている形式なら対応可能です。

**Q: 出力ファイル名を変更したい**

A: `main.py` の `split_video()` メソッドを修正してください（詳細は `README.md` を参照）。

---

## 🎉 完了！

すべてのセットアップが完了したら、mp4-split2 で動画分割を楽しんでください！ 🚀

---

**作成日**: 2025-12-27  
**対応OS**: Windows 11  
**ステータス**: ✅ セットアップ完了  

何か問題が発生した場合は、このガイドの **トラブルシューティング** セクションを参照してください。

