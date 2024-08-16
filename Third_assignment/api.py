from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
import crud
import database
import schema
import socket
import platform
import os

app = FastAPI()

# 데이터베이스 초기화
models.Base.metadata.create_all(bind=database.engine)

# Jinja2 템플릿 및 정적 파일 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/users/")
def create_user(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.post("/access/")
def handle_access(request: schema.AccessRequest, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=request.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.user_id == "allowed_user_id":
        crud.create_access(db, access_id=request.access_id, user_id=request.user_id, channel_id=request.channel_id)
        return {"message": "Access granted. Welcome!"}
    else:
        return {"message": "Access denied"}

@app.get("/ioc/")
async def get_ioc_data(query_item: str, query_type: str, db: Session = Depends(database.get_db)):
    vt_result = virustotal(query_item, query_type)
    otx_result = otx(query_item, query_type)
    
    return JSONResponse(
        content={
            "virustotal_result": vt_result,
            "otx_result": otx_result
        },
        status_code=200,
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(database.get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/ioc/log/create")
async def create_ioc_log(data: schema.IoC_Data, db: Session = Depends(database.get_db)):
    crud.write_ioc(db, data)
    return JSONResponse(content={"message": "IoC log written to database", "status_code": 200})
