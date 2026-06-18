from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app =FastAPI()

@app.get("/")
def get_root():
    return {"message": "Hello World"}

# Path Parameters
@app.get("/items/{item_id}")
def get_item(item_id:int):
    return {"item_id": item_id}

@app.get("/models/{model_name}")
def get_models(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    else:
        return {"model_name": model_name, "message": "Have some residuals"}
    
@app.get("/files/{file_path:path}")
def get_file(file_path:str):
    return {"file_path": file_path}

# Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/itemsq/")
def get_query_items(skip:int=0, limit:int=10):
    return fake_items_db[skip: skip + limit]


# @app.get("/itemsq/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


@app.get("/itemsq/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# request body



class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
