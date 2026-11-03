from typing import Optional, List
from pydantic import BaseModel, Field

class CarFeaturesInput(BaseModel):
    symboling: int = Field(default=3, description="Insurance risk rating (-3 to 3)")
    carbrand: Optional[str] = Field(default="toyota", description="Car manufacturer/brand name")
    CarName: Optional[str] = Field(default=None, description="Full car name (e.g. toyota corolla)")
    fueltype: str = Field(default="gas", description="gas or diesel")
    aspiration: str = Field(default="std", description="std or turbo")
    doornumber: str = Field(default="four", description="two or four")
    carbody: str = Field(default="sedan", description="convertible, hatchback, sedan, wagon, hardtop")
    drivewheel: str = Field(default="fwd", description="rwd, fwd, 4wd")
    enginelocation: str = Field(default="front", description="front or rear")
    wheelbase: float = Field(default=98.8, description="Wheelbase dimension")
    carlength: float = Field(default=175.0, description="Car length in inches")
    carwidth: float = Field(default=65.5, description="Car width in inches")
    carheight: float = Field(default=54.0, description="Car height in inches")
    curbweight: int = Field(default=2400, description="Curb weight in lbs")
    enginetype: str = Field(default="ohc", description="Engine type: dohc, ohcv, ohc, l, etc.")
    cylindernumber: str = Field(default="four", description="four, six, five, eight, etc.")
    enginesize: int = Field(default=120, description="Engine size in cubic inches")
    fuelsystem: str = Field(default="mpfi", description="mpfi, 2bbl, mfi, 1bbl, etc.")
    boreratio: float = Field(default=3.3, description="Bore ratio")
    stroke: float = Field(default=3.2, description="Stroke dimension")
    compressionratio: float = Field(default=9.0, description="Compression ratio")
    horsepower: int = Field(default=100, description="Horsepower")
    peakrpm: int = Field(default=5200, description="Peak RPM")
    citympg: int = Field(default=26, description="City MPG")
    highwaympg: int = Field(default=32, description="Highway MPG")

    model_config = {
        "json_schema_extra": {
            "example": {
                "symboling": 1,
                "carbrand": "toyota",
                "fueltype": "gas",
                "aspiration": "std",
                "doornumber": "four",
                "carbody": "sedan",
                "drivewheel": "fwd",
                "enginelocation": "front",
                "wheelbase": 95.7,
                "carlength": 166.3,
                "carwidth": 64.4,
                "carheight": 53.0,
                "curbweight": 2081,
                "enginetype": "ohc",
                "cylindernumber": "four",
                "enginesize": 98,
                "fuelsystem": "2bbl",
                "boreratio": 3.19,
                "stroke": 3.03,
                "compressionratio": 9.0,
                "horsepower": 70,
                "peakrpm": 4800,
                "citympg": 30,
                "highwaympg": 37
            }
        }
    }

class PredictionResponse(BaseModel):
    status: str
    predicted_price: float
    currency: str = "USD"
    model_version: str
    inference_id: str

class BatchPredictionRequest(BaseModel):
    records: List[CarFeaturesInput]

class BatchPredictionResponse(BaseModel):
    status: str
    count: int
    predictions: List[float]
    model_version: str

class HealthResponse(BaseModel):
    status: str
    service: str
    model_loaded: bool
    version: str
