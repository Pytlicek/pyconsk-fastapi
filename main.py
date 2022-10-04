from fastapi import FastAPI, Path
from pydantic import BaseModel
from users_router import router as us_r


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="Our Perfect API Service",
    version="0.1.1",
    openapi_tags=tags_metadata,
    description="""
    This is our API service
    We can write here something like links or so...
    """,
)

app.include_router(us_r, prefix="/users")


@app.get("/", tags=["items"])
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.post("/items/get/")
def read_item_wide(item_id: int, description: str | None = None):
    return {"item_id": item_id, "description": description}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


items = {
    "1": {"name": "Foo", "price": 50.2, "description": "Fooooooo"},
    "2": {
        "name": "Bar",
        "description": "The Bar fighters",
        "price": 62,
        "tax": 20.2,
    },
    "3": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description", "price"],
)
async def read_item_name(item_id: str):
    """
    ABC
    Sem mozeme dat nejaky popis
    ## Aj tu
    [Link text Here](https://link-url-here.org)
    """
    # if item_id not in items:
    #     return {
    #         "name": "string",
    #         "description": "string",
    #         "price": 0,
    #         "tax": 0,
    #     }
    return items[item_id]
