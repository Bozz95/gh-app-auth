"""GitHub App authentication CLI for CodeBuild."""
import sys
import time
from pathlib import Path

import jwt
import typer
from github import Auth, GithubIntegration


app = typer.Typer(help="GitHub App authentication for CodeBuild")


def generate_jwt(app_id: int, private_key: str) -> str:
    """Generate JWT for GitHub App authentication."""
    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + (10 * 60),
        "iss": app_id,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token(app_id: int, private_key: str, installation_id: int) -> str:
    """Get installation access token using PyGithub."""
    auth = Auth.AppAuth(app_id, private_key)
    gi = GithubIntegration(auth=auth)
    installation = gi.get_access_token(installation_id)
    return installation.token


@app.command()
def configure_git(
    app_id: int = typer.Option(..., "--app-id", help="GitHub App ID"),
    installation_id: int = typer.Option(..., "--installation-id", help="GitHub App Installation ID"),
    private_key_path: str = typer.Option(..., "--private-key", help="Path to .pem file with Github App private key"),
    repo_owner: str = typer.Option(..., "--repo-owner", help="Repository owner"),
    repo_name: str = typer.Option(..., "--repo-name", help="Repository name"),
):
    """Configure git with GitHub App authentication and print clone URL."""
    try:
        private_key = Path(private_key_path).read_text()
        token = get_installation_token(app_id, private_key, installation_id)
        clone_url = f"https://x-access-token:{token}@github.com/{repo_owner}/{repo_name}.git"
        typer.echo(clone_url)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def get_token(
    app_id: int = typer.Option(..., "--app-id", help="GitHub App ID"),
    installation_id: int = typer.Option(..., "--installation-id", help="GitHub App Installation ID"),
    private_key_path: str = typer.Option(..., "--private-key", help="Path to .pem file with Github App private key"),
):
    """Get installation access token."""
    try:
        private_key = Path(private_key_path).read_text()
        token = get_installation_token(app_id, private_key, installation_id)
        print(token)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
