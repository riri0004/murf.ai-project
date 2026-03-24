from flask import Flask, render_template, request, jsonify
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

NEWS_API_KEY = "a3c957e86e0c401aa28f6d47058e6d8f"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_news", methods=["POST"])
def get_news():
    try:
        data = request.json
        language = data.get("language", "en")

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        print("RAW API RESPONSE:", data)

        articles = data.get("articles", [])

        news_list = []

        for article in articles[:10]:
            title = article.get("title")
            description = article.get("description")

            if not title:
                continue

            full_text = f"{title}. {description or ''}"

            # ✅ TRANSLATION PART (FIX)
            if language != "en":
                try:
                    title = GoogleTranslator(source="auto", target=language).translate(title)
                    full_text = GoogleTranslator(source="auto", target=language).translate(full_text)
                except Exception as e:
                    print("TRANSLATION ERROR:", e)

            news_list.append({
                "title": title,
                "full": full_text
            })

        print("FINAL NEWS:", news_list)

        return jsonify(news_list)

    except Exception as e:
        print("ERROR:", e)
        return jsonify([])

# 🎧 Murf AI
@app.route("/speak", methods=["POST"])
def speak():
    try:
        text = request.json["text"]

        url = "https://api.murf.ai/v1/speech/generate"

        headers = {
            "api-key": "ap2_6991fbcf-3de1-4852-bccc-03da9762b4c4",
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "voiceId": "en-US-natalie",
            "format": "mp3"
        }

        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        print("MURF FULL RESPONSE:", result)

        # ✅ SUPER SAFE EXTRACTION
        audio_url = None

        if "audioFile" in result:
            audio_url = result["audioFile"]

        elif "audio_url" in result:
            audio_url = result["audio_url"]

        elif "data" in result:
            audio_url = result["data"].get("audioFile") or result["data"].get("audio_url")

        if not audio_url:
            print("❌ No audio found in response")
            return jsonify({"audio": ""})

        return jsonify({"audio": audio_url})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"audio": ""})
if __name__ == "__main__":
    app.run(debug=True)