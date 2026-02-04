# GitHub App Authentication CLI <!-- omit in toc -->

- [Installation](#installation)
  - [Development Setup](#development-setup)
  - [Build Distribution](#build-distribution)
- [Usage](#usage)
  - [Get Installation Token](#get-installation-token)
  - [Configure Git with Clone URL](#configure-git-with-clone-url)
- [Test Local CodeBuild Run](#test-local-codebuild-run)
  - [Setup](#setup)
  - [Buildspec Example](#buildspec-example)
- [References](#references)

A minimal Python CLI tool for GitHub App authentication in AWS CodeBuild environments.

**This is useful when needing write permission on a Github repository since CodeStart Connections only offer read permissions.**

## Installation

### Development Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and project
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### Build Distribution

```bash
# Build wheel and source distribution
uv build

# Output: dist/gh_app_auth-0.1.0-py3-none-any.whl
#         dist/gh_app_auth-0.1.0.tar.gz
```

## Usage

### Get Installation Token

```bash
gh-app-auth get-token \
  --app-id YOUR_APP_ID \
  --installation-id YOUR_INSTALLATION_ID \
  --private-key /path/to/private-key.pem
```

### Configure Git with Clone URL

```bash
REPO_URL=$(gh-app-auth configure-git \
  --app-id YOUR_APP_ID \
  --installation-id YOUR_INSTALLATION_ID \
  --private-key /path/to/private-key.pem \
  --repo-owner owner \
  --repo-name repo)

git clone "$REPO_URL"
```

## Test Local CodeBuild Run

### Setup

1. Install [CodeBuild local agent](https://docs.aws.amazon.com/codebuild/latest/userguide/use-codebuild-agent.html)
2. Create `test.env` file with your credentials:

```bash
GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nYourKey...\n-----END RSA PRIVATE KEY-----"
GITHUB_APP_ID=your_app_id
GITHUB_APP_INSTALL_ID=your_installation_id
GITOPS_REPO_OWNER=owner
GITOPS_REPO_NAME=repo
GIT_USERNAME=bot
GIT_MAIL=bot@example.com
```

3. Run CodeBuild locally:

```bash
./codebuild_build.sh -i "public.ecr.aws/codebuild/amazonlinux-x86_64-standard:5.0" -a /tmp/artifacts -e test.env
```

### Buildspec Example

Replace manual authentication with the CLI:

```yaml
pre_build:
  commands:
      - pip install https://github.com/Longwave-innovation/gh-app-auth/releases/download/v0.2.0/gh_app_auth-0.2.0-py3-none-any.whl
      
      - echo "Saving private key into .pem file..."
      - echo "$GITHUB_APP_PRIVATE_KEY" > private_key.pem
      
      - echo "Getting authenticated clone URL..."
      - |
        REPO_URL=$(gh-app-auth configure-git \
          --app-id $GITHUB_APP_ID \
          --installation-id $GITHUB_APP_INSTALL_ID \
          --private-key private_key.pem \
          --repo-owner $GITOPS_REPO_OWNER \
          --repo-name $GITOPS_REPO_NAME)
      
      - echo "Configuring Git..."
      - git config --global user.email "$GIT_MAIL"
      - git config --global user.name "$GIT_USERNAME"

build:
  commands:
    - git clone "$REPO_URL"
    - cd $GITOPS_REPO_NAME
    # ... rest of your commands
```

## References

- [uv Documentation](https://docs.astral.sh/uv/)
- [GitHub Apps Authentication](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app)
