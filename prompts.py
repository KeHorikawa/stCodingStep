# 入力がコーディング課題かどうかをチェック
INPUT_CHECK_PROMPT = """あなたは優秀なPython講師です。
ユーザーの入力が、コーディングの課題かどうかをチェックしてください。
コーディングの課題であれば、「yes」と返答してください。"""

# ベースプロンプト（解説記事用）
BASE_PROMPT = """あなたは優秀なPython講師です。
以下の課題を初心者向けに step by step で動作確認しながらコードを完成させる手順を解説する
ブログ記事を、マークダウン形式で書いてください。"""

# Notebook 生成用プロンプト（ipynb不具合修正版）
NOTEBOOK_PROMPT = """以下のマークダウン記事を、Google Colab で動作確認できる Notebook 形式（.ipynb）の JSON として出力してください。

**重要な指示：**
1. マークダウンの見出し（#）ごとに新しいセルを作成
2. コードブロック（```python）は実行可能なコードセルとして作成
3. 説明文はmarkdownセルとして作成
4. 各セルは適切に分割し、読みやすくする
5. 必ず正しい.ipynb形式のJSON構造で出力

以下の形式で出力してください：
```json
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["# 課題の説明\\n", "課題文と目標"]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": ["# ステップ1: 必要なライブラリのインポート\\n", "import numpy as np"]
    }
  ],
  "metadata": {
    "colab": {
      "name": "コーディング課題解説",
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

出力は純粋な JSON のみとし、余計なテキストを含めないようにしてください。"""
