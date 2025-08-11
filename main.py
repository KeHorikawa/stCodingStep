# main.py

import os
import re
import json
import streamlit as st
from openai import OpenAI

# プロンプトファイルから読み込み
try:
    from prompts import (
        INPUT_CHECK_PROMPT,
        BASE_PROMPT,
        NOTEBOOK_PROMPT
    )
except ImportError:
    st.error("prompts.py ファイルが見つかりません")
    st.stop()

# --- 両対応APIキー取得 ---
API_KEY = None
try:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("OPENAI_API_KEY")
except Exception:
    pass

if not API_KEY:
    try:
        API_KEY = st.secrets["OPENAI_API_KEY"]
    except Exception:
        API_KEY = None

if not API_KEY:
    st.error("OpenAI APIキーが設定されていません。\n\n"
             "ローカル実行の場合は .env ファイルに OPENAI_API_KEY を設定してください。\n"
             "Streamlit Cloud の場合は Secrets に OPENAI_API_KEY を追加してください。")
    st.stop()

# OpenAI クライアントの初期化
client = OpenAI(api_key=API_KEY)


def extract_pure_json(text: str) -> str | None:
    """ API 応答から Notebook JSON 部分だけを抽出する """
    m = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"({[\s\S]*})", text)
    if m2:
        return m2.group(1)
    return None


def validate_notebook_json(json_str: str) -> tuple[bool, list[str]]:
    """生成されたJSONが正しい.ipynb形式かチェックし、不足しているキーを返す"""
    try:
        data = json.loads(json_str)
        required_keys = ["cells", "metadata", "nbformat", "nbformat_minor"]
        missing_keys = [key for key in required_keys if key not in data]
        is_valid = len(missing_keys) == 0
        return is_valid, missing_keys
    except Exception:
        return False, ["JSON形式が不正です"]


def main():
    st.title("コーディング課題 解説ジェネレーター")

    # セッション状態の初期化
    if 'explanation_md' not in st.session_state:
        st.session_state.explanation_md = None
    if 'notebook_json' not in st.session_state:
        st.session_state.notebook_json = None

    # 1) ユーザ入力
    challenge = st.text_area(
        "コーディングの課題文を入力してください",
        height=200
    )

    # 2) 生成トリガー
    model = "gpt-5-mini"
    if st.button("解説を生成"):
        if not challenge.strip():
            st.error("まずは課題文を入力してください。")
            return

        if len(challenge) > 500:
            st.error("課題文は500文字以内にしてください。")
            return

        # 入力文がコーディング課題かどうかをチェックする
        with st.spinner("入力課題をチェック中…"):
            try:
                resp1 = client.responses.create(
                    model=model,
                    input=f"{INPUT_CHECK_PROMPT}\n[課題]\n{challenge}"
                )
                if not resp1.output_text.strip().lower().startswith("yes"):
                    st.error("入力課題がコーディング課題ではありません。")
                    return
            except Exception as e:
                st.error(f"APIエラー: {e}")
                return

        # 解説記事 (Markdown) の生成
        with st.spinner("解説記事を生成中…"):
            try:
                resp1 = client.responses.create(
                    model=model,
                    max_output_tokens=5000,
                    input=f"{BASE_PROMPT}\n[課題]\n{challenge}"
                )
                st.session_state.explanation_md = resp1.output_text
            except Exception as e:
                st.error(f"APIエラー: {e}")
                return

        # Notebook (.ipynb) の生成
        with st.spinner("Notebookファイルを生成中…"):
            try:
                resp2 = client.responses.create(
                    model=model,
                    max_output_tokens=5000,
                    input=(f"{NOTEBOOK_PROMPT}\n[マークダウン記事]\n"
                           f"{st.session_state.explanation_md}")
                )
                notebook_json = extract_pure_json(resp2.output_text)
                
                # JSONの検証
                if notebook_json:
                    is_valid, missing_keys = validate_notebook_json(notebook_json)
                    st.session_state.notebook_json = notebook_json
                    
                    if not is_valid:
                        st.warning("⚠️ Notebook JSONの形式に問題があります。")
                        st.info(f"不足しているキー: {', '.join(missing_keys)}")
                        st.info("ダウンロードは可能ですが、Google Colabでの実行に問題がある可能性があります。")
                else:
                    st.error("Notebook JSON の抽出に失敗しました。")
                    return
                    
            except Exception as e:
                st.error(f"APIエラー: {e}")
                return

        st.success(
            "生成完了！下記のダウンロードボタンからファイルを取得できます。"
        )

    # 3) 生成結果の表示とダウンロード
    if st.session_state.explanation_md:
        st.subheader("📝 解説記事 (Markdown)")
        st.markdown(st.session_state.explanation_md)
        st.download_button(
            label="Markdownファイルをダウンロード",
            data=st.session_state.explanation_md,
            file_name="explanation.md",
            mime="text/markdown",
            key="md_download"
        )

    if st.session_state.notebook_json:
        st.subheader("📓 Google Colab 用 Notebook")
        st.download_button(
            label="Notebookファイル(.ipynb)をダウンロード",
            data=st.session_state.notebook_json,
            file_name="explanation_notebook.ipynb",
            mime="application/json",
            key="ipynb_download"
        )
    elif (st.session_state.explanation_md and 
          not st.session_state.notebook_json):
        st.error("Notebook JSON の抽出に失敗しました。")


if __name__ == "__main__":
    main()
