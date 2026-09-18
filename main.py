from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/posts")
def home():
    return "Hello juli :)"
