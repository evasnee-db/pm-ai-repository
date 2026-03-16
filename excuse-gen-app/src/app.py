import os
import json
import logging
import time
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Excuse Email Draft Tool",
    description="Generate creative excuse emails using Databricks Model Serving",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request details
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    # Log response details
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response

# Configuration
class Config:
    DATABRICKS_API_TOKEN = os.getenv("DATABRICKS_API_TOKEN", "")
    DATABRICKS_ENDPOINT_URL = os.getenv(
        "DATABRICKS_ENDPOINT_URL",
        "https://dbc-32cf6ae7-cf82.staging.cloud.databricks.com/serving-endpoints/databricks-gpt-oss-120b/invocations"
    )
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")

config = Config()

# Pydantic models
class ExcuseRequest(BaseModel):
    category: str
    tone: str
    seriousness: int
    recipient_name: str
    sender_name: str
    eta_when: str
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = [
            "Running Late", "Missed Meeting", "Deadline", 
            "WFH/OOO", "Social", "Travel"
        ]
        if v not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v
    
    @validator('tone')
    def validate_tone(cls, v):
        valid_tones = ["Sincere", "Playful", "Corporate"]
        if v not in valid_tones:
            raise ValueError(f"Tone must be one of: {', '.join(valid_tones)}")
        return v
    
    @validator('seriousness')
    def validate_seriousness(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("Seriousness must be between 1 and 5")
        return v

class ExcuseResponse(BaseModel):
    subject: str
    body: str
    success: bool
    error: Optional[str] = None

# LLM Integration
class LLMClient:
    def __init__(self, api_token: str, endpoint_url: str):
        self.api_token = api_token
        self.endpoint_url = endpoint_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _build_prompt(self, request: ExcuseRequest) -> str:
        """Build the prompt for the LLM based on the request parameters."""
        
        seriousness_map = {
            1: "very silly and humorous",
            2: "playful and lighthearted", 
            3: "balanced and reasonable",
            4: "professional and sincere",
            5: "serious and formal"
        }
        
        seriousness_desc = seriousness_map.get(request.seriousness, "balanced")
        
        prompt = f"""
You are an expert email writer. Generate an excuse email with the following parameters:

Category: {request.category}
Tone: {request.tone}
Seriousness Level: {request.seriousness}/5 ({seriousness_desc})
Recipient: {request.recipient_name}
Sender: {request.sender_name}
ETA/When: {request.eta_when}

Please generate a JSON response with exactly this structure:
{{
    "subject": "Brief email subject line",
    "body": "Complete email body with greeting, apology/excuse, reason, next step, and sign-off"
}}

Guidelines:
- Match the {request.tone.lower()} tone throughout
- Keep the {seriousness_desc} style appropriate for level {request.seriousness}
- Include a proper greeting using the recipient's name
- Provide a believable excuse related to {request.category.lower()}
- Include the timeframe: {request.eta_when}
- End with an appropriate sign-off using the sender's name
- Keep it concise but complete
"""
        
        return prompt.strip()
    
    async def generate_excuse(self, request: ExcuseRequest) -> ExcuseResponse:
        """Generate an excuse email using the Databricks Model Serving endpoint."""
        
        if not self.api_token:
            logger.warning("No API token provided, using fallback response")
            return self._get_fallback_response(request)
        
        prompt = self._build_prompt(request)
        
        # Databricks Model Serving API format
        payload = {
            "inputs": [prompt],
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 0.9
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"Making request to LLM endpoint: {self.endpoint_url}")
            
            response = await self.client.post(
                self.endpoint_url,
                json=payload,
                headers=headers
            )
            
            logger.info(f"LLM response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"LLM API error: {response.status_code} - {response.text}")
                return ExcuseResponse(
                    subject="",
                    body="",
                    success=False,
                    error=f"LLM API error: {response.status_code}"
                )
            
            # Parse response - handle both OpenAI and Databricks formats
            result = response.json()
            logger.info(f"Raw LLM response: {result}")
            
            # Extract text from various response formats
            text_content = self._extract_text_from_response(result)
            
            if not text_content:
                logger.error("No text content found in LLM response")
                return self._get_fallback_response(request)
            
            # Parse JSON from the response
            parsed_email = self._parse_email_response(text_content)
            
            if parsed_email:
                return ExcuseResponse(
                    subject=parsed_email["subject"],
                    body=parsed_email["body"],
                    success=True
                )
            else:
                logger.error("Failed to parse JSON from LLM response")
                return self._get_fallback_response(request)
                
        except Exception as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            return ExcuseResponse(
                subject="",
                body="",
                success=False,
                error=f"API call failed: {str(e)}"
            )
    
    def _extract_text_from_response(self, response: Dict[str, Any]) -> str:
        """Extract text content from various LLM response formats."""
        
        # Try different response formats
        if isinstance(response, dict):
            # OpenAI-style format
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
                elif "text" in choice:
                    return choice["text"]
            
            # Databricks-style format
            if "predictions" in response and len(response["predictions"]) > 0:
                prediction = response["predictions"][0]
                if isinstance(prediction, dict) and "generated_text" in prediction:
                    return prediction["generated_text"]
                elif isinstance(prediction, str):
                    return prediction
            
            # Direct text response
            if "text" in response:
                return response["text"]
            
            # Response as direct string array
            if isinstance(response, list) and len(response) > 0:
                return str(response[0])
        
        # If response is a string itself
        if isinstance(response, str):
            return response
        
        return ""
    
    def _parse_email_response(self, text: str) -> Optional[Dict[str, str]]:
        """Parse JSON email response from text, with fallback strategies."""
        
        try:
            # Try direct JSON parsing
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass
        
        try:
            # Try to extract JSON from markdown code blocks
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                if end != -1:
                    json_text = text[start:end].strip()
                    return json.loads(json_text)
            
            # Try to extract JSON from regular code blocks
            if "```" in text:
                start = text.find("```") + 3
                end = text.find("```", start)
                if end != -1:
                    json_text = text[start:end].strip()
                    return json.loads(json_text)
            
            # Try to find JSON-like structure in text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                json_text = text[start:end]
                return json.loads(json_text)
                
        except json.JSONDecodeError:
            pass
        
        return None
    
    def _get_fallback_response(self, request: ExcuseRequest) -> ExcuseResponse:
        """Generate a fallback response when LLM is unavailable."""
        
        fallback_subjects = {
            "Running Late": f"Running Late - ETA {request.eta_when}",
            "Missed Meeting": f"Apologies for Missing Our Meeting",
            "Deadline": f"Extension Request - {request.eta_when}",
            "WFH/OOO": f"Working from Home - {request.eta_when}",
            "Social": f"Can't Make It - {request.eta_when}",
            "Travel": f"Travel Delay - ETA {request.eta_when}"
        }
        
        fallback_bodies = {
            "Running Late": f"Dear {request.recipient_name},\n\nI wanted to let you know that I'm running late and will be there in {request.eta_when}. Thank you for your patience!\n\nBest regards,\n{request.sender_name}",
            "Missed Meeting": f"Dear {request.recipient_name},\n\nI sincerely apologize for missing our meeting. I'll reach out to reschedule at your earliest convenience.\n\nBest regards,\n{request.sender_name}",
            "Deadline": f"Dear {request.recipient_name},\n\nI need to request an extension until {request.eta_when} for the current deadline. Thank you for understanding.\n\nBest regards,\n{request.sender_name}",
            "WFH/OOO": f"Dear {request.recipient_name},\n\nI'll be working from home {request.eta_when}. I'll be available via email and phone as needed.\n\nBest regards,\n{request.sender_name}",
            "Social": f"Dear {request.recipient_name},\n\nI won't be able to make it {request.eta_when}. Sorry for any inconvenience!\n\nBest,\n{request.sender_name}",
            "Travel": f"Dear {request.recipient_name},\n\nMy travel has been delayed and I'll arrive {request.eta_when}. Thank you for your patience!\n\nBest regards,\n{request.sender_name}"
        }
        
        return ExcuseResponse(
            subject=fallback_subjects.get(request.category, f"Update from {request.sender_name}"),
            body=fallback_bodies.get(request.category, f"Dear {request.recipient_name},\n\nI wanted to update you regarding {request.category.lower()}. I'll be {request.eta_when}.\n\nBest regards,\n{request.sender_name}"),
            success=True
        )

# Initialize LLM client
llm_client = LLMClient(config.DATABRICKS_API_TOKEN, config.DATABRICKS_ENDPOINT_URL)

# API Routes
@app.post("/api/generate-excuse", response_model=ExcuseResponse)
async def generate_excuse(request: ExcuseRequest):
    """Generate an excuse email based on the provided parameters."""
    try:
        logger.info(f"Generating excuse for: {request.dict()}")
        result = await llm_client.generate_excuse(request)
        return result
    except Exception as e:
        logger.error(f"Error generating excuse: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoints
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/healthz") 
async def healthz():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# Metrics endpoint (Prometheus format)
@app.get("/metrics")
async def metrics():
    return {
        "http_requests_total": 0,
        "http_request_duration_seconds": 0.0,
        "app_info": {
            "version": "1.0.0",
            "name": "excuse-email-tool"
        }
    }

# Debug endpoint
@app.get("/debug")
async def debug():
    return {
        "environment": {
            "DATABRICKS_ENDPOINT_URL": config.DATABRICKS_ENDPOINT_URL,
            "DATABRICKS_API_TOKEN": "***" if config.DATABRICKS_API_TOKEN else "Not Set",
            "PORT": config.PORT,
            "HOST": config.HOST,
        },
        "working_directory": str(Path.cwd()),
        "python_path": os.environ.get("PYTHONPATH", "Not Set")
    }

# Serve React frontend
def get_frontend_file_path() -> Optional[Path]:
    """Find the frontend file across different possible locations."""
    possible_paths = [
        Path("public/index.html"),
        Path("../public/index.html"),
        Path("./public/index.html"),
        Path(__file__).parent.parent / "public" / "index.html",
    ]
    
    for path in possible_paths:
        if path.exists():
            logger.info(f"Found frontend file at: {path}")
            return path
    
    logger.error("Frontend file not found in any expected location")
    return None

@app.get("/")
async def serve_frontend():
    """Serve the React frontend."""
    frontend_path = get_frontend_file_path()
    if frontend_path:
        return FileResponse(frontend_path, media_type="text/html")
    else:
        return JSONResponse(
            status_code=404,
            content={"error": "Frontend not found. Please ensure public/index.html exists."}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)





