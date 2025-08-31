from fastapi import FastAPI, HTTPException
import asyncpg
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Using DATABASE_URL: {DATABASE_URL}")

@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()

@app.get("/pincode/health")
async def health_check():
    return {"status": "ok"} 

@app.get("/pincode/{pincode}")
async def get_pincode_details(pincode: int):
    async with app.state.db_pool.acquire() as connection:
        result = await connection.fetchrow(
            f"SELECT * FROM public.pincode WHERE pincode = '{pincode}'"
        )
        if result:
            return dict(result)
        else:
            raise HTTPException(status_code=404, detail="Pincode not found")
        
