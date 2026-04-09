```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import datetime

# Pydantic models for request and response
class InputPayload(BaseModel):
    """
    Represents the input structure for the processing endpoint.
    """
    input: str = Field(..., min_length=1, description="Text input to be processed.")

class OutputPayload(BaseModel):
    """
    Represents the output structure after processing the input.
    """
    original_input: str = Field(..., description="The original text input.")
    processed_output: str = Field(..., description="The processed text output.")
    timestamp: str = Field(..., description="Timestamp of when the processing occurred.")
    processor_info: str = Field("FastAPI String Processor v1.0", description="Information about the processor.")


app = FastAPI(
    title="FastAPI Serverless Processor",
    description="A simple FastAPI backend deployed on AWS Lambda that processes text input without a database.",
    version="1.0.0",
)

# Configure CORS middleware
# IMPORTANT: For production, replace "*" with your specific frontend domain(s)
# e.g., origins = ["https://yourfrontenddomain.com", "http://localhost:8080"]
origins = [
    "http://localhost:8000",  # For local frontend development
    "http://127.0.0.1:5500",  # Example for VS Code Live Server
    "*"  # Allows all origins, BE CAREFUL IN PRODUCTION!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    """
    Root endpoint providing a welcome message and instructions.
    """
    return {
        "message": "Welcome to the FastAPI Processor. Use the /run endpoint for processing.",
        "documentation": "/docs"
    }

@app.post("/run", response_model=OutputPayload)
async def run_processor(payload: InputPayload):
    """
    Processes the input text by reversing it and adding a timestamp.
    """
    try:
        if not payload.input.strip():
            raise HTTPException(status_code=400, detail="Input cannot be empty.")

        processed_text = payload.input[::-1]  # Simple processing: reverse the string
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

        return OutputPayload(
            original_input=payload.input,
            processed_output=f"Reversed: {processed_text}",
            timestamp=current_time
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# This is the entry point for AWS Lambda when using Mangum
# The Lambda handler should be set to 'main.handler'
from mangum import Mangum
handler = Mangum(app)

```

---

### **Frontend Code**