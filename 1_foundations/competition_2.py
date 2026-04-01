import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display

# Load environment variables
load_dotenv(override=True)

# Get API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

# Initialize clients
openai = OpenAI(api_key=openai_api_key)
claude = Anthropic(api_key=anthropic_api_key)
gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")
# ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

# Define the question
question = "How many 'r's are in the word strawberry"
messages = [{"role": "user", "content": question}]

# Define all models from the competition
models = [
    {
        "name": "gpt-4o-mini",
        "client": openai,
        "method": "chat.completions.create",
        "params": {"model": "gpt-4o-mini", "messages": messages}
    },
    {
        "name": "claude-3-7-sonnet-latest",
        "client": claude,
        "method": "messages.create",
        "params": {"model": "claude-3-7-sonnet-latest", "messages": messages, "max_tokens": 1000}
    },
    {
        "name": "gemini-2.0-flash",
        "client": gemini,
        "method": "chat.completions.create",
        "params": {"model": "gemini-2.0-flash", "messages": messages}
    },
    {
        "name": "deepseek-chat",
        "client": deepseek,
        "method": "chat.completions.create",
        "params": {"model": "deepseek-chat", "messages": messages}
    },
    # {
    #     "name": "llama3.2",
    #     "client": ollama,
    #     "method": "chat.completions.create",
    #     "params": {"model": "llama3.2", "messages": messages}
    # }
]

def query_model(model_config):
    """Query a single model and return the response"""
    try:
        client = model_config["client"]
        method_name = model_config["method"]
        params = model_config["params"]
        
        # Get the method from the client
        method = getattr(client, method_name)
        
        # Call the method with parameters
        response = method(**params)
        
        # Extract the answer based on the model type
        if model_config["name"].startswith("claude"):
            answer = response.content[0].text
        else:
            answer = response.choices[0].message.content
            
        return {
            "model": model_config["name"],
            "answer": answer,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "model": model_config["name"],
            "answer": f"Error: {str(e)}",
            "status": "error"
        }

def main():
    """Main function to query all models"""
    print("=" * 60)
    print("QUERYING ALL MODELS: How many 'r's are in the word 'strawberry'?")
    print("=" * 60)
    print()
    
    results = []
    
    for model_config in models:
        print(f"Querying {model_config['name']}...")
        result = query_model(model_config)
        results.append(result)
        
        print(f"Model: {result['model']}")
        print(f"Status: {result['status']}")
        print(f"Answer: {result['answer']}")
        print("-" * 40)
        print()
    
    # Summary
    print("SUMMARY:")
    print("=" * 40)
    successful_results = [r for r in results if r['status'] == 'success']
    failed_results = [r for r in results if r['status'] == 'error']
    
    print(f"Successfully queried: {len(successful_results)} models")
    print(f"Failed queries: {len(failed_results)} models")
    
    if failed_results:
        print("\nFailed models:")
        for result in failed_results:
            print(f"  - {result['model']}: {result['answer']}")
    
    print("\nAll responses:")
    for result in results:
        print(f"\n{result['model']}:")
        print(f"  {result['answer']}")

if __name__ == "__main__":
    main()
