from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
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
    @field_validator('field') : field_validator is a function that automatically runs when a model is created, to check or change a field’s value.
    You never call it yourself.
    Because of @field_validator('email'), Pydantic automatically passes the value of the email field to that function as value.
    Whenever the email field gets a value, send that value to this function.
    
    @classmethod : 

    """

    @field_validator('email')
    @classmethod
    def email_check(cls, value):
        valid_domains = ['hdfc.com','icici.com']
        domain = value.split('@')[-1]

        if domain not in valid_domains:
            raise ValueError(f"Invalid Domains should be from {valid_domains}")
        
        return value

def create_patient_info(patient : Patient): 
    print(patient.name)
    print(patient.age)
    print(patient.height)
    print(patient.weight)
    print(patient.allergies)
    print(patient.married)
    print(patient.contact_details)
    print(patient.email)
    print(patient.url)

patient_info1 = {"name":"Tushar Sutar", "age":100, "height":1.74, "weight":50.6, "allergies":["dust", "pollen"], "contact_details":{'phone':'866897892'}, "email":'tusharsutar@hdfc.com', 'url':'https://htp.com'}

patient1 = Patient(**patient_info1)
create_patient_info(patient1)