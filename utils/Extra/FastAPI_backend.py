from fastapi import FastAPI, Form
from grant_recommendation import read_grants_from_csv, recommend_grants

print("read_grants_from_csv():", read_grants_from_csv("backend/grants.csv"))
print("recommend_grants():", recommend_grants("test", [], 5))

app = FastAPI()
grant_data = read_grants_from_csv("backend/grants.csv")


@app.post("/get_recommendations")
async def get_recommendations(user_description: str):
    print(f"user_description: {user_description}")
    top_n = 5
    recommended_grants, recommended_grants_scores = recommend_grants(
        user_description, grant_data, top_n
    )
    response = []
    for i, (grant, score) in enumerate(
        zip(recommended_grants, recommended_grants_scores)
    ):
        response.append(
            {
                "rank": i + 1,
                "grant_name": grant["grant_name"],
                "score": "{:.2%}".format(score),
                "details_link": grant["details_link"],
                "foundation_name": grant["foundation_name"],
                "grant_prize": grant["grant_prize"],
                "tags": grant["tags"],
            }
        )
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
