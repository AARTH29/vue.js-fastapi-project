
import databases,sqlalchemy
from fastapi import FastAPI
from sqlalchemy.sql.schema import ForeignKey
from pydantic import BaseModel,main,Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
origins = [
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# postgres database
DATABASE_URL = "postgresql://postgres:aarthi@127.0.0.1:5432/DB"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


doctor = sqlalchemy.Table(
    "doctor",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True,index=True),
    sqlalchemy.Column("name",sqlalchemy.String),
    sqlalchemy.Column("specification",sqlalchemy.String),
)

location = sqlalchemy.Table(
    "location",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,ForeignKey("doctor"),index=True),
    sqlalchemy.Column("place",sqlalchemy.String),
    sqlalchemy.Column("state",sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

# Models

class doctorlist(BaseModel):
    id : int
    name : str
    specification : str

class locationlist(BaseModel):
    id : int
    place : str
    state : str

class fulllist(BaseModel):
    name : str
    specification : str
    place : str
    state : str

class doctorEntry(BaseModel):
    id : int = Field(...,example="25")
    name : str = Field(...,example="Percy")
    specification : str = Field(...,example="ent")
    
class locationEntry(BaseModel):
    id : int = Field(...,example="23")
    place : str = Field(...,example="udaipur")
    state : str = Field(...,example="rajasthan")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/doctor",response_model=List[fulllist])
async def find_doctor(search:str=""):
    query = 'SELECT DOCTOR.name,DOCTOR.specification,LOCATION.place,LOCATION.state FROM DOCTOR JOIN LOCATION ON DOCTOR.id=LOCATION.id '\
    "WHERE DOCTOR.name LIKE '%"+search+"%' OR DOCTOR.specification LIKE '%"+search+"%' OR LOCATION.place LIKE '%"+search+"%' OR LOCATION.state LIKE '%"+search+"%' "
    var = await database.fetch_all(query)
    return var

@app.post("/doctor",response_model=doctorlist)
async def register_doctor(user:doctorEntry):

    query = doctor.insert().values(
        id = (user.id),
        name = (user.name),
        specification = (user.specification)
    )
    await database.execute(query)
    return {
        **user.dict()
    }

@app.post("/location",response_model=locationlist)
async def register_location(user:locationEntry):

    query = location.insert().values(
        id = (user.id),
        place = (user.place),
        state = (user.state)
    )
    await database.execute(query)
    return{
        **user.dict()
    }