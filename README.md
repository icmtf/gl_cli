# GitLab CLI

GitLab CLI is a small command-line tool for interacting with GitLab repositories. It allows users to configure their GitLab credentials, list repositories, and perform various operations such as cloning and updating repositories.

## TLDR Quickstart
1. Install Python Libraries and download script.

Using wget:
```bash
pip install click pre-commit python-gitlab rich && \
  wget https://raw.githubusercontent.com/icmtf/gl_cli/refs/heads/master/gl_cli.py
```
Using cURL:
```bash
pip install click python-gitlab rich && \
  curl https://raw.githubusercontent.com/icmtf/gl_cli/refs/heads/master/gl_cli.py \
    -o gl_cli.py
```

2. Run the script.
```bash
python gl_cli.py check
```
<details>
   <summary>Quickstart Demo Screen recording</summary>

   ![Quickstart Demo](https://github.com/icmtf/gl_cli/blob/media/quickstart.gif)
</details>

## Requirements

- Python 3.10+
- Installed libraries: click, python-gitlab, rich

## Installation

1. Clone this repository:
   ```
   git clone <REPOSITORY_URL>
   ```

2. Navigate to the project directory:
   ```
   cd <DIRECTORY_NAME>
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before using the tool, you need to configure the GitLab instance URL and private token. You can do this using the command:

```
python gl_cli.py config
```

Alternatively, you can set the environment variables `GITLAB_URL` and `GITLAB_TOKEN`.

## Usage

### Checking Configuration

To check if your GitLab token and URL are working correctly:

```
python gl_cli.py check
```

### Listing Repositories

To display a list of available repositories:

```
python gl_cli.py list-repos
```

### Repository Operations

#### Cloning Repositories

To clone all repositories into a specified directory:

```
python gl_cli.py repo clone --dir <DIRECTORY_PATH>
```

#### Cloning Repositories with Overwrite

To clone all repositories, overwriting existing ones:

```
python gl_cli.py repo clone-overwrite --dir <DIRECTORY_PATH>
```

#### Updating Existing Repositories

To update existing repositories in a specified directory:

```
python gl_cli.py repo clone-update --dir <DIRECTORY_PATH>
```

## Pre-commit Configuration

The project includes a pre-commit configuration that uses the following tools:
- Ruff: for linting and formatting Python code
- Bandit: for Python code security analysis

To install pre-commit hooks, run:

```
pre-commit install
```

## Project Structure

- `gl_cli.py`: Main CLI script
- `.pre-commit-config.yaml`: Pre-commit configuration
- `.ruff.toml`: Configuration for Ruff
- `pyproject.toml`: Configuration for Bandit and other Python tools

## License

MIT