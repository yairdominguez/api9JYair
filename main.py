from fastapi import FastAPI

app = FastAPI()

def index():
    return "Api en ejecución"