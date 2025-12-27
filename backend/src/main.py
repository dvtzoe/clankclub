import fastapi

from discuss import discuss
from schemas import DiscussRequest

app = fastapi.FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/discuss")
async def discuss_endpoint(request: DiscussRequest):
    user_query = request.query
    if not user_query:
        return fastapi.Response(status_code=400, content="Query is required")

    response = await discuss(user_query)
    return {"response": response}
