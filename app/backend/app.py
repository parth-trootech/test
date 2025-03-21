import uuid

from PIL import Image
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from app.backend.schemas import UserCreate, UserLogin

# Database configuration
DATABASE_URL = "postgresql://parth:1234@localhost/users"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define models (imported from db.models.py)
from app.db.models import User, ImageUpload, PredictionResult

# Initialize FastAPI
app = FastAPI()


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Utility functions for password hashing and verification
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Endpoint to handle user signup
@app.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(User).filter(User.user_email == user.user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving
    hashed_password = hash_password(user.user_password)

    # Create the user
    new_user = User(user_email=user.user_email, user_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# Endpoint to handle user login
@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if the user exists in the database
    db_user = db.query(User).filter(User.user_email == user.user_email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Verify the password
    if not verify_password(user.user_password, db_user.user_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": db_user.user_id, "user_email": db_user.user_email}


# Endpoint for image upload
@app.post("/upload_image")
async def upload_image(user_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the image to the server
    file_location = f"uploads/{uuid.uuid4().hex}_{image.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await image.read())

    # Save the image upload record in the database
    image_upload = ImageUpload(
        user_id=user_id,
        image_path=file_location
    )
    db.add(image_upload)
    db.commit()
    db.refresh(image_upload)

    return {"message": "Image uploaded successfully", "image_id": image_upload.image_id}


# Endpoint for making a prediction
@app.post("/predict")
async def predict(image_id: int, db: Session = Depends(get_db)):
    # Get the image from the database
    image_upload = db.query(ImageUpload).filter(ImageUpload.image_id == image_id).first()
    if not image_upload:
        raise HTTPException(status_code=404, detail="Image not found")

    # Load the image
    image_path = image_upload.image_path
    image = Image.open(image_path).convert("RGB")

    # Initialize the OCR model
    processor = TrOCRProcessor.from_pretrained('/home/trootech/PycharmProjects/trocr-small-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('/home/trootech/PycharmProjects/trocr-small-handwritten')
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    # Generate prediction
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # Save the prediction result in the database
    prediction_result = PredictionResult(
        image_id=image_id,
        predicted_digit=int(generated_text),  # Assuming the result is a digit
        confidence_score=None  # Set confidence_score to None by default
    )
    db.add(prediction_result)
    db.commit()
    db.refresh(prediction_result)

    return {"predicted_digit": generated_text, "prediction_id": prediction_result.prediction_id}
