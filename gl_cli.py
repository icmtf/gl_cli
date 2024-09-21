import configparser
import os
import shutil
import subprocess
from pathlib import Path

import click
import gitlab
from rich.console import Console
from rich.table import Table

CONFIG_FILE = Path.home() / ".gl-cli-config"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def save_config(url, token):
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"url": url, "token": token}
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def get_gitlab_instance():
    config = load_config()
    url = os.environ.get("GITLAB_URL") or config.get("DEFAULT", "url", fallback=None)
    token = os.environ.get("GITLAB_TOKEN") or config.get("DEFAULT", "token", fallback=None)

    if not url or not token:
        click.echo("GitLab URL or token not found. Please set them using the 'config' command.")
        return None

    try:
        gl = gitlab.Gitlab(url, private_token=token)
        gl.auth()
        return gl
    except gitlab.exceptions.GitlabAuthenticationError:
        click.echo("Authentication failed. Please check your token and URL.")
        return None
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")
        return None


def clone_or_update_repo(project, repo_path, token, overwrite=False):
    if os.path.exists(repo_path):
        if overwrite:
            click.echo(f"Removing existing repository: {project.path_with_namespace}")
            shutil.rmtree(repo_path)
        else:
            click.echo(f"Updating repository: {project.path_with_namespace}")
            subprocess.run(["git", "-C", repo_path, "pull"], check=True)
            return

    click.echo(f"Cloning: {project.path_with_namespace}")
    clone_url = project.http_url_to_repo.replace("https://", f"https://oauth2:{token}@")
    subprocess.run(["git", "clone", clone_url, repo_path], check=True)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--url", prompt="GitLab URL", help="GitLab instance URL")
@click.option("--token", prompt="GitLab Token", help="Private token for authentication")
def config(url, token):
    """Set GitLab URL and token"""
    save_config(url, token)
    click.echo("Configuration saved successfully.")


@cli.command()
def check():
    """Check if GitLab token and URL are working"""
    gl = get_gitlab_instance()
    if gl:
        click.echo("Authentication successful. Token and URL are working.")


@cli.command()
def list():
    """List available repositories for the token"""
    gl = get_gitlab_instance()
    if gl:
        projects = gl.projects.list(all=True)

        table = Table(title="GitLab Repositories")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Project Name", style="magenta")
        table.add_column("Repo Name", style="yellow")
        table.add_column("Repo Path", style="green")

        for project in projects:
            project_path = project.path_with_namespace
            path_parts = project_path.split("/")
            project_name = path_parts[0]
            repo_name = path_parts[-1]
            repo_path = "/".join(path_parts[1:])

            table.add_row(str(project.id), project_name, repo_name, repo_path)

        console = Console()
        console.print(table)


@cli.group()
def repo():
    """Commands for repository management"""
    pass


@repo.command()
@click.option("--dir", "clone_dir", required=True, help="Directory to clone repositories into")
def clone(clone_dir):
    """Clone repositories"""
    gl = get_gitlab_instance()
    if gl:
        projects = gl.projects.list(all=True)
        for project in projects:
            repo_path = os.path.join(clone_dir, project.path_with_namespace)
            os.makedirs(os.path.dirname(repo_path), exist_ok=True)
            clone_or_update_repo(project, repo_path, gl.private_token)


@repo.command()
@click.option("--dir", "clone_dir", required=True, help="Directory to clone repositories into")
def clone_overwrite(clone_dir):
    """Clone repositories, overwriting existing ones"""
    gl = get_gitlab_instance()
    if gl:
        projects = gl.projects.list(all=True)
        for project in projects:
            repo_path = os.path.join(clone_dir, project.path_with_namespace)
            os.makedirs(os.path.dirname(repo_path), exist_ok=True)
            clone_or_update_repo(project, repo_path, gl.private_token, overwrite=True)


@repo.command()
@click.option("--dir", "clone_dir", required=True, help="Directory with cloned repositories")
def clone_update(clone_dir):
    """Update existing repositories"""
    gl = get_gitlab_instance()
    if gl:
        projects = gl.projects.list(all=True)
        for project in projects:
            repo_path = os.path.join(clone_dir, project.path_with_namespace)
            if os.path.exists(repo_path):
                click.echo(f"Updating repository: {project.path_with_namespace}")
                subprocess.run(["git", "-C", repo_path, "pull"], check=True)
            else:
                click.echo(f"Repository not found, skipping: {project.path_with_namespace}")


if __name__ == "__main__":
    cli()
