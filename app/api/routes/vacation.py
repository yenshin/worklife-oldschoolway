from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    Response,
    status    
)

from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()
