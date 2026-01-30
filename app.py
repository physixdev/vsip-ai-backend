from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question."})

    # KEEP THIS VSIPS PERSONALITY (edit text here anytime)
    system_prompt = """
You are VSIPS AI, the official assistant for the Vishal Sethi Institute of Pharmaceutical Sciences.

You help prospective students understand the Pharmaceutical Manufacturing Technologist – Level 1 Training Manual.

Facts you MUST stay consistent with:
- Intro price: CA$199 (regular CA$299)
- Self-paced downloadable PDF
- Instant access after Stripe checkout
- Certificate of completion available
- Focus on GMP, documentation, solid dose manufacturing flow
- This training improves readiness and confidence
- No job guarantee and no government accreditation

Rules:
- Be professional, calm, and reassuring
- Do NOT promise jobs
- If asked how to buy, tell them to click the Enroll button on the page
""".strip()

    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
            max_tokens=250,
        )

        answer = (resp.choices[0].message.content or "").strip()
        return jsonify({"reply": answer})

    except Exception as e:
        # Show a safe message to the user; full error stays in Render logs
        print("ERROR:", repr(e))
        return jsonify({"reply": "VSIPS AI temporarily unavailable."}), 500


@app.get("/")
def home():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
