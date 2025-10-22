from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load KYC data
kyc_df = pd.read_csv('../datasets/synthetic_customers_kyc.csv')

class PhoneRequest(BaseModel):
    phone: str

class KYCResponse(BaseModel):
    customer_id: int
    name: str
    phone: str
    address: str
    id_proof: str
    status: str
@app.get("/")
def read_root():
    return {"message": "Hello"}
@app.post("/kyc/fetch", response_model=KYCResponse)
def fetch_kyc_data(request: PhoneRequest):
    # Search for customer by phone number
    customer = kyc_df[kyc_df['Phone'] == request.phone]
    
    if customer.empty:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get the first matching record
    row = customer.iloc[0]
    
    return KYCResponse(
        customer_id=int(row['CustomerID']),
        name=row['Name'],
        phone=row['Phone'],
        address=row['Address'],
        id_proof=row['ID Proof'],
        status=row['Status']
    )