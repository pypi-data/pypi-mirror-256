from launchflow.cli.project_gen import Framework

# TODO: look at adding templates for using the provided resources
FAST_API_TEMPLATE = """\
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
"""


def template(framework: Framework):
    if framework == Framework.FASTAPI:
        return FAST_API_TEMPLATE
