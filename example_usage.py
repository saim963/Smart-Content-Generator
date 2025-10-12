"""
Example usage of the Gemini Content API
"""
import requests
import json

API_URL = "http://localhost:8000"

def example_1_generate_story():
    """Generate a creative story"""
    print("Example 1: Generate Story")
    print("-" * 50)
    
    response = requests.post(
        f"{API_URL}/api/generate",
        json={
            "prompt": "Write a short sci-fi story about a programmer who discovers their code is alive",
            "temperature": 0.9,
            "max_tokens": 500
        }
    )
    
    result = response.json()
    if result['success']:
        print(result['data']['generated_text'])
    print("\n")

def example_2_summarize_article():
    """Summarize a long article"""
    print("Example 2: Summarize Article")
    print("-" * 50)
    
    long_text = """
    Python is a high-level, interpreted programming language known for its simplicity and readability.
    Created by Guido van Rossum and first released in 1991, Python has become one of the most popular
    programming languages in the world. Its design philosophy emphasizes code readability with the use
    of significant indentation. Python is dynamically typed and garbage-collected, supporting multiple
    programming paradigms including structured, object-oriented, and functional programming.
    
    Python's extensive standard library is one of its greatest strengths, providing tools for everything
    from file I/O to web services. The language has a large and active community that has created thousands
    of third-party packages available through the Python Package Index (PyPI). Popular frameworks like
    Django and Flask for web development, NumPy and Pandas for data science, and TensorFlow and PyTorch
    for machine learning have made Python the go-to language for many domains.
    """
    
    response = requests.post(
        f"{API_URL}/api/summarize",
        json={
            "text": long_text,
            "length": "short"
        }
    )
    
    result = response.json()
    if result['success']:
        print(f"Summary: {result['data']['summary']}")
    print("\n")

def example_3_translate_multiple():
    """Translate to multiple languages"""
    print("Example 3: Multiple Translations")
    print("-" * 50)
    
    text = "Good morning! How are you today?"
    languages = ["Spanish", "French", "German", "Hindi"]
    
    for lang in languages:
        response = requests.post(
            f"{API_URL}/api/translate",
            json={
                "text": text,
                "target_language": lang
            }
        )
        
        result = response.json()
        if result['success']:
            print(f"{lang}: {result['data']['translated']}")
    print("\n")

def example_4_explain_complex_code():
    """Explain a complex code snippet"""
    print("Example 4: Explain Complex Code")
    print("-" * 50)
    
    code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
    """
    
    response = requests.post(
        f"{API_URL}/api/explain-code",
        json={
            "code": code,
            "language": "Python"
        }
    )
    
    result = response.json()
    if result['success']:
        print(result['data']['explanation'])
    print("\n")

def example_5_qa_with_context():
    """Ask questions with context"""
    print("Example 5: Q&A with Context")
    print("-" * 50)
    
    questions = [
        {
            "question": "What are the benefits of using FastAPI?",
            "context": "For building production-ready APIs"
        },
        {
            "question": "How does async/await work?",
            "context": "In Python asyncio programming"
        }
    ]
    
    for q in questions:
        response = requests.post(
            f"{API_URL}/api/qa",
            json=q
        )
        
        result = response.json()
        if result['success']:
            print(f"Q: {result['data']['question']}")
            print(f"A: {result['data']['answer']}\n")
    print("\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Gemini Content API - Example Usage")
    print("=" * 60)
    print("\n")
    
    try:
        example_1_generate_story()
        example_2_summarize_article()
        example_3_translate_multiple()
        example_4_explain_complex_code()
        example_5_qa_with_context()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")