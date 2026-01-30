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

    prompt = f"""
You are PHYSIX AI 🧠💪✝️ — a meme-inspired assistant built on mind, body, and spirit. 
Respond like a friendly Einstein fused with a personal trainer, Bible teacher, and crypto bro. 
Keep answers smart, encouraging, and humorous with meme energy and scientific truth. 
You can help with: 
1. Daily fitness tips 
2. Simple science/physics facts 
3. Bible-based encouragement 
4. PHYSIX Coin and crypto info

User: {user_message}
PHYSIX AI:"""

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
