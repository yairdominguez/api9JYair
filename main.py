from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from uuid import uuid4  # Para generar IDs únicos

# Creamos la app
app = FastAPI()

# Directorio donde están las vistas HTML
vistas = Jinja2Templates(directory="vistas")

# Modelo de datos: cómo se ve una publicación
class Post(BaseModel):
    id: str
    title: str
    body: str

# Lista que guardará todas las publicaciones (en memoria)
posts = []

#Página principal que muestra todo
@app.get("/", response_class=HTMLResponse)
def mostrar_todo(request: Request):
    return vistas.TemplateResponse("index.html", {"request": request, "posts": posts})

#Agregar una nueva publicación
@app.post("/create")
def agregar_post(title: str = Form(...), body: str = Form(...)):
    nuevo_post = Post(id=str(uuid4()), title=title, body=body)
    posts.append(nuevo_post)
    return RedirectResponse("/", status_code=303)

#Actualizar una publicación
@app.post("/update/{post_id}")
def actualizar_post(post_id: str, title: str = Form(...), body: str = Form(...)):
    for post in posts:
        if post.id == post_id:
            post.title = title
            post.body = body
            break
    return RedirectResponse("/?updated=true", status_code=303)

#Eliminar una publicación
@app.get("/delete/{post_id}")
def eliminar_post(post_id: str):
    global posts
    posts = [post for post in posts if post.id != post_id]
    return RedirectResponse("/?deleted=true", status_code=303)

#Ver una publicación específica (JSON)
@app.get("/libros/{post_id}")
def ver_post(post_id: str):
    for post in posts:
        if post.id == post_id:
            return {"data": post}
    return {"error": "No encontrado"}