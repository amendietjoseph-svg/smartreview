"""
Router for account operations
CRUD endpoints for managing trading accounts
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Account
from schemas import AccountCreate, AccountUpdate, Account as AccountSchema

router = APIRouter()


@router.post("", include_in_schema=True)
@router.post("/", response_model=AccountSchema)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """
    Create a new trading account
    Supports both personal accounts and prop firm challenges
    """
    db_account = Account(**account.dict())
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return db_account


@router.get("", include_in_schema=True)
@router.get("/", response_model=List[AccountSchema])
def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all accounts
    """
    accounts = db.query(Account).offset(skip).limit(limit).all()
    return accounts


@router.get("/active", response_model=List[AccountSchema])
def get_active_accounts(db: Session = Depends(get_db)):
    """
    Get only active accounts
    """
    accounts = db.query(Account).filter(Account.is_active == True).all()
    return accounts


@router.get("/{account_id}", response_model=AccountSchema)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """
    Get a specific account by ID
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return account


@router.put("/{account_id}", response_model=AccountSchema)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing account
    """
    db_account = db.query(Account).filter(Account.id == account_id).first()
    
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update fields
    update_data = account_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    db.commit()
    db.refresh(db_account)
    
    return db_account


@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """
    Delete an account
    This will also delete all associated trades
    """
    db_account = db.query(Account).filter(Account.id == account_id).first()
    
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(db_account)
    db.commit()
    
    return {"message": "Account deleted successfully"}
