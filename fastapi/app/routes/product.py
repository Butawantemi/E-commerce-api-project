from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix = "/products",
    tags=['Products']
)


@router.get("/")
def get_product(db : Session = Depends(get_db), response_model=List[schemas.Product]):
    product = db.query(models.Post).all()
    return product

@router.product("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create_product(product : schemas.PostCreate, db : Session = Depends(get_db),):
    
    new_product = models.Post(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

@router.get("/{id}")
def get_product(id: int, response: Response, db : Session = Depends(get_db), response_model=schemas.Product):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"product with id: {id} was not found")
    return product





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db : Session = Depends(get_db), response_model=schemas.Product):
    product = db.query(models.Product).filter(models.Product.id == id)
    
    if product.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"product with id: {id} was not found") 
    product.delete(synchronize_session=False)
    db.commit()
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_product(id: int, product: schemas.ProductCreate, db : Session = Depends(get_db), response_model=schemas.Product):
    
    product_query = db.query(models.Product).filter(models.Product.id == id)
    
    older_product = product_query.first()
    
    if older_product == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"product with id: {id} was not found")
    product_query.update(product.dict(), synchronize_session=False)
    
    db.commit()
    
    return product_query.first()
