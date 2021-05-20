from sqlalchemy.orm import Session

from app.api import models, schemas


def get_language(db: Session, language_id: int):
    return db.query(models.Language).filter(models.Language.id == language_id).first()


def get_languages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Language).offset(skip).limit(limit).all()


def create_language(db: Session, language: schemas.LanguageCreate):
    db_language = models.Language(name=language.name, code=language.code)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def update_language(db: Session, db_language: schemas.Language, language_updates: schemas.LanguageBase):
    db_language.name = language_updates.name
    db_language.code = language_updates.code
    db.add(db_language)
    db.commit()
    return db.refresh(db_language)


def delete_language(db: Session, db_language: schemas.Language):
    db.delete(db_language)
    return db.commit()
