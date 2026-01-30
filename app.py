from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up OpenAI client (new style)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")

    prompt = """
You are VSIPS AI, the official assistant for the Vishal Sethi Institute of Pharmaceutical Sciences.

You help prospective students understand the
Pharmaceutical Manufacturing Technologist – Level 1 Training Manual.

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
"""


    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        print("🔍 FULL RESPONSE:", response)
        answer = response.choices[0].message.content.strip()
        return jsonify({"reply": answer})
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("🔥 ERROR TRACEBACK:\\n", error_message)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
