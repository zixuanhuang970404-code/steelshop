from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4
from .services import extract_member_records, compare_members

app = FastAPI(title="SteelShop MVP", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
PROJECTS: dict[str, dict] = {}

class ProjectInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/projects")
def create_project(payload: ProjectInput):
    identifier = str(uuid4())
    project = {"id": identifier, "name": payload.name}
    PROJECTS[identifier] = project
    return project

@app.get("/api/v1/projects")
def list_projects():
    return list(PROJECTS.values())

@app.post("/api/v1/compare")
async def compare(design: UploadFile = File(...), shop: UploadFile = File(...)):
    for item in (design, shop):
        if not item.filename or not item.filename.lower().endswith(".pdf"):
            raise HTTPException(400, "Both inputs must be PDF files")
    design_bytes, shop_bytes = await design.read(), await shop.read()
    max_bytes = 30 * 1024 * 1024
    if any(len(data) > max_bytes for data in (design_bytes, shop_bytes)):
        raise HTTPException(413, "Maximum PDF upload size is 30 MB per file")
    try:
        design_records = extract_member_records(design_bytes)
        shop_records = extract_member_records(shop_bytes)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(422, str(exc)) from exc
    return {"design_members": design_records, "shop_members": shop_records,
            "issues": compare_members(design_records, shop_records)}
