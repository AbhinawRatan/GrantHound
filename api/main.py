from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from grant_recommendation import recommend_grants, read_grants_from_csv

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

grant_data = read_grants_from_csv("grants.csv")

class UserInput(BaseModel):
    description: str
    top_n: int = 5
    
API_KEY = "samridh"

async def api_key_dependency(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/recommend_grants")
async def get_recommended_grants(user_input: UserInput, api_key: str = Depends(api_key_dependency)):
    recommended_grants, recommended_grants_scores = recommend_grants(
        user_input.description, grant_data, user_input.top_n
    )

    response = []
    for grant, score in zip(recommended_grants, recommended_grants_scores):
        response.append(
            {
                "grant_name": grant["grant_name"],
                "score": score,
                "description": grant["description"],
                "foundation_name": grant["foundation_name"],
                "details_link": grant["details_link"],
                "grant_prize": grant["grant_prize"],
                "tags": grant["tags"],
                
            }
        )
    return response

__name__ = "api"
