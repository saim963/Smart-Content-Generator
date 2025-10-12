# list_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

print("🛰️  Asking Google for a list of available models for your key...")
load_dotenv()

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in your .env file!")

    genai.configure(api_key=api_key)

    print("\n✅ Here are the models you can use:\n")

    # This loop checks every available model...
    for m in genai.list_models():
      # ...and only prints the ones that support content generation
      if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")

except Exception as e:
    print(f"\n❌ An error occurred while trying to list models.")
    print("   Error details:", e)