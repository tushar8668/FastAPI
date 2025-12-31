from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name : str
    age : Annotated[int, Field(gt=0, le=100, name='Age of the person',description='Age should be less 100.')]
    height : float
    weight : Annotated[float, Field(gt=0, strict=True)]
    married : Annotated[Optional[bool], Field(default=False)]
    allergies : Annotated[Optional[List[str]], Field(max_length=5)]
    contact_details : Dict[str, str]
    email : EmailStr
    url : Optional[AnyUrl] = None
    
    """
    BaseModel : BaseModel is a Pydantic class that helps you store, validate, convert data automatically, and throw clear errors when data is wrong.
    Annotated : Annotated lets you attach extra information (rules, metadata) to a type.
    Field() : Field() is a Pydantic helper used to add validation rule, default values, metadata, and control how data behaves.
    Optional  : This value can be present OR it can be None.
    EmailStr : is a special Pydantic type used to validate email addresses.
    AnyUrl : is special Pydantic type used to validate the url.
    List[str] : A list where every item must be a string.
    Dict[str, str] : A Dictionary where key and value both are in the string format.
    """

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

patient_info1 = {"name":"Tushar Sutar", "age":100, "height":1.74, "weight":50.6, "allergies":["dust", "pollen"], "contact_details":{'phone':'866897892'}, "email":'tusharsutar@gmail.com', 'url':'https://htp.com'}

patient1 = Patient(**patient_info1)
create_patient_info(patient1)



