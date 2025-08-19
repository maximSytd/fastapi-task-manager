from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist, IntegrityError

from db.models import User
import schemas
from services.auth import create_access_token, verify_password, get_password_hash
from app.dependencies import get_current_user

user_router = APIRouter()

@user_router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await User.get(username=form_data.username)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    try:
        new_user = await User.create(
            username=user.username,
            password_hash=hashed_password
        )
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@user_router.get("/me", response_model=schemas.UserProfile, tags=["user"])
async def get_profile(current_user: User = Depends(get_current_user)):
    await current_user.fetch_related("grade__specialty", "performance_reviews")

    specialty = None
    grade_info = None
    next_review_date = None

    if current_user.grade:
        specialty = {"title": current_user.grade.specialty.title}
        grade_info = {
            "title": current_user.grade.title,
            "salary": current_user.grade.salary,
        }

    if current_user.performance_reviews:
        latest_review = max(
            current_user.performance_reviews,
            key=lambda r: r.date_held,
        )
        next_review_date = latest_review.date_held

    return schemas.UserProfile(
        username=current_user.username,
        specialty=specialty,
        grade=grade_info,
        next_performance_review=next_review_date,
    )