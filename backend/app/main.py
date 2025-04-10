from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from .api.v1.orgs import router as orgs_router
from .api.v1.inventory import router as inventory_router
app = FastAPI(title="Inventory Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orgs_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "Backend working 🚀"}