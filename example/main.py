from datetime import datetime, time, timedelta
from uuid import UUID
from typing import Optional, List
from fastapi import FastAPI, Query, Path, Body, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class Batch(BaseModel):
    name: str = Field(..., min_length=3, example="hello")
    description: str
    claims: Optional[List[Optional[str]]] = None
    items: Item


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/entities/")
async def get_items(q: Optional[str] = Query(None, max_length=50, title="query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/peoples/")
def read_people(
    q: Optional[str] = Query(..., regex="^fast", title="Simple query"),
    queries: Optional[List[str]] = Query(None),
):
    results = {
        "people": [{"name": "John Doe", "age": 32}, {"name": "Jane Doe", "age": 30}]
    }
    if q:
        results.update({"q": q})
    return results


@app.get("/user-items/{item_id}")
async def read_user_item_id(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


@app.get("/items/{item_id}/")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# use function parameter alias for get operation
@app.get("/batches/{id}/")
def read_batch(
    batch_id: int = Path(
        ..., alias="id", title="Batch ID", description="The ID of selected batch"
    )
):
    return {"batch_id": batch_id, "name": "January"}


# embed body as json property
@app.put("/batches/{batch_id}/")
async def update_batch(batch_id: int, batch: Batch = Body(..., embed=True)):
    return {"batch": batch}


@app.put("/demos/{item_id}")
async def read_demo_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

@app.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

@app.get("/home/")
async def main():
    content = """
        <body>
        <form action="/files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)