

import babyagi
import os
import logging

app = babyagi.create_app('/dashboard')

# Add OpenAI key to enable automated descriptions and embedding of functions.
# babyagi.add_key_wrapper('openai_api_key',os.environ['OPENAI_API_KEY'])

logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return f"Welcome to the main app. Visit <a href=\"/dashboard\">/dashboard</a> for BabyAGI dashboard."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
