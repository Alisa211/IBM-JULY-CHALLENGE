import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference

# Load credentials from .env
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

if not API_KEY or not PROJECT_ID:
    print("Error: WATSONX_API_KEY or WATSONX_PROJECT_ID missing from .env")
    exit(1)

print("Testing Watsonx API Connection...")
print(f"Project ID: {PROJECT_ID}")

try:
    # Initialize the model inference client
    model = ModelInference(
        model_id="ibm/granite-4-h-small", # Using a model supported in your environment
        credentials={
            "apikey": API_KEY,
            "url": "https://us-south.ml.cloud.ibm.com"
        },
        project_id=PROJECT_ID,
        params={
            "max_new_tokens": 50,
            "temperature": 0.5
        }
    )

    # Test generation
    response = model.generate_text("Say hello in one short sentence.")
    print("\n--- Success! Model Response: ---")
    print(response.strip())
    print("--------------------------------")

except Exception as e:
    print("\n!!! Connection Failed !!!")
    print(str(e))
    print("\nPlease verify:")
    print("1. Your API key is correct")
    print("2. The Project ID matches the one in Watsonx")
    print("3. You have the 'watsonx.ai Runtime' service associated with the project")
