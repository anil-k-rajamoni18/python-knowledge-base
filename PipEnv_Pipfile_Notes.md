# Pipfile & Pipenv — Complete Guide

A **Pipfile** is a modern dependency management file used in Python projects, mainly with **Pipenv**.

Think of it like:

| Ecosystem   | Dependency File  |
|-------------|------------------|
| Python      | Pipfile          |
| Node.js     | package.json     |
| Java Maven  | pom.xml          |
| Java Gradle | build.gradle     |

---

## Why Pipfile Exists

Earlier Python projects mainly used `requirements.txt`.

**Problems with `requirements.txt`:**

- No clear separation between dev and production dependencies
- Dependency conflicts are harder to manage
- No proper metadata
- No built-in virtual environment handling
- Version resolution is weak

So **Pipfile + Pipfile.lock** were introduced.

---

## Main Files

### 1. Pipfile

Human-readable dependency definition.

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
requests = ">=2.31.0"
pandas = "~=2.2"

[dev-packages]
pytest = "*"
black = "*"

[requires]
python_version = "3.12"
```

### 2. Pipfile.lock

Machine-generated lock file. Contains:

- Exact dependency versions
- Dependency tree
- Hashes for security
- Reproducible builds

```json
{
  "default": {
    "flask": {
      "version": "==3.1.0"
    }
  }
}
```

| File          | Edited By      |
|---------------|----------------|
| Pipfile       | Humans         |
| Pipfile.lock  | Auto-generated |

---

## Important Sections in Pipfile

### `[[source]]`

Defines the package repository.

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"
```

Equivalent to installing from PyPI. You can also use private repos (Nexus, Artifactory, AWS CodeArtifact).

### `[packages]`

Production/runtime dependencies — installed on production servers.

```toml
[packages]
fastapi = "*"
uvicorn = "*"
sqlalchemy = ">=2.0"
```

### `[dev-packages]`

Only for development — usually **not** deployed to production.

```toml
[dev-packages]
pytest = "*"
black = "*"
ruff = "*"
```

Examples: linters, test frameworks, formatters.

### `[requires]`

Python version requirement — helps maintain consistency across teams.

```toml
[requires]
python_version = "3.12"
```

---

## Common Pipenv Commands

### Install Pipenv

```bash
pip install pipenv
```

### Create Project

```bash
pipenv install
```

Creates a virtual environment, Pipfile, and Pipfile.lock.

### Install a Package

```bash
pipenv install flask
```

Automatically updates `Pipfile` and `Pipfile.lock`.

### Install Dev Dependency

```bash
pipenv install pytest --dev
```

Adds to `[dev-packages]`.

### Activate Virtual Environment

```bash
pipenv shell
```

Equivalent to `source venv/bin/activate`.

### Run Without Activating Shell

```bash
pipenv run python app.py
```

### Install From Existing Pipfile

```bash
pipenv install
```

### Install Exact Locked Versions (Production)

```bash
pipenv install --deploy
```

Ensures exact versions from lock file for safer deployments.

---

## Version Symbols

| Symbol | Meaning            |
|--------|--------------------|
| `*`    | Latest             |
| `==`   | Exact version      |
| `>=`   | Greater or equal   |
| `~=`   | Compatible release |

**Example:**

```toml
flask = "~=3.1"
```

Means `>=3.1, <4.0`.

---

## Project Structure Example

```
myproject/
│
├── Pipfile
├── Pipfile.lock
├── app.py
├── requirements.txt
└── src/
```

---

## Pipfile vs requirements.txt

| Feature                  | Pipfile   | requirements.txt |
|--------------------------|-----------|------------------|
| Dependency Resolution    | Better    | Basic            |
| Dev Dependencies         | Separate  | Manual           |
| Locking                  | Yes       | Weak             |
| Virtualenv Integration   | Yes       | No               |
| Readability              | Better    | Simple           |
| Standardization          | Moderate  | Very Common      |

---

## Industry Reality

| Tool                  | Popularity           |
|-----------------------|----------------------|
| pip + requirements.txt | Very High           |
| Pipenv                | Moderate             |
| Poetry                | Growing Fast         |
| uv                    | Very Fast Growing    |
| Conda                 | ML/Data Science      |

---

## Modern Recommendation (2026)

| Use Case              | Recommended              |
|-----------------------|--------------------------|
| Simple backend app    | uv or Poetry             |
| Enterprise legacy     | pip + requirements.txt   |
| ML projects           | Conda or uv              |
| Existing Pipenv project | Continue Pipenv        |

---

## Example Workflow

### Create a FastAPI Project

```bash
mkdir myapi
cd myapi
pipenv install fastapi uvicorn
pipenv install pytest black --dev
```

Generated `Pipfile`:

```toml
[packages]
fastapi = "*"
uvicorn = "*"

[dev-packages]
pytest = "*"
black = "*"
```

Run the app:

```bash
pipenv run uvicorn main:app --reload
```

---

## Best Practices

✅ **Commit:**
- `Pipfile`
- `Pipfile.lock`

❌ **Do NOT commit:**
- virtualenv folder

---

## Important Interview Question

**Difference Between Pipfile and Pipfile.lock**

| File          | Purpose                          | Example               |
|---------------|----------------------------------|-----------------------|
| Pipfile       | Declares dependency intentions   | `flask = ">=3.0"`     |
| Pipfile.lock  | Stores exact resolved versions   | `"flask": "==3.1.0"`  |

This ensures reproducible environments and consistent deployments.

### Simple Mental Model

```
Pipfile       → What you WANT
Pipfile.lock  → What you ACTUALLY installed
```

---

