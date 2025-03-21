from datetime import datetime
from typing import List, Optional

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Relationship


# Users Table
class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(default=None, primary_key=True)
    user_email: str = Field(index=True, unique=True, nullable=False)
    user_password: str = Field(nullable=False)

    # Relationship
    image_uploads: List["ImageUpload"] = Relationship(back_populates="user")


# Image_Uploads Table
class ImageUpload(SQLModel, table=True):
    __tablename__ = "image_uploads"

    image_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    image_path: str = Field(nullable=False)
    upload_time: datetime = Field(default=datetime.utcnow, nullable=False)

    # Relationship
    user: User = Relationship(back_populates="image_uploads")
    predictions: List["PredictionResult"] = Relationship(back_populates="image_upload")


# Prediction_Results Table
class PredictionResult(SQLModel, table=True):
    __tablename__ = "prediction_results"

    prediction_id: int = Field(default=None, primary_key=True)
    image_id: int = Field(foreign_key="image_uploads.image_id")
    predicted_digit: int = Field(nullable=False)
    confidence_score: Optional[float] = Field(default=None, nullable=True)  # Make confidence_score optional
    prediction_time: datetime = Field(default=datetime.utcnow, nullable=False)

    # Relationship
    image_upload: ImageUpload = Relationship(back_populates="predictions")


DATABASE_URL = "postgresql://parth:1234@localhost/users"
# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the table if it doesn't exist
SQLModel.metadata.create_all(engine)
