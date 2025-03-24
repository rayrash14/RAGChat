import os
from huggingface_hub import InferenceClient  # To interact with Hugging Face's API for inference

# Retrieve the Hugging Face token and repository ID from environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
HUGGING_FACE_REPO_ID = os.getenv("HUGGING_FACE_REPO_ID")

# Print some information for debugging purposes (HF_TOKEN is partially displayed for privacy)
print("✅ Inside llm.py")
print("HF_TOKEN:", HF_TOKEN[:8] + "..." if HF_TOKEN else "❌ NOT FOUND")
print("HUGGING_FACE_REPO_ID:", HUGGING_FACE_REPO_ID)

# HF_TOKEN = os.getenv("HF_TOKEN")
# HUGGING_FACE_REPO_ID = os.getenv("HUGGING_FACE_REPO_ID", "mistralai/Mistral-7B-Instruct-v0.3")

# Function to load the LLM (Large Language Model) for inference
def load_llm():
    if not HF_TOKEN:
        raise EnvironmentError("HF_TOKEN not set in environment.")

    client = InferenceClient(
        model=HUGGING_FACE_REPO_ID,
        token=HF_TOKEN
    )
    
    # Define a function to generate responses from the LLM given a prompt
    def generate(prompt: str) -> str:
        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=512,
            temperature=0.3,
            stop_sequences=["</s>"]
        )
        return response

    return generate
