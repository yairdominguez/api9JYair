from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Message" : "Hola, Mundo"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {"data" : id}