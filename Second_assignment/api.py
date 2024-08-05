from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
import crud
import database
import schema

app = FastAPI()

# 데이터베이스 모델 생성
models.Base.metadata.create_all(bind=database.engine)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# Static files 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 사용자 생성
@app.post("/users/")
def create_user(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user_id=user.user_id)

# 접근 요청 처리
@app.post("/access/")
def handle_access(request: schema.AccessRequest, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=request.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 접근 허용 또는 거부 로직
    if request.user_id == "allowed_user_id":  # 여기에 허용할 사용자 ID를 설정
        crud.create_access(db, access_id=request.access_id, user_id=request.user_id, channel_id=request.channel_id)
        return {"message": "Access granted. Welcome!"}
    else:
        return {"message": "Access denied"}

# IOC 조회하여 JSON 결과 반환
@app.get("/ioc/")
def get_ioc():
    ioc_data = {
        "indicators": [
            {"type": "domain", "value": "example.com"},
            {"type": "ip", "value": "192.168.1.1"},
        ]
    }
    return ioc_data

# 기본 경로
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(database.get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
