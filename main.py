from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, Usuario

# Rodar o código
# python -m uvicorn main:app --reload

app = FastAPI(title="Sistema de login")

templates = Jinja2Templates(directory="templates")

#Sistema com SSR - (GET - POST)
#Rota de cadastro
@app.get("/cadastro")
def tela_cadastro(request:Request):
    return templates.TemplateResponse(
        request,
        "cadastro.html",
        {"request": request}
    )

@app.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request}
    )

# Rota para criar um usuario - cadastrar usuario
# Rota (post)

@app.post("/cadastro")
def cadastrar_usuario(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
    ):
        user_existente = db.query(Usuario).filter_by(email=email).first()
        
        if user_existente:
            return templates.TemplateResponse(
                request,
                "cadastro.html",
                {"request": request, "erro": "Email já cadastrado!"}
            )

        novo_usuario = Usuario(email=email, senha=senha)
        db.add(novo_usuario)
        db.commit()
        return RedirectResponse(url="/login", status_code=303)

#Rota login - post

@app.post("/login")
def fazer_login(
     request: Request,
     email: str = Form(...),
     senha: str = Form(...),
     db: Session = Depends(get_db)
):
    #Validar email e senha
    user_existente = db.query(Usuario).filter(Usuario.email==email).filter(Usuario.senha==senha).first()

    if user_existente is None:
         return templates.TemplateResponse(
                request,
                "login.html",
                {"request": request, "erro": "Email ou senha inválidos!"}
            )
    response = RedirectResponse(url="/home", status_code=303)

    #Criando cookie simples (manter o login do usuário ativo)
    response.set_cookie(
         key="usuario_id",
         value= str(user_existente.id)
    )
    return response

# rota protegida 
@app.get("/home")
def tela_inicial(
    request: Request,
    db: Session = Depends(get_db)
):
    usuario_id = request.cookies.get("usuario_id")

    if usuario_id is None:
        return RedirectResponse(url="/login", status_code=303)
    usuario = db.query(Usuario).get(int(usuario_id))
    return templates.TemplateResponse(
        request,
        "home.html",
        {"request": request, "usuario": usuario}
    )