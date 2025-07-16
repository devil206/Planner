from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import db
from bson.objectid import ObjectId
from passlib.context import CryptContext

user_router = APIRouter(
    tags=["User"],
)

users_collection = db["users"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")



@user_router.post("/signup")
async def sign_user_up(user: User):
    existing_user = users_collection.find_one({"email":user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )

    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password

    result = users_collection.insert_one(user_dict)
    return {"message": "User created", "user_id": str(result.inserted_id)}





@user_router.post("/signin")
def sign_user_in(user: UserSignIn):
    existing_user = users_collection.find_one({"email":user.email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401,detail = "Incorrect Password")
    
    return {
        "message": "User signed in successfully",
        "user_id": str(existing_user['_id'])
    }