from flask import Flask, request, jsonify
import openai
import os

# 환경변수에서 키 읽기 (Render 환경변수 사용 시)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        user_message = request.json['userRequest']['utterance']
        prompt = f"""너는 서울 강서구 선정형외과 실장이다. 병원 예약, 위치, 진료시간, 주차 등 안내만 친절한 존댓말로 해줘.
        진료비 등 민감한 건 "전화 문의만 가능합니다"로 답해. 질문: {user_message}"""

        completion = client.chat.completions.create(
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
    except Exception as e:
        # 에러 메시지와 실제로 받은 request 내용을 로그에 모두 출력
        print("에러 발생:", e)
        print("request.json:", request.json)
        return jsonify({"error": str(e), "req": str(request.json)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
