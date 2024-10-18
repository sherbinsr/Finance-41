from sqlalchemy.orm import Session
from . import models, schemas

def get_articles(db: Session):
    return db.query(models.Article).all()

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(title=article.title, content=article.content)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article