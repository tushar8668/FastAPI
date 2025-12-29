from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def hello():
    return {"Message":"Hello, Welcome to the Application."}

@app.get("/about")
def about():
    return {"Message":"I am Tushar sutar. Building an API to use this in production ready application."}