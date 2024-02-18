import typer
from pathlib import Path

# Add the cli directory to the Python path
# spai_cli_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(spai_cli_dir))

from .commands import auth as _auth
from .commands import list
from .repos import APIRepo
from .project import (
    init_project,
    install_requirements,
    run_local,
    deploy_folder,
    get_logs,
    download_template,
    deploy_template,
    get_services,
    stop_service,
    stop_service_by_name,
    delete_project,
)
from .auth import auth
from . import __version__

app = typer.Typer(help="Welcome to SPAI")
app.add_typer(_auth.app, name="auth")
app.add_typer(list.app, name="list")


@app.command(help="Create a new project from starter template")
def init(path: Path = typer.Option(Path.cwd(), "-p", "--path", help="Project path")):
    try:
        project_name = typer.prompt("Project name")
        init_project(path, project_name)
        typer.echo(f"Project {project_name} created at {path}")
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command(help="Install requirements for a project")
def install(
    path: Path = typer.Argument(Path.cwd(), help="Project path"),
    verbose: bool = typer.Option(False, "-v", "--verbose"),
):
    try:
        install_requirements(path, typer, verbose)
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command(help="Run a project locally")
def run(
    path: Path = typer.Argument(Path.cwd(), help="Project path"),
    template: str = typer.Option(None, "-t", "--template", help="Template name"),
    template_path: Path = typer.Option(
        Path.cwd(),
        "-p",
        "--path",
        help="Destination path for the project created from the template",
    ),
    force: bool = typer.Option(False, "-f", "--force", help="Force download template"),
):
    try:
        if template is not None:
            user = auth()
            path = download_template(user, template, template_path, force)
        return run_local(path, typer)
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command(help="Deploy a project to the cloud")
def deploy(
    path: Path = typer.Argument(Path.cwd(), help="Project path"),
    template: str = typer.Option(None, "-t", "--template", help="Template name"),
    verbose: bool = typer.Option(False, "-v", "--verbose"),
):
    try:
        user = auth()
        if template:
            return deploy_template(user, template)
        return deploy_folder(user, path, typer, verbose)
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command(help="Retrieve the logs of a service")
def logs(
    project: str = typer.Argument(..., help="Project name"),
    service_type: str = typer.Argument(
        ..., help="Service type (script, api, ui, etc.)"
    ),
    service_name: str = typer.Argument(..., help="Service name"),
):
    try:
        user = auth()
        logs = get_logs(user, project, service_type, service_name)
        typer.echo(logs)
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command(help="Clone a template")
def clone(
    template: str = typer.Argument(..., help="Template name"),
    path: Path = typer.Option(
        Path.cwd(),
        "-p",
        "--path",
        help="Destination path for the project created from the template",
    ),
    force: bool = typer.Option(False, "-f", "--force", help="Force download template"),
):
    try:
        user = auth()
        path = download_template(user, template, path, force)
        typer.echo(f"Template available at {path}.")
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command(help="Stop a project")
def stop(
    project: str = typer.Argument(..., help="Project name"),
    service_type: str = typer.Argument(None, help="Service type"),
    service_name: str = typer.Argument(None, help="Service name"),
):
    try:
        user = auth()
        if project is None:
            raise Exception("Project name is required.")
        services = get_services(user, project)
        if len(services) == 0:
            return typer.echo(f"No services running in project '{project}'.")
        if service_type and service_name:
            return stop_service_by_name(user, project, service_type, service_name)
        typer.echo(f"Stopping all services in project '{project}'...")
        for service_id in services:
            stop_service(user, project, service_id)
        return typer.echo(f"Stopped all services in project '{project}'.")
    except Exception as e:
        return typer.echo(e)


@app.command(help="Delete a project")
def delete(
    project: str = typer.Argument(..., help="Project name"),
):
    try:
        user = auth()
        if project is None:
            raise Exception("Project name is required.")
        delete_project(user, project)
        return typer.echo(f"Deleted project '{project}'.")
    except Exception as e:
        return typer.echo(e)


@app.command(help="Get SPAI version")
def version():
    typer.echo(f"SPAI Version: {__version__}")


@app.command(help="Get SPAI API url and status")
def api():
    repo = APIRepo()
    typer.echo(f"SPAI API URL: {repo.url}")
    typer.echo(repo.info())


if __name__ == "__main__":
    app()
