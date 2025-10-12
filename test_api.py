import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.json()}")
    assert response.status_code == 200

def test_generate_text():
    """Test text generation"""
    payload = {
        "prompt": "Write a short poem about Python programming",
        "temperature": 0.8,
        "max_tokens": 200
    }
    response = requests.post(f"{BASE_URL}/api/generate", json=payload)
    result = response.json()
    print("\n=== Text Generation ===")
    print(f"Prompt: {payload['prompt']}")
    print(f"Response: {result['data']['generated_text']}")
    assert response.status_code == 200

def test_summarize():
    """Test summarization"""
    payload = {
        "text": """
        Artificial Intelligence (AI) is revolutionizing the world. 
        Machine learning, a subset of AI, enables computers to learn from data. 
        Deep learning uses neural networks with multiple layers. 
        Natural language processing helps computers understand human language.
        Computer vision allows machines to interpret visual information.
        AI applications include healthcare, finance, transportation, and more.
        """,
        "length": "short"
    }
    response = requests.post(f"{BASE_URL}/api/summarize", json=payload)
    result = response.json()
    print("\n=== Summarization ===")
    print(f"Summary: {result['data']['summary']}")
    assert response.status_code == 200

def test_translate():
    """Test translation"""
    payload = {
        "text": "Hello, how are you today?",
        "target_language": "Hindi"
    }
    response = requests.post(f"{BASE_URL}/api/translate", json=payload)
    result = response.json()
    print("\n=== Translation ===")
    print(f"Original: {result['data']['original']}")
    print(f"Translated: {result['data']['translated']}")
    assert response.status_code == 200

def test_explain_code():
    """Test code explanation"""
    payload = {
        "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        "language": "Python"
    }
    response = requests.post(f"{BASE_URL}/api/explain-code", json=payload)
    result = response.json()
    print("\n=== Code Explanation ===")
    print(f"Explanation: {result['data']['explanation']}")
    assert response.status_code == 200

def test_qa():
    """Test question answering"""
    payload = {
        "question": "What is FastAPI and why is it popular?",
        "context": "In the context of modern web development"
    }
    response = requests.post(f"{BASE_URL}/api/qa", json=payload)
    result = response.json()
    print("\n=== Question & Answer ===")
    print(f"Question: {result['data']['question']}")
    print(f"Answer: {result['data']['answer']}")
    assert response.status_code == 200

if __name__ == "__main__":
    print("Starting API Tests...\n")
    print("=" * 60)
    
    try:
        test_health()
        test_generate_text()
        test_summarize()
        test_translate()
        test_explain_code()
        test_qa()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
