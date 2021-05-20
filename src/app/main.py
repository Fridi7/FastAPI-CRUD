from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"home": "Home page"}


@app.post("/languages/", response_model=schemas.Language, status_code=201)
def create_language(language: schemas.LanguageCreate, db: Session = Depends(get_db)):
    return crud.create_language(db=db, language=language)


@app.get("/languages/", response_model=List[schemas.Language])
def read_languages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    languages = crud.get_languages(db, skip=skip, limit=limit)
    return languages


@app.get("/languages/{language_id}", response_model=schemas.Language)
def read_language(language_id: int, db: Session = Depends(get_db)):
    db_language = crud.get_language(db, language_id=language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language


@app.put("/languages/{language_id}", response_model=schemas.Language)
def update_language(language_id: int, language_updates: schemas.LanguageBase, db: Session = Depends(get_db)):
    db_language = crud.get_language(db, language_id=language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    crud.update_language(db, db_language=db_language, language_updates=language_updates)
    return db_language


@app.delete("/language/{language_id}")
def delete_language(language_id: int, db: Session = Depends(get_db)):
    db_language = crud.get_language(db, language_id=language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    crud.delete_language(db, db_language=db_language)
    return {"message": "Language has been deleted successfully"}
