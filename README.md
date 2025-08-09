# コーディング課題 解説ジェネレーター

このプロジェクトは、ユーザーが入力したコーディング課題に対して、解説記事とGoogle Colab用のNotebookを生成するStreamlitアプリケーションです。

## セットアップ

### 必要条件

- Python 3.x
- `pip` (Pythonパッケージマネージャ)

### 仮想環境の作成

1. 仮想環境を作成します。
   ```bash
   python3 -m venv myenv
   ```

2. 仮想環境を有効化します。
   ```bash
   source myenv/bin/activate
   ```

### 依存関係のインストール

`requirements.txt` ファイルを使用して、必要なパッケージをインストールします。(streamlit cloud用にpython-dotenvがコメントアウトされているので、必要に応じて修正してください）

```bash
pip install -r requirements.txt
```

## APIキーの設定

このアプリケーションはOpenAI APIを使用します。APIキーの設定方法は以下の通りです。

- **ローカル環境**: `.env` ファイルをプロジェクトのルートディレクトリに作成し、以下のようにAPIキーを設定してください。
  ```
  OPENAI_API_KEY=your_openai_api_key_here
  ```

- **Streamlit Cloud**: StreamlitのSecrets管理を使用して、`OPENAI_API_KEY` を設定してください。

## モデルとトークンの設定

- **モデル**: 使用するモデルはコード内で指定されていますが、必要に応じてお好みのモデルに変更してください。
- **最大トークン数**: `max_output_tokens` の値もお好みで調整可能です。

## アプリケーションの起動

仮想環境を有効にした状態で、以下のコマンドを実行してアプリケーションを起動します。

```bash
streamlit run main.py
```

## 使用方法

1. アプリケーションを起動すると、ブラウザにインターフェースが表示されます。
2. コーディングの課題文を入力し、「解説を生成」ボタンをクリックします。
3. 解説記事とNotebookが生成され、ダウンロード可能になります。

---

このプロジェクトは、教育目的での使用を想定しています。