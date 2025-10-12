from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import google.generativeai as genai
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(
    title="Smart Content Generator API",
    description="AI-powered content generation using Google Gemini",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class TextRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000, description="Input text prompt")
    max_tokens: Optional[int] = Field(1000, ge=100, le=8000, description="Maximum tokens in response")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Creativity level (0-2)")

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to summarize")
    length: Optional[str] = Field("medium", description="Summary length: short, medium, long")

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    target_language: str = Field(..., description="Target language (e.g., Spanish, French, Hindi)")

class CodeExplainRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Code snippet to explain")
    language: Optional[str] = Field("Python", description="Programming language")

class QARequest(BaseModel):
    question: str = Field(..., min_length=5, description="Question to answer")
    context: Optional[str] = Field(None, description="Additional context")

class APIResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None

# Dependency to get Gemini model
@lru_cache()
def get_gemini_model(model_name: str = "gemini-pro-latest"):
    return genai.GenerativeModel(model_name)

# Helper function to generate content
async def generate_content(prompt: str, temperature: float = 0.7) -> str:
    try:
        model = get_gemini_model()
        generation_config = {
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 40,
        }
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# Routes
@app.get("/", response_model=dict)
async def root():
    """API root endpoint"""
    return {
        "message": "Smart Content Generator API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "generate": "/api/generate",
            "summarize": "/api/summarize",
            "translate": "/api/translate",
            "explain-code": "/api/explain-code",
            "question-answer": "/api/qa"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint that also verifies Gemini API key configuration.
    """
    # Start with the basic health status
    response_data = {
        "status": "healthy", 
        "service": "running"
    }

    # Check if the Gemini API key is present in the environment
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    # Add the Gemini API status to the response dictionary
    if gemini_key:
        response_data["gemini_api"] = "configured"
    else:
        response_data["gemini_api"] = "not_configured"
    
    return response_data

@app.post("/api/generate", response_model=APIResponse)
async def generate_text(request: TextRequest):
    """
    Generate text based on a prompt
    
    Example:
    ```json
    {
        "prompt": "Write a short story about a robot learning to paint",
        "max_tokens": 500,
        "temperature": 0.8
    }
    ```
    """
    try:
        result = await generate_content(request.prompt, request.temperature)
        return APIResponse(
            success=True,
            data={"generated_text": result, "prompt": request.prompt},
            message="Text generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize", response_model=APIResponse)
async def summarize_text(request: SummarizeRequest):
    """
    Summarize long text
    
    Example:
    ```json
    {
        "text": "Your long article text here...",
        "length": "short"
    }
    ```
    """
    try:
        length_map = {
            "short": "in 2-3 sentences",
            "medium": "in 1 paragraph",
            "long": "in 2-3 paragraphs"
        }
        length_instruction = length_map.get(request.length, "in 1 paragraph")
        
        prompt = f"Summarize the following text {length_instruction}:\n\n{request.text}"
        result = await generate_content(prompt, temperature=0.3)
        
        return APIResponse(
            success=True,
            data={"summary": result, "original_length": len(request.text), "summary_length": len(result)},
            message="Text summarized successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate", response_model=APIResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text to another language
    
    Example:
    ```json
    {
        "text": "Hello, how are you?",
        "target_language": "Spanish"
    }
    ```
    """
    try:
        prompt = f"Translate the following text to {request.target_language}:\n\n{request.text}"
        result = await generate_content(prompt, temperature=0.3)
        
        return APIResponse(
            success=True,
            data={
                "original": request.text,
                "translated": result,
                "target_language": request.target_language
            },
            message="Translation successful"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/explain-code", response_model=APIResponse)
async def explain_code(request: CodeExplainRequest):
    """
    Explain code snippet in simple terms
    
    Example:
    ```json
    {
        "code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
        "language": "Python"
    }
    ```
    """
    try:
        prompt = f"""Explain the following {request.language} code in simple terms, including:
1. What it does
2. How it works
3. Key concepts used

Code:
```{request.language.lower()}
{request.code}
```"""
        
        result = await generate_content(prompt, temperature=0.5)
        
        return APIResponse(
            success=True,
            data={
                "code": request.code,
                "language": request.language,
                "explanation": result
            },
            message="Code explained successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/qa", response_model=APIResponse)
async def question_answer(request: QARequest):
    """
    Answer questions with optional context
    
    Example:
    ```json
    {
        "question": "What is machine learning?",
        "context": "Explain in the context of modern AI applications"
    }
    ```
    """
    try:
        if request.context:
            prompt = f"Context: {request.context}\n\nQuestion: {request.question}\n\nProvide a detailed answer:"
        else:
            prompt = f"Question: {request.question}\n\nProvide a detailed answer:"
        
        result = await generate_content(prompt, temperature=0.7)
        
        return APIResponse(
            success=True,
            data={
                "question": request.question,
                "answer": result,
                "context_provided": request.context is not None
            },
            message="Question answered successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get API usage statistics"""
    return {
        "endpoints": 5,
        "models_used": ["gemini-pro"],
        "features": [
            "Text Generation",
            "Summarization",
            "Translation",
            "Code Explanation",
            "Question Answering"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
