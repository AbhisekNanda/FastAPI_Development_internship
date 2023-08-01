from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import SessionLocal,engine
import models
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import jwt
import requests
import uuid

app=FastAPI() 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

class signup(BaseModel):
    Firstname : str
    email : str
    password :str

@app.post("/signup")
def get_token(signup:signup,db:Session = Depends(get_db)):
    
    check_email = db .query(models.User).filter(models.User.email == signup.email).all()
    if check_email:
        return {"status":"User already exist"}
    else:
        max_id =db .query(models.User).count()
        id=max_id+1
        db_user = models.User(id=id,Fullname=signup.Firstname ,email=signup.email,password=signup.password)
        db.add(db_user)
        db.commit()
        return {"status":"User is created"}


@app.post("/login")
def get_token(form_data : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    user = db .query(models.User).filter(models.User.email == form_data.username).all()
    if user:
        if user[0].password == form_data.password:

            my_secret = 'my_login_xyz'
            payload_data  = {"id":int(user[0].id)}
        
            token = jwt.encode(
            payload=payload_data,
            key=my_secret
            )
            
            return token
        else:
            return {"status":"Invalid username or password"}
    else:
        
        return {"status":"User not exist"}

@app.get("/uploaddata")
def upload_data(token: Annotated[str, Depends(oauth2_scheme)],db:Session = Depends(get_db)):

    import requests

    url = "https://airdna1.p.rapidapi.com/properties"

    querystring = {"location":"santa monica","currency":"native"}

    headers = {
        "X-RapidAPI-Key": "22e7513f64msh41a4dbea2a1a24ep1e8844jsn1989fb4183fc",
        "X-RapidAPI-Host": "airdna1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    
    count=db .query(models.User).count()
    for i in data['properties']:
        count=count+1
        db_rooms = models.Rooms(
            id=count,
            room_id = i["id"],
            title = i["title"],
            long = i["longitude"],
            lat = i["latitude"],
            rating = i["rating"],
            revenue = i["revenue"],
            room_type = i["room_type"],
            review = i["reviews"],
            bedroom = i["bedrooms"],
            bathroom = i["bathrooms"],
            days_available = i["days_available"],
            property_type = i["property_type"],
        )

        db.add(db_rooms)
        db.commit()

        count=count+1
        print(count)
    

    return {"status":"Data uploaded to database"}

@app.get("/getdata")
def getdata(token: Annotated[str, Depends(oauth2_scheme)],db:Session = Depends(get_db)):
    db_rooms = db.query(models.Rooms).all()
    return {"data":jsonable_encoder(db_rooms)}