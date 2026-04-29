

import babyagi
import os
import logging

app = babyagi.create_app('/dashboard')

# Add OpenAI key to enable automated descriptions and embedding of functions.
for env_name, key_name in {
    'OPENAI_API_KEY': 'openai_api_key',
    'OPENAI_API_BASE': 'openai_api_base',
    'OPENAI_BASE_URL': 'openai_base_url',
    'ANTHROPIC_API_KEY': 'anthropic_api_key',
    'ANTHROPIC_API_BASE': 'anthropic_api_base',
    'ANTHROPIC_BASE_URL': 'anthropic_base_url',
    'ANTHROPIC_MODEL': 'anthropic_model',
    'BABYAGI_LLM_MODEL': 'babyagi_llm_model',
    'BABYAGI_EMBEDDING_MODEL': 'babyagi_embedding_model',
}.items():
    if os.getenv(env_name):
        babyagi.add_key_wrapper(key_name, os.environ[env_name])

logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return f"Welcome to the main app. Visit <a href=\"/dashboard\">/dashboard</a> for BabyAGI dashboard."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
