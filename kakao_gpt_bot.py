from flask import Flask, request, jsonify
import openai
import os   # 환경변수 사용을 위해 추가!

app = Flask(__name__)

# 환경변수에서 키 읽어오기
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    user_message = request.json['userRequest']['utterance']
    prompt = f"""너는 서울 강서구 선정형외과 실장이다. 병원 예약, 위치, 진료시간, 주차 등 안내만 친절한 존댓말로 해줘.
    진료비 등 민감한 건 "전화 문의만 가능합니다"로 답해. 질문: {user_message}"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    answer = completion.choices[0].message.content

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": answer}}
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
