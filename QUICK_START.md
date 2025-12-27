# 🚀 MP4 Split 2 - クイックスタート

## ⚡ 最短実行手順（初回のみ）

```bash
# 1️⃣ ディレクトリに移動
cd /Users/suzukishinji/projects/mp4-split2

# 2️⃣ 仮想環境を作成・有効化
python3 -m venv venv
source venv/bin/activate

# 3️⃣ 依存ライブラリをインストール
pip install librosa numpy python-dotenv

# 4️⃣ .env ファイルを作成
cp env.example .env

# 5️⃣ 実行
./run.sh
```

---

## 🔄 次回以降の実行手順（毎回）

```bash
# 1️⃣ ディレクトリに移動
cd /Users/suzukishinji/projects/mp4-split2

# 2️⃣ 仮想環境を有効化
source venv/bin/activate

# 3️⃣ 実行
./run.sh
```

---

## ⚙️ パラメータ調整（オプション）

分割数を調整したい場合は `.env` を編集：

```bash
# .env を編集
nano .env

# 例：MIN_SILENCE_DURATION を 30 に変更
# MIN_SILENCE_DURATION=30
```

---

## 📊 実行結果

実行完了時にターミナルに表示：

```
【生成ファイル一覧】
ファイル名                                  サイズ
────────────────────────────────────────────────
lecture_001.mp4                            40.1M
lecture_002.mp4                           110.0M
...
────────────────────────────────────────────────
合計                                     1,213.5M
```

分割ファイルは `output/` ディレクトリに保存されます。

---

## 🎯 まとめ

| フェーズ | 回数 |
|---------|------|
| 初回セットアップ | 1回 |
| 毎回の実行 | 3コマンド |

**シンプルです！** 🚀