## Useful Pipenv Commands (Advanced)

### 1. Show Installed Dependency Tree

```bash
pipenv graph
```

Example output:

```
fastapi==0.115.0
├── pydantic
├── starlette
│   └── anyio
└── typing-extensions

requests==2.32.0
├── certifi
├── charset-normalizer
├── idna
└── urllib3
```

Shows top-level packages, sub-dependencies, and dependency hierarchy.

### 2. Show Reverse Dependency Tree

```bash
pipenv graph --reverse
```

Example:

```
urllib3==2.2.1
└── requests
```

Meaning: `requests` depends on `urllib3`. Useful for debugging.

### 3. Check Security Vulnerabilities

```bash
pipenv check
```

Checks dependency vulnerabilities and Python version compatibility.

### 4. View Exact Installed Packages

```bash
pipenv run pip freeze
```

Equivalent to `requirements.txt` style output.

### 5. View Dependency Graph Visually (Advanced)

```bash
pip install pipdeptree
pipenv run pipdeptree
```

Very useful for large projects and debugging conflicts.

### 6. Check Outdated Packages

```bash
pipenv update --outdated
```

Shows current version and latest available version.

### 7. Inspect Pipfile.lock Directly

```bash
cat Pipfile.lock
```

Look for:

```json
"default": {}   // production packages
"develop": {}   // dev packages
```

---

## Real Example — AI/ML Project

`Pipfile`:

```toml
[packages]
fastapi = "*"
transformers = "*"
langchain = "*"
```

`pipenv graph` output:

```
langchain
├── pydantic
├── SQLAlchemy
├── aiohttp
└── langsmith

transformers
├── numpy
├── tokenizers
├── huggingface-hub
└── safetensors
```

This helps you understand why many packages got installed, detect conflicts, and track package size growth.

> In GenAI projects, dependency trees become huge because of `torch`, `transformers`, `langchain`, `chromadb`, `grpc`, and the `numpy` ecosystem. `pipenv graph` is extremely useful for debugging and optimizing Docker image size.

---

## Troubleshooting: Why `pipenv graph` Failed

`pipenv graph` only works when:
- A virtual environment exists
- Dependencies are installed

### Step 1 — Check Pipfile Requirement

```bash
cat Pipfile
```

Look for:

```toml
[requires]
python_version = "3.11"
```

### Step 2 — Install Correct Python Version

**Mac (using Homebrew):**

```bash
brew install python@3.11
python3.11 --version
```

### Step 3 — Create Virtual Environment Explicitly

```bash
pipenv --python 3.11
```

### Step 4 — Install Dependencies Without Locking First

```bash
PIPENV_SKIP_LOCK=1 pipenv install
```

This installs dependencies, skips lock generation, and avoids resolver failure initially.

### Step 5 — Verify Environment

```bash
pipenv shell
python --version
# Should show: Python 3.11.x
```

### Step 6 — View Dependency Tree

```bash
pipenv graph
```

### Step 7 — Generate Lock File Later

```bash
pipenv lock
```

---

## How Pipenv Selects Python

```
Pipfile requires 3.11
        ↓
Pipenv searches system
        ↓
Python 3.11 not found
        ↓
Environment creation fails
        ↓
No dependency graph available
```

---

## No Pipfile.lock? Here's What Happens

If you only have a `Pipfile` and no `Pipfile.lock`, Pipenv will:

1. Read dependencies from `Pipfile`
2. Resolve compatible versions
3. Create a new virtualenv
4. Generate a fresh `Pipfile.lock`

Installation currently fails during **step 2** (dependency resolution).

---

## Correct Way to Proceed (Full Walkthrough)

```bash
# Step 1 — Verify Python version requirement
cat Pipfile

# Step 2 — Install correct Python
brew install python@3.11

# Step 3 — Create virtual environment
pipenv --python 3.11

# Step 4 — Install without locking
PIPENV_SKIP_LOCK=1 pipenv install

# Step 5 — Activate and verify
pipenv shell
python --version   # Python 3.11.x

# Step 6 — View dependency tree
pipenv graph

# Step 7 — Generate lock file
pipenv lock
```

---

## Debugging Installation Failures

```bash
pipenv install --verbose
```

Look for lines like:

```
Cannot install X because Y depends on Z<2
```

### Common AI/ML Conflicts

```toml
tensorflow = "==2.4"
numpy = ">=2"       # ← conflict

fastapi = "<old version>"
pydantic = "<new version>"  # ← conflict
```

### Risky Dependency Examples

```toml
torch = "==1.7"
tensorflow = "==2.3"
numpy = "==2.0"
```

---

## Recommended Modern Setup (Mac)

| Tool            | Purpose                       |
|-----------------|-------------------------------|
| Homebrew        | Install Python                |
| pyenv / asdf    | Manage multiple Python versions |
| Pipenv/uv/Poetry | Dependency management        |

**Quick Fix Commands:**

```bash
brew install python@3.11
pipenv --python 3.11
pipenv install
pipenv graph
```

**Verify environment:**

```bash
pipenv --venv           # shows virtualenv path
pipenv run python --version   # should show Python 3.11.x
```

**If Pipenv gets corrupted:**

```bash
pipenv --rm     # remove old env
pipenv install  # recreate
```

---

## Pro Tips

- Always commit both `Pipfile` and `Pipfile.lock`
- Use `pyenv` or `asdf` to manage multiple Python versions across projects
- For AI/ML projects, `pipenv graph` is essential for understanding transitive dependencies
- Use `PIPENV_SKIP_LOCK=1` when debugging resolver failures
- Prefer `uv` or `Poetry` for greenfield projects in 2026
