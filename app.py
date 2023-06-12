import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
あなたは文章を単語に分類してタグをつけるシステムです。
以下のルールを厳格に守ってください。
・文章の単語をそれぞれ以下のいずれかの「タグ」に分類してください
　・Country
　・Prefecture
　・City
　・Country sub division
　・Street number
　・Street name

・タグは上記の順番で回答してください。
・入力の「,」は回答不要です。
・全ての単語を「タグ名：単語/」のフォーマットで回答してください。

・入力が「Toyosu Building , 3-3-3 Toyosu, Koto-ku, Tokyo, Japan」の場合は、以下の通り回答してください。
　Country:Japan
　Prefecture:Tokyo
　Country sub division:Koto-ku
　Country sub division:Toyosu
　Street number:3-3-3
　Street name:Toyosu Building

・入力が「Aichi kencho, 3-1-2 Sannomaru, Naka-ku, Nagoya, Aichi, Japan」の場合は、以下の通り回答してください。
　Country:Japan
　Prefecture:Aichi
　City:Nagoya
　Country sub division:Naka-ku
　Country sub division:Sannomaru
　Street number:3-1-2
　Street name:Aich kencho
"""


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("フォーマット変換します")
#st.image("bom_v2.1.png")
st.write("変換前の住所を設定してください。")
st.write("例：Toyosu Building, 3-3-3 Toyosu, Koto-ku, Tokyo, Japan")

user_input = st.text_input("変換前の住所", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
