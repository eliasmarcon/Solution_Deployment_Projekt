import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
# from fastapi.responses import StreamingResponse
# from fastapi import FastAPI, UploadFile, File,HTTPException

app = FastAPI(title = "Percentage Calculation")

class Percentage(BaseModel):
    
    percentageFrei : float
    percentageOCovid : float
    percentageCovid : float

@app.get("/")
def root():
    return {"hello fhtw course!"}

@app.post("/calculatePercantage", response_model = Percentage)
def operator(maxGesamtkapazität : int, sumFrei : int, sumOCovid : int, sumCovid : int):

    percentageFrei = round(((sumFrei / maxGesamtkapazität) * 100), 2)
    percentageOCovid = round(((sumOCovid / maxGesamtkapazität) * 100), 2)
    percentageCovid = round(((sumCovid / maxGesamtkapazität) * 100), 2)

    return {'percentageFrei' : percentageFrei, 'percentageOCovid' : percentageOCovid, 'percentageCovid' : percentageCovid}


def start():
    uvicorn.run("FastAPI:app", host="0.0.0.0",reload=False)

if __name__ == '__main__':
    start()