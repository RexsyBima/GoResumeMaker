import json
from pydantic import BaseModel


class Identity(BaseModel):
    fullname: str
    phone_number: str
    homeaddress: str
    email: str
    university: str
    gpa: float
    cumlaude: bool
    major: str

    def __str__(self):
        return f"current user data is: {self.fullname.upper()}, with its phone number: {self.phone_number}, its address: {self.homeaddress}, and its email : {self.email}, its university is {self.university}, and its gpa is {self.gpa}, and its cumlaude status is {self.cumlaude}, and its major is {self.major}"


def read_json(filename: str = "profile.json") -> Identity:
    with open(filename, "r") as f:
        data = json.loads(f.read())
        profile = Identity.model_validate(data)
    return profile


def read_md(filename: str) -> str:
    with open(filename, "r") as f:
        resume = f.read()
    return resume


def init_agent():
    pass
