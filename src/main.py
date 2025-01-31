from fastapi import FastAPI

app = FastAPI()

@app.get("/api/")
def test() -> str:
    return "it works"