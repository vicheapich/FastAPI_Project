from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from .. import models, schemas

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(db: Session, request: schemas.Blog , user_id:int):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id:int, db:Session):
    blog= db.query(models.Blog).filter(models.Blog.id ==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"

def update(id:int, request:schemas.Blog, db:Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blogs.update({'title':request.title, 'body':request.body})
    db.commit()
    return "updated"

def show(id:int, db:Session):
    blog_id = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id {id} is not available')
    return blog_id