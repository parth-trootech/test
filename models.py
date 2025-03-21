"""-- Table 7.2.1: Users
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL UNIQUE,
    user_password VARCHAR(32) NOT NULL
);

-- Table 7.2.2: Image_Uploads
CREATE TABLE Image_Uploads (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    image_path VARCHAR(255) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table 7.2.3: Prediction_Results
CREATE TABLE Prediction_Results (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT,
    predicted_digit INT NOT NULL,
    confidence_score FLOAT NOT NULL,
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (image_id) REFERENCES Image_Uploads(image_id)
);
"""

from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime


# Users Table
class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(default=None, primary_key=True, autoincrement=True)
    user_email: str = Field(index=True, unique=True, nullable=False)
    user_password: str = Field(nullable=False)

    # Relationship
    image_uploads: List["ImageUpload"] = Relationship(back_populates="user")


# Image_Uploads Table
class ImageUpload(SQLModel, table=True):
    __tablename__ = "image_uploads"

    image_id: int = Field(default=None, primary_key=True, autoincrement=True)
    user_id: int = Field(foreign_key="users.user_id")
    image_path: str = Field(nullable=False)
    upload_time: datetime = Field(default=datetime.utcnow, nullable=False)

    # Relationship
    user: User = Relationship(back_populates="image_uploads")
    predictions: List["PredictionResult"] = Relationship(back_populates="image_upload")


# Prediction_Results Table
class PredictionResult(SQLModel, table=True):
    __tablename__ = "prediction_results"

    prediction_id: int = Field(default=None, primary_key=True, autoincrement=True)
    image_id: int = Field(foreign_key="image_uploads.image_id")
    predicted_digit: int = Field(nullable=False)
    confidence_score: float = Field(nullable=False)
    prediction_time: datetime = Field(default=datetime.utcnow, nullable=False)

    # Relationship
    image_upload: ImageUpload = Relationship(back_populates="predictions")
