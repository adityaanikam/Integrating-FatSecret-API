from fastapi import FastAPI, HTTPException
import httpx
from datetime import datetime, timedelta
import base64
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_BASE_URL = "https://platform.fatsecret.com/rest/server.api"

token_data = {
    "access_token": None,
    "expires_at": None
}


async def get_access_token():
    try:
        now = datetime.now()

        if token_data["access_token"] and token_data["expires_at"] and token_data["expires_at"] > now:
            return token_data["access_token"]

        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "basic"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:  # Added timeout
            print("Attempting to get token...")  # Debug log
            response = await client.post(TOKEN_URL, headers=headers, data=data)
            print(f"Token response status: {response.status_code}")  # Debug log
            print(f"Token response: {response.text}")  # Debug log

            response.raise_for_status()
            token_info = response.json()
            token_data["access_token"] = token_info["access_token"]
            token_data["expires_at"] = now + timedelta(seconds=token_info["expires_in"] - 300)
            return token_data["access_token"]
    except Exception as e:
        print(f"Detailed token error: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Failed to get access token: {str(e)}")


@app.get("/test-connection")
async def test_connection():
    """Test if we can make basic HTTP requests"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://httpbin.org/ip")
            return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/")
async def root():
    return {
        "message": "FatSecret API Integration is running",
        "client_id_present": bool(CLIENT_ID),
        "client_secret_present": bool(CLIENT_SECRET)
    }


@app.get("/search_food/{query}")
async def search_food(query: str):
    try:
        access_token = await get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        params = {
            "method": "foods.search",
            "search_expression": query,
            "format": "json"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                API_BASE_URL,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Search error: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")