from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI="mongodb+srv://ravi:bunny@cluster0.m6iwsdt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster00"



client = AsyncIOMotorClient(MONGO_URI)
database = client["app_db"]  # Ensures we are using the 'app_db' database
applications_collection = database["applications"]  # Access the 'applications' collection
