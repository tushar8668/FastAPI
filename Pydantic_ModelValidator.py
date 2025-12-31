from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name : str
    age : int
    height : float
    weight : float
    married : Optional[bool] = False  
    allergies : Optional[List[str]] = None
    contact_details : Dict[str, str]
    email : EmailStr
    url : Optional[AnyUrl] = None

    """
    FieldValidator is use to validate the single field, but what if we want to validate more than one field
    Example : Suppose we want a validate saying if age > 70 then patient must have emergency number in contact_details

    To solve above problem, @ModelValidator comes in..

    @modelvalidator : is used when you want to check or change the whole object, not just one.
    Think like this

    Field validator:
    “Is the email valid?”

    Model validator:
    “Does age match date_of_birth?”
    “If country is India, is phone number starting with 91?”

    👉 These need multiple fields at once.

    """

    @model_validator(mode = 'after')
    def validate_emergency_details(cls, model):
        if model.age > 70 and 'emergency' not in model.contact_details:
            raise ValueError('Age greater than 70 must have emergency number.')
        else:
            return model
        
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

patient_info1 = {"name":"tushar sutar", "age":'80', "height":1.74, "weight":50.6, "allergies":["dust", "pollen"], "contact_details":{'phone':'866897892','emergency':'86669789'}, "email":'tusharsutar@hdfc.com', 'url':'https://htp.com'}

patient1 = Patient(**patient_info1)
create_patient_info(patient1)
