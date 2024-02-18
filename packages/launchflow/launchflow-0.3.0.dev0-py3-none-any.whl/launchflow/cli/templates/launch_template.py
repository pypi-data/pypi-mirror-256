from typing import List

from launchflow.cli.project_gen import Framework, Resource

LAUNCH_TEMPLATE = """\
import launchflow

launchflow.project = "{project}"

app = launchflow.ServerlessDeployment("{project}", {entrypoint})
{resources}
{environment}
"""


def template(project: str, framework: str, resources: List[str]):
    if framework == Framework.FASTAPI:
        entrypoint = '"uvicorn main:app"'
    else:
        raise NotImplementedError(f"{framework} is not supported yet.")

    resource_strs = []
    resource_vars = []
    for resource in resources:
        if resource == Resource.POSTGRESQL:
            resource_strs.append(f'pg = launchflow.Postgres("{project}-postgres")')
            resource_vars.append("pg")
        else:
            raise NotImplementedError(f"{resource} is not supported yet.")

    env = []
    if not resource_vars:
        env = "dev = launchflow.Environment([app])"
    else:
        env = f"dev = launchflow.Environment([app], [{', '.join(resource_vars)}])"
    return LAUNCH_TEMPLATE.format(
        project=project,
        entrypoint=entrypoint,
        resources=("\n" + "\n".join(resource_strs)) if resource_strs else "",
        environment=env,
    )
