# this is a simple example of registering two functions into babyagi, executing the function stored in the database, and loading the dashboard

import babyagi
import os
import logging

app = babyagi.create_app('/dashboard')

# Add provider settings to enable automated descriptions and embedding of functions.
for env_name, key_name in {
    'OPENAI_API_KEY': 'openai_api_key',
    'OPENAI_API_BASE': 'openai_api_base',
    'OPENAI_BASE_URL': 'openai_base_url',
    'ANTHROPIC_API_KEY': 'anthropic_api_key',
    'ANTHROPIC_API_BASE': 'anthropic_api_base',
    'ANTHROPIC_BASE_URL': 'anthropic_base_url',
    'ANTHROPIC_MODEL': 'anthropic_model',
    'ANTHROPIC_LLM_PROVIDER': 'anthropic_llm_provider',
    'BABYAGI_LLM_MODEL': 'babyagi_llm_model',
    'BABYAGI_EMBEDDING_MODEL': 'babyagi_embedding_model',
}.items():
    if os.getenv(env_name):
        babyagi.add_key_wrapper(key_name, os.environ[env_name])

@babyagi.register_function()
def world():
    return "world"

@babyagi.register_function(dependencies=["world"])
def hello_world():
    x = world()
    return f"Hello {x}!"

logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return f"Welcome to the main app. Visit <a href=\"/dashboard\">/dashboard</a> for BabyAGI dashboard."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
