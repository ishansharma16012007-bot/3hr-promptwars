import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from dotenv import load_dotenv

load_dotenv()

from system_prompts import (
    StudentInput,
    GenerationResponse,
    ElaborationInput,
    ElaborationResponse
)
from generator import generate_ideas, elaborate_idea
from candidate_db import CANDIDATE_IDEAS

app = FastAPI(
    title="Antigravity — AI Project Idea Generator & Mentor",
    description="AI Mentor for final-year engineering and computer science students building capstone projects.",
    version="1.0.0"
)

# Enable CORS for Vercel & local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Antigravity AI Mentor API active. Static frontend file missing.</h1>")

@app.get("/ppt", response_class=HTMLResponse)
async def get_ppt_viewer():
    ppt_path = os.path.join(os.path.dirname(__file__), "static", "ppt.html")
    if os.path.exists(ppt_path):
        with open(ppt_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>PPT Viewer missing.</h1>")

@app.get("/api/download-ppt")
async def download_ppt():
    pptx_path = os.path.join(os.path.dirname(__file__), "antigravity_presentation.pptx")
    if not os.path.exists(pptx_path):
        # Regenerate PPTX if not present
        from generate_ppt import create_presentation
        create_presentation()
    return FileResponse(
        path=pptx_path,
        filename="antigravity_3d_presentation_deck.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

@app.get("/health")
async def health_check():
    has_api_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "healthy",
        "app": "Antigravity AI Project Mentor",
        "ai_engine": "Gemini 2.5 Flash" if has_api_key else "Smart Fallback Matrix Engine",
        "candidate_ideas_count": len(CANDIDATE_IDEAS),
        "ppt_available": os.path.exists(os.path.join(os.path.dirname(__file__), "antigravity_presentation.pptx"))
    }

@app.get("/api/candidate-ideas")
async def get_candidate_ideas():
    """Returns the 8 pre-curated reference domain project ideas."""
    return {"candidate_ideas": CANDIDATE_IDEAS}

@app.post("/api/generate", response_model=GenerationResponse)
async def api_generate_ideas(student_input: StudentInput):
    """
    Generates 3 tailored project ideas enforcing all 9 schema requirements & constraints.
    """
    try:
        return generate_ideas(student_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/elaborate", response_model=ElaborationResponse)
async def api_elaborate_idea(elaboration_input: ElaborationInput):
    """
    Generates Section 4 Elaboration details for a chosen project idea.
    """
    try:
        return elaborate_idea(elaboration_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
