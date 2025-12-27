#!/bin/bash

# MP4 Split シンプル版 実行スクリプト
# 仮想環境を有効化して main.py を実行

cd "$(dirname "$0")" || exit 1

# 仮想環境を有効化（存在する場合）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# main.py を実行
python main.py






