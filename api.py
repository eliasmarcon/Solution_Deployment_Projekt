import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from sklearn import linear_model

app = FastAPI()

# load the model from disk
filename = './lm_model.pkl'
model = pickle.load(open(filename, 'rb'))

# enable validation
class Prediction(BaseModel):
    noOfBreaches: int

# create endpoint
@app.post("/predict", response_model=Prediction)
def predict(year: int):
    return {"noOfBreaches": int(model.predict([[year]]))}

# startup function
def start():
    uvicorn.run("api:app", host="0.0.0.0", reload=False)

if __name__ == '__main__':
    start()
