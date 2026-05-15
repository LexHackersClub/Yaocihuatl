from fastapi import FastAPI


app = FastAPI(
    title="Yaocihuatl Backend",
    description="Scaffolding API service",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "backend", "module": "api"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
