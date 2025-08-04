from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import database.models
from database.models import Entry,Profile,Issues
from database.session import db_dependency, get_db
from database.session import engine
from sqlalchemy.orm import Session
from database.schema import EntryBase, ProfileBase, IssuesBase, TokenRequest
from math import radians, cos, sin, asin, sqrt
from uuid import UUID
from firebase_admin_setup import *
from firebase_admin import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

database.models.Base.metadata.create_all(bind = engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/google")
def google_login(data: TokenRequest, db: Session = Depends(get_db)):
    try:
        decoded_token = auth.verify_id_token(data.id_token)
        email = decoded_token.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        user = db.query(Entry).filter(Entry.email == email).first()

        if not user:
            user = Entry(email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

        return {
            "message": "Login successful",
            "uuid": str(user.uuid),
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")


@app.post("/createProfile")
async def createProfile(profile: ProfileBase, db: db_dependency):
    
    try:
        newProfile = Profile(
            name = profile.name,
            uuid = profile.uuid,
            email = profile.email,
            pno = profile.pno,
            address = profile.address
        )
        
        db.add(newProfile)
        db.commit()
        db.refresh(newProfile)
        
        return {
            "status": "success",
            "data" : newProfile
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/getProfile")
async def getProfile(id: UUID, db: db_dependency):
    
    try:
        profile = db.query(Profile).filter(Profile.uuid == id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {
            "status": "success",
            "data" : profile
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@app.post("/createIssue")
async def createIssue(issue: IssuesBase, db: db_dependency):
    
    try:
        newIssue = Issues(
            uuid = issue.uuid,
            name = issue.name,
            image = issue.image,
            lat = issue.lat,
            long = issue.long,
            description = issue.description,
            status = issue.status
        )
        
        db.add(newIssue)
        db.commit()
        db.refresh(newIssue)
        
        return {
            "status": "success",
            "data" : newIssue
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

@app.get("/getIssues")
def getIssues(latitude:float, longtitude:float, db: db_dependency):
    try:
        user_lat = latitude
        user_lon = longtitude
    except ValueError:
        return JSONResponse({"error": "Invalid latitude/longitude"}, status=400)

    nearby = []
    for issue in db.query(Issues).all():
        try:
            comm_lat = float(issue.lat)
            comm_lon = float(issue.long)
            distance = haversine(user_lat, user_lon, comm_lat, comm_lon)
            if distance <= 10.0: 
                nearby.append(issue)
        except ValueError:
            continue

    return {
        "status": "success",
        "data": nearby
            }

@app.get("/")
async def index():
    return {"message": "Hello World"} 