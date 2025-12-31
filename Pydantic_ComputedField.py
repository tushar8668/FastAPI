from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name : str
    age : int
    height : float
    weight : float
    married : Optional[bool] = None
    allergies : Optional[List[str]] = None
    contact_details : Dict[str, str]
    email : EmailStr
    url : Optional[AnyUrl] = None

    """
    @computed_field : is used to create a field whose value is calculated from other fields, not given by the user.
    
    @property : lets us use a function like a variable.
    example : 

        👉 without @property :

            class Person:
                def full_name(self):
                return "Tushar Sutar"

            p1 = Person()
            p1.full_name()

        With @property :   
            p1.full_name

    """ 
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    

def create_patient_info(patient : Patient): 
    print(patient.name)
    print(patient.age)
    print(patient.height)
    print(patient.weight)
    print(patient.allergies)
    print("bmi", patient.bmi)
    print(patient.married)
    print(patient.contact_details)
    print(patient.email)
    print(patient.url)

patient_info1 = {"name":"tushar sutar", "age":'50', "height":1.74, "weight":50.6, "allergies":["dust", "pollen"], "contact_details":{'phone':'866897892'}, "email":'tusharsutar@hdfc.com', 'url':'https://htp.com'}

patient1 = Patient(**patient_info1)
create_patient_info(patient1)
