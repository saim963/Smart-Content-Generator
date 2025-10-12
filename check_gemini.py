# check_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

print("🚀 Attempting to connect to Google's Gemini API...")

# Load the .env file where your key is stored
load_dotenv()

try:
    # Get the key and configure the library
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in your .env file!")

    genai.configure(api_key=api_key)

    # Make a very simple, low-cost API call to the free tier model
    model = genai.GenerativeModel('gemini-pro-latest')
    response = model.generate_content("Can you hear me? Respond with a single word.")

    # If the code reaches here, the key is working!
    print("\n✅ Success! Your Gemini API key is working perfectly.")
    print("🤖 Gemini's Response:", response.text)

except Exception as e:
    # If there's any kind of error, it will be caught and printed here
    print(f"\n❌ Failure! There seems to be an issue.")
    print("   Error details:", e)