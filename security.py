from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from utils import GetID

API_KEY_SCHEME = APIKeyHeader(name="ID_FOR_VERIFICATION")

async def Verify_ID(inputedID : Annotated[str, Depends(API_KEY_SCHEME)]):
    currID = GetID()

    if inputedID != currID:
        raise HTTPException(status_code=401, detail="Incorrect ID. Please try again.")
    
    return inputedID

