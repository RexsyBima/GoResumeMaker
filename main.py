import subprocess
from markitdown import MarkItDown

from utils import init_agent, read_jsonv2, read_text


def read_resume(filepath: str):
    md = MarkItDown(enable_plugins=True)
    result = md.convert(filepath)
    return result.markdown


if __name__ == "__main__":
    job_desc = read_text("job_desc.txt")
    identity = read_jsonv2()
    resume = read_text("RESUME.md")
    # resume = read_resume("resumetest.pdf")
    agent = init_agent(resume)
    result = agent.run_sync(job_desc, deps=identity)
    with open("RESUMEOUTPUT.md", "w") as f:
        f.write(result.output.markdown)

    result = subprocess.run(["./resume"], capture_output=True, text=True)
    print("Output:", result.stdout)
