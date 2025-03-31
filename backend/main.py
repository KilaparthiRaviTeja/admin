from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ MongoDB Connection
client = MongoClient("mongodb+srv://ravi:bunny@cluster0.m6iwsdt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["app_db"]
collection = db["applications"]  # ✅ Ensure this matches your database collection

# ✅ Fetch All Applications (For Admin)
@app.get("/admin/applications/")
async def get_applications():
    try:
        apps = list(collection.find({}, {"_id": 1, "first_name": 1, "last_name": 1, "status": 1, "approval_eta": 1, "approval_date": 1}))
        for app in apps:
            app["_id"] = str(app["_id"])  # Convert ObjectId to string
        return apps
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Update Application Status (Approve/Reject)
@app.put("/admin/applications/{app_id}")
async def update_application(app_id: str, status: str):
    try:
        if status not in ["Approved", "Rejected"]:
            raise HTTPException(status_code=400, detail="Invalid status")

        update_data = {"status": status}

        if status == "Approved":
            approval_eta = 3  # Example: Approval takes 3 days
            approval_date = datetime.utcnow().strftime("%Y-%m-%d")
            update_data.update({"approval_eta": approval_eta, "approval_date": approval_date, "approval_estimated_date": None})

        elif status == "Rejected":
            update_data.update({"approval_eta": 0, "approval_date": None, "approval_estimated_date": None, "rejection_date": datetime.utcnow().strftime("%Y-%m-%d")})

        result = collection.update_one({"_id": ObjectId(app_id)}, {"$set": update_data})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Application not found")

        return {"status": "Application updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
