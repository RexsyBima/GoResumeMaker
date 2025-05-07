from unittest import TestCase
from dataclasses import dataclass
import os
import unittest
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider


@dataclass
class OutputMarkdown:
    markdown: str
    def __str__(self):
        return self.markdown

@dataclass
class Identity:
    fullname: str
    phone_number: str 
    homeaddress: str
    email: str
    def __str__(self):
        return f"current user data is: {self.fullname.upper()}, with its phone number: {self.phone_number}, its address: {self.homeaddress}, and its email : {self.email}"

load_dotenv()


class TestAgent(TestCase):
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    assert DEEPSEEK_API_KEY is not None
    model = OpenAIModel(
        'deepseek-chat',
        provider=DeepSeekProvider(api_key=DEEPSEEK_API_KEY),
    )
    agent = Agent(model)

    @unittest.skip("finished")
    def test_run_agent(self):
        result = self.agent.run_sync("is this working?")
        print(result)
        self.assertTrue(bool(result))


    def test_run_cv_agent(self):
        with open("RESUME.md", "r") as f:
            resume = f.read()
        agent = Agent(self.model, deps_type=Identity, output_type=OutputMarkdown,system_prompt=(f"""you are an ai agent that focuses creating curiculum vitae profile in markdown format. make sure that the output result will be just like an example below, make sure that it is ATS friendly, return the answer the markdown data only please but without the markdown ```markdown ```

now, the user will inputted the qualification of the job, make sure you create the cv based on that job requirement.
make sure you are priorizing the job requirement, make sure you are creating the cv based on the job requirement, but when it goes to sensitive data like username, home address, take the answer to the current user data
example output:
{resume}
        """))
        @agent.system_prompt
        def return_user_identity(ctx: RunContext[Identity]):
            return str(ctx.deps)

        job_desc = """
About the job

Junior Backend Developer (Python)


Requirements :

    Bachelor's Degree in Computer Science, Information Technology, or a related field.
    At least 1 years of experience in backend development, with strong experience in Python.
    Experience with django Rest Framework sama flask/JWT token
    Strong problem-solving skills and the ability to optimize code for performance and scalability.
    Excellent communication skills to effectively collaborate with team members and stakeholders.
    Ability to work independently and proactively in a fast-paced environment.
    Strong attention to detail, analytical skills, and problem-solving abilities.
    Proven experience working effectively in collaborative team environments.
    Handle project in sector financial use Django Rest Framework sama flask/JWT token.
    Ready on site yogyakarta
        """
        result = agent.run_sync(job_desc, deps=Identity(fullname="rexsy bima trima wahyu", phone_number="+6234321342", homeaddress="Purwokerto, Jawa Tengah", email="rere@gmail.com"))
        print(result)
        with open("RESUMEtest.md", "w") as f:
            f.write(result.output.markdown)
        self.assertTrue(bool(result))


class TestDeps(TestCase):
    @unittest.skip("finished")
    def test_deps(self):
        @dataclass
        class Identity:
            fullname: str
            phone_number: str 
            address: str
            email: str
            def __str__(self):
                return f"{self.fullname}, {self.phone_number}, {self.address}, {self.email}"
        identity = Identity(fullname="test", phone_number="test", address="test", email="test")
        print(str(identity))
        self.assertTrue(bool(identity))


class TestMD(TestCase):
    @unittest.skip("finished")
    def test_read_md(self):
        with open("RESUME.md", "r") as f:
            print(f.read())
            self.assertTrue(True)
