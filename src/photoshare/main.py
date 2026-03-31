import uvicorn
from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=settings.run.port,
        host=settings.run.host,
        reload=True,
    )
