from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router

app = FastAPI(title="FastAPI", description="FastAPI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYmNkIiwiaWF0IjoxNjkyNDIwMjA0LCJleHAiOjE2OTUwMTIyMDR9.3RKPELz0vpEGQL8maguGHhbA54R7ruJvF4FCk2T-CJI
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
