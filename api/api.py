import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()

filename = '../lm_model.pkl'

# load the model from disk
model = pickle.load(open(filename, 'rb'))


class Prediction(BaseModel):
    noOfBreaches: int


@app.post("/predict", response_model=Prediction)
def predict(year: int):
    return {"noOfBreaches": int(model.predict([[year]]))}


def start():
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=False)


if __name__ == '__main__':
    start()
