from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

@app.route('/')
def index():
    return render_template('shin.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    mbti_report = data['mbtiReport']
    big_five_report = data['bigFiveReport']

    # Generate content for MBTI type
    mbti_prompt = f"Given the MBTI personality type {mbti_report}, suggest positive qualities and suitable career paths. Provide detailed and positive suggestions."
    mbti_response = model.generate_content(mbti_prompt)

    # Generate content for Big Five personality traits
    big_five_prompt = f"Given the Big Five personality traits {big_five_report}, describe the positive qualities and suitable career paths. Focus on positive and uplifting suggestions."
    big_five_response = model.generate_content(big_five_prompt)

    return jsonify({
        "mbtiReport": mbti_report,
        "bigFiveReport": big_five_report,
        "mbtiSuggestions": mbti_response.text,
        "bigFiveSuggestions": big_five_response.text
    })

if __name__ == '__main__':
    app.run(port=5008,debug=True)
