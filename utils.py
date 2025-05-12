from dataclasses import dataclass
from typing_extensions import deprecated
import json, os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

load_dotenv()


@dataclass
class OutputMarkdown:
    markdown: str

    def __str__(self):
        return self.markdown


class Identity(BaseModel):
    fullname: str
    phone_number: str
    homeaddress: str
    email: str
    university: str
    gpa: float
    cumlaude: bool
    major: str
    website: str

    def __str__(self):
        return f"current user data is: {self.fullname.upper()}, with its phone number: {self.phone_number}, its address: {self.homeaddress}, and its email : {self.email}, its university is {self.university}, and its gpa is {self.gpa}, and its cumlaude status is {self.cumlaude}, and its major is {self.major}, its website is {self.website}"


@deprecated("use read_jsonv2")
def read_json(filename: str = "profile.json") -> Identity:
    with open(filename, "r") as f:
        data = json.loads(f.read())
        profile = Identity.model_validate(data)
    return profile


def read_jsonv2(filename: str = "profile.json") -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
        assert isinstance(data, dict)
    return data


def unpack_json_dict(data: dict) -> str:
    output = ""
    for k in data:
        output += f"{k}: {data[k]}\n"
    return output


def read_text(filename: str) -> str:
    with open(filename, "r") as f:
        resume = f.read()
    return resume


def init_agent(resume: str) -> Agent[dict, OutputMarkdown]:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    assert DEEPSEEK_API_KEY is not None
    model = OpenAIModel(
        "deepseek-chat",
        provider=DeepSeekProvider(api_key=DEEPSEEK_API_KEY),
    )
    agent = Agent(
        model,
        deps_type=dict,
        output_type=OutputMarkdown,
        system_prompt=(
            f"""you are an ai agent that focuses creating curiculum vitae profile in markdown format. you have a function tool calling to access user data named `return_user_identity`. make sure that the output result will be just like an example below, make sure that it is ATS friendly, return the answer the markdown data only please but without the markdown ```markdown ```

now, the user will inputted the qualification of the job, make sure you create the cv based on that job requirement.
make sure you are priorizing the job requirement, make sure you are creating the cv based on the job requirement, but when it goes to sensitive data like username, home address, take the answer to the current user data. When the job requirement requiring a major that differs than user, make sure that you emphasize of switch career statement in the summary statement. do not add certificate if the provided user data does not have any. add imaginary job experience history as you see fit based on the job description
example output:
{resume}

in the example output, ma
    """
        ),
    )

    @agent.system_prompt
    def return_user_identity(ctx: RunContext[dict]):
        return unpack_json_dict(ctx.deps)

    return agent
