from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import List, Dict, Annotated, Literal, Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()

class Patient(BaseModel):
    
    Id : Annotated[str, Field(..., description="Unique Identification ID for each Patient.", examples=['P001'])]
    Name : Annotated[str, Field(..., description="Name of the Patient.")]
    Age : Annotated[int, Field(..., gt=0, lt=100, description="Age of the Patient.")]
    City : Annotated[str, Field(description="City where patient is Living.")]
    Gender : Annotated[Literal['Male','Female','Others'], Field(..., description="Gender of the Patient.")]
    Weight : Annotated[float, Field(..., gt=0, description="Weight of the Patient.")]
    Height : Annotated[float, Field(..., gt=0, description="Height of the Patient.")]

    @computed_field
    @property
    def BMI(self) -> float:
        bmi = self.Weight/(self.Height**2)
        return bmi
    
    @computed_field
    @property
    def Verdict(self) -> str:
        if self.BMI > 15:
            return "Underweight"
        elif self.BMI > 25:
            return "Overweight"
        else:
            return "Obese"

class UpdatePatient(BaseModel):
    Name : Annotated[Optional[str], Field(default=None)]
    Age : Annotated[Optional[int], Field(gt=0, default=None)]
    City : Annotated[Optional[str], Field(default=None)]
    Gender : Annotated[Optional[Literal['Male','Female','Others']], Field(default=None)]
    Weight : Annotated[Optional[float], Field(gt=0, default=None)]
    Height : Annotated[Optional[float], Field(gt=0, default=None)]


def load_data():
    with open('Database.json', 'r') as p:
        data = json.load(p) 
    return data    
    
def save_data(data):
    with open('Database.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def home():
    return {'Message':'Welcome, This is a Patient Management Application.'}

@app.get("/about")
def about():
    return {'Message':'This is an patient management application. Where you can get the detailed view and managment of your patients records.'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patients/{patient_id}")
def view_patients(patient_id : str = Path(..., description="Enter patient_id to get the details.")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient_ID not found.")
    
@app.get("/sort")
def view_sort(sort_by : str = Query(..., description="Add the parameters to sort the patients data."), 
              order : str = Query('asc', description="Sort in ASC or Desc order.")):
    
    valid_fields = ['Height', 'Weight', 'BMI']
    if sort_by not in valid_fields: 
        raise HTTPException(status_code=400, detail=f"Invalid Detail, select from {valid_fields}")
        
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid Detail, Select from [asc, desc]")
    
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by,0), reverse=sort_order)  
    
    return sorted_data

@app.post("/create")
def create_record(patient:Patient):
    # Load the Data
    data = load_data()

    # Checking if Id is already exists in the Database.
    if patient.Id in data:
        raise HTTPException(status_code=400, detail="Patient ID is already exists in the Database.")

    # Save new record in the database.
    data[patient.Id] = patient.model_dump(exclude="Id")

    save_data(data)

    # Message for user...
    return JSONResponse(status_code=201, content="New Record Added Successfully..")

@app.put('/edit/{patient_id}')
def update_info(patient_id : str, updatepatient : UpdatePatient):
    #load the data
    data = load_data()
    
    #Check if id is present to update the info
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Id not found in our database.")
    
    # existing patient info
    existing_patient_info = data[patient_id]

    #updated_info
    updated_patient_info = updatepatient.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #update existing data
    existing_patient_info['Id'] = patient_id

    pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = pydantic_object.model_dump(exclude='Id')
    data[patient_id] = existing_patient_info

    #save the data
    save_data(data)

    # Message
    return JSONResponse(status_code=
                        201, content={'Message':"Record Updated successfully..."})


@app.delete("/delete/{patient_id}")
def delete_patient_details(patient_id:str):
    #load the data
    data = load_data()

    #Check if Id is present in the database
    if patient_id not in data:
        raise HTTPException(status_code=404, detail= f"Patient ID {patient_id} not found in the database.")
    
    #delete the record
    del data[patient_id]

    #save the data
    save_data(data)

    return JSONResponse(status_code=201, content={'Message':f'Patient Id {patient_id} deleted from database.'})






