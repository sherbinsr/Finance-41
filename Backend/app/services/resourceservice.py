from spacy import schemas
from sqlalchemy.orm import Session
from app.dto import schemas
from app.entity import models


def get_all_resources(db: Session):
    return db.query(models.EducationalResource).all()

def create_resource(db: Session, resource: schemas.EducationalResourceCreate):
    db_resource = models.EducationalResource(title=resource.title, content=resource.content, video_url=resource.video_url, created_at=resource.created_at)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource