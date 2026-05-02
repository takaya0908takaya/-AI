import os
import random
from dotenv import load_dotenv
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# .envファイル読み込み
load_dotenv()

# APIキー取得
api_key = os.getenv("GEMINI_API_KEY")

# モデル名
model_name = "gemini-2.0-flash"

# Geminiクライアント作成
client = genai.Client(api_key=api_key)

# Gemini設定
config = GenerateContentConfig(
    tools=[Tool(google_search=GoogleSearch())],
    response_modalities=["TEXT"],
    max_output_tokens=256
)

# 都道府県一覧
prefecture_names = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県",
    "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県",
    "沖縄県"
]

# 挨拶
def print_greeting():
    print("博士：こんにちは。私は地理に詳しい博士です。")
    print("　　　都道府県クイズを始めましょう！")
    print("　　　「おしまい」と入力すると終了できます。\n")

# ヒント生成
def generate_hint(pref_name):
    prompt = f"""
あなたは日本の地理に詳しい博士です。

次の都道府県について、
都道府県名を絶対に出さずに、
特徴的なヒントを3つ出してください。

100文字以内で簡潔に答えてください。

都道府県: {pref_name}
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )

    return response.text.strip()

# 正解時の説明
def explain_correct(pref_name):
    prompt = f"""
あなたは日本地理に詳しい博士です。

{pref_name}について、
観光・食べ物・地理などを含めて、
100文字以内でやさしく説明してください。
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )

    return response.text.strip()

# 不正解時
def explain_wrong(correct_pref, wrong_pref):
    prompt = f"""
ユーザーは「{wrong_pref}」と答えましたが不正解です。

「{wrong_pref}」について軽く触れつつ、
正解の都道府県につながる追加ヒントを
100文字以内で出してください。

正解の都道府県名は絶対に言わないでください。
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )

    return response.text.strip()

# クイズ本体
def start_quiz():
    print_greeting()

    while True:
        answer = random.choice(prefecture_names)

        print("博士：問題です！")
        print("　　　この都道府県はどこでしょう？\n")

        hint = generate_hint(answer)

        print("【ヒント】")
        print(hint)
        print()

        while True:
            user_input = input("あなたの答え：").strip()

            if user_input == "おしまい":
                print("\n博士：お疲れさまでした！また挑戦してくださいね。")
                return

            if user_input == answer:
                print("\n博士：正解です！")
                print(explain_correct(answer))
                print()
                break

            else:
                print("\n博士：不正解です。")
                print(explain_wrong(answer, user_input))
                print("\n【もう一度ヒント】")
                print(hint)
                print()

# 実行
if __name__ == "__main__":
    start_quiz()