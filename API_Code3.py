from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('Database.json', 'r') as p:
        data = json.load(p) 
    return data    
   
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
def view_patients(patient_id : str = Path(..., description="Enter patient_id to get the details.", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient_ID not found.")
    
@app.get("/sort")
def view_sort(sort_by : str = Query(..., description="Add the parameters to sort the patients data.", example='Height'), 
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