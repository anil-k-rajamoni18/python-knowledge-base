# Python Build Tools & Dependency Management
## In-Depth Engineering Notes

> **Author's Note:** These notes are written from the perspective of a senior Python engineer and tutor. Every concept is explained with the *why*, not just the *what*. Read sequentially for full context, or jump to any section as a reference.

---

## Table of Contents

1. [Introduction to the Python Packaging Ecosystem](#1-introduction-to-the-python-packaging-ecosystem)
2. [Python Packaging Fundamentals](#2-python-packaging-fundamentals)
3. [The Python Build Tools Landscape](#3-the-python-build-tools-landscape)
4. [Pipenv — Complete Deep Dive](#4-pipenv--complete-deep-dive)
5. [Poetry — Complete Deep Dive](#5-poetry--complete-deep-dive)
6. [Pipenv vs Poetry — Detailed Comparison](#6-pipenv-vs-poetry--detailed-comparison)
7. [Python Dependency Security & Vulnerability Management](#7-python-dependency-security--vulnerability-management)
8. [Migration Guides](#8-migration-guides)
9. [Best Practices Cheat Sheet](#9-best-practices-cheat-sheet)

---

## 1. Introduction to the Python Packaging Ecosystem

### 1.1 Why Build Tools Exist

Python was designed to be simple and fast to write. But as projects grow from a single script to a team-maintained application with dozens of libraries, you face fundamental problems:

- **Reproducibility:** "It works on my machine" — but not on the server, not on your colleague's laptop, not in CI.
- **Isolation:** Library A requires `requests==2.28`, but Library B requires `requests>=2.30`. If you install globally, one of them breaks.
- **Transitive dependencies:** You install Flask. Flask installs Werkzeug, Jinja2, Click, MarkupSafe, itsdangerous. Now your project depends on 6 packages, not 1. Who manages them?
- **Publishing:** You wrote a reusable library. How do you package it so others can `pip install` it?
- **Security:** A vulnerability is found in `cryptography==38.0.0`. Which of your 100 projects use it, and how do you safely update it?

Build tools solve all of these — but different tools solve different subsets of these problems.

### 1.2 Problems They Solve

| Problem | Without Tools | With Tools |
|---|---|---|
| Dependency conflicts | Runtime `ImportError`, wrong version silently loaded | Explicit lock files, environment isolation |
| Reproducibility | `requirements.txt` without pins drifts over time | `Pipfile.lock` / `poetry.lock` pin exact hashes |
| Environment isolation | Global Python polluted with every project's deps | Per-project virtualenv, auto-managed |
| Publishing | Manual tar, upload to PyPI | `poetry build && poetry publish` |
| Security | Manual CVE hunting | `pip-audit`, `safety check`, `pipenv check` |
| Dev vs Prod deps | Everything in one flat `requirements.txt` | Separate groups for dev/test/prod |

### 1.3 Build vs Package vs Dependency Manager vs Environment Manager

These terms are often used interchangeably, but they mean different things:

```
┌────────────────────────────────────────────────────────────┐
│  Build Tool                                                │
│  Converts source code → distributable artifact             │
│  (setuptools, flit, hatchling, pdm-backend)                │
├────────────────────────────────────────────────────────────┤
│  Package Manager                                           │
│  Downloads & installs packages into an environment         │
│  (pip, uv)                                                 │
├────────────────────────────────────────────────────────────┤
│  Dependency Manager                                        │
│  Resolves, pins, and manages your project's dep graph      │
│  (pip-tools, Poetry resolver, Pipenv resolver)             │
├────────────────────────────────────────────────────────────┤
│  Environment Manager                                       │
│  Creates isolated Python environments                      │
│  (venv, virtualenv, conda, pyenv)                          │
└────────────────────────────────────────────────────────────┘
```

**Poetry and Pipenv are all-in-one tools** — they handle environment management, dependency management, and (Poetry) even packaging. This is why they're popular: fewer tools to learn.

### 1.4 Evolution of Python Packaging

```
1991  Python 1.0 — no packaging story whatsoever
2000  distutils added to stdlib — basic setup.py, bdist/sdist
2002  PyPI launched (the "Cheeseshop")
2004  setuptools created — extended distutils with egg format
2008  pip created — superior to easy_install (setuptools' installer)
2012  virtualenv becomes the de facto isolation tool
2013  wheel format (PEP 427) — binary distribution, replaces eggs
2014  venv added to stdlib (Python 3.3+) — lightweight virtualenv
2017  Pipenv released — combines pip + virtualenv + Pipfile
2018  Poetry released — full packaging + dependency management
2021  PEP 517/518 finalized — standardizes build backends
2022  PDM, Hatch mature; pip-tools widely adopted
2023  uv released by Astral — ultra-fast Rust-based pip replacement
2024  uv grows into full project manager (venv + pip + lock)
```

**Key insight:** Python packaging has been iteratively improved over 30 years. The ecosystem is now excellent, but has historical baggage that explains why multiple competing tools exist.

---

## 2. Python Packaging Fundamentals

### 2.1 pip — The Universal Package Installer

`pip` is Python's standard package installer, bundled with Python 3.4+. It downloads packages from PyPI (or any index) and installs them.

```bash
# Basic install
pip install requests

# Specific version
pip install "requests==2.31.0"

# Version range
pip install "requests>=2.28,<3.0"

# From git
pip install git+https://github.com/psf/requests.git@main

# From local path (editable install)
pip install -e .

# Install from requirements file
pip install -r requirements.txt

# Upgrade a package
pip install --upgrade requests

# Uninstall
pip uninstall requests

# Show installed packages
pip list
pip show requests

# Freeze current env to requirements
pip freeze > requirements.txt
```

**How pip installs packages:**
1. Contacts the package index (default: PyPI)
2. Fetches the package metadata (versions, dependencies)
3. Resolves the dependency tree
4. Downloads wheels (binary) or sdist (source)
5. Unpacks into `site-packages`

**pip's big weakness:** It installs into whichever Python environment is active. It does NOT create isolated environments. It does NOT lock transitive dependencies by default. That's why `venv` + `pip-tools` or higher-level tools are needed.

### 2.2 venv — Built-in Virtual Environments

`venv` (Python 3.3+, stdlib) creates lightweight isolated Python environments. Each virtual environment has its own:
- Python interpreter (symlinked)
- `pip` binary
- `site-packages` directory

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Deactivate
deactivate

# Create with specific Python version
python3.11 -m venv .venv

# Create without pip (bare env)
python -m venv .venv --without-pip

# See where venv is
which python  # (after activation)
# → /your/project/.venv/bin/python
```

**What `source activate` actually does:**
- Prepends `.venv/bin` to your `$PATH`
- Sets `$VIRTUAL_ENV` environment variable
- Updates shell prompt (optional: `--prompt`)

**venv vs virtualenv:**

| Feature | venv (stdlib) | virtualenv (third-party) |
|---|---|---|
| Installation | Built-in, no install needed | `pip install virtualenv` |
| Speed | Slower creation | Faster |
| Python version targeting | Limited | Full (via `--python`) |
| Seed packages | Only pip | pip, setuptools, wheel |
| Extendable | No | Yes (via seeds, activators) |

Use `venv` for simple cases. `virtualenv` when you need extra control (e.g., specifying exact Python patch versions).

### 2.3 setuptools — The Legacy Build System

`setuptools` is the dominant build backend for creating distributable Python packages. It reads your project metadata and source, then produces:
- **sdist** (source distribution): A tarball of your source code
- **wheel** (binary distribution): A pre-built `.whl` ZIP file

```python
# Classic setup.py (legacy but still widely seen)
from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="1.0.0",
    author="AK Developer",
    description="My awesome package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.28",
        "click>=8.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "mypy"],
        "docs": ["sphinx", "furo"],
    },
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "mycli=mypackage.cli:main",
        ],
    },
)
```

**Key insight:** `setup.py` is executable Python code — it runs on import. This is a security risk (installing a package runs arbitrary code). PEP 517/518 fixed this with declarative `pyproject.toml`.

### 2.4 wheel — Binary Distribution Format

A `.whl` file is a ZIP archive with a specific structure. It's the modern replacement for eggs.

```
mypackage-1.0.0-py3-none-any.whl
│             │    │    │    └── Platform tag (any = pure Python)
│             │    │    └──── ABI tag (none = no C extensions)
│             │    └──────── Python tag (py3 = Python 3.x)
│             └───────────── Version
└─────────────────────────── Package name
```

**Why wheels over sdist?**
- No build step at install time (no `setup.py` execution)
- Much faster installation
- No need for a compiler on the user's machine
- Deterministic: exact bytes, no build variation

**Platform-specific wheels** (for C extensions):
```
cryptography-41.0.0-cp311-cp311-manylinux_2_28_x86_64.whl
                    │     │     └── OS + arch (manylinux glibc 2.28, x86_64)
                    │     └──────── ABI (CPython 3.11 stable ABI)
                    └────────────── CPython 3.11
```

### 2.5 sdist — Source Distribution

An sdist is a tarball (`.tar.gz`) of your source + metadata. Used when:
- No wheel exists for the target platform
- You want the user to build from source
- You're distributing a pure-Python package and prefer source

```bash
# Build sdist using setuptools
python setup.py sdist           # Legacy
python -m build --sdist         # Modern (uses PEP 517)
```

### 2.6 requirements.txt

The most basic dependency specification format. A plain text file, one requirement per line.

```
# Pinned (exact version) - maximally reproducible
requests==2.31.0
urllib3==2.0.4
certifi==2023.7.22

# Loose (range) - flexible but drifts
requests>=2.28,<3.0

# With hash verification (most secure)
requests==2.31.0 \
    --hash=sha256:58cd2187423d2a947... \
    --hash=sha256:942c5a758f98d790... 

# From git
git+https://github.com/psf/requests.git@v2.31.0#egg=requests

# From local path
-e ./my-local-lib

# Include another requirements file
-r requirements-base.txt

# Constrain via constraints file
-c constraints.txt
```

**Generating requirements.txt properly:**
```bash
# Bad: only includes top-level (misses transitive deps)
echo "requests" > requirements.txt

# Good: freeze current env (captures everything)
pip freeze > requirements.txt

# Best: use pip-tools (separates intent from lock)
echo "requests" > requirements.in
pip-compile requirements.in  # generates pinned requirements.txt
```

### 2.7 constraints.txt

A constraints file applies version restrictions WITHOUT installing packages. Useful for enforcing org-wide dependency versions.

```bash
# constraints.txt
requests==2.31.0     # Constrain requests to exactly this version
urllib3<2.0          # Constrain urllib3 to <2.0 if it gets installed

# Usage
pip install -c constraints.txt mypackage
```

The difference: `requirements.txt` says "install these packages." `constraints.txt` says "if any of these get installed for any reason, use these versions."

### 2.8 setup.cfg — Declarative setuptools Config

A `.cfg` (INI-format) alternative to `setup.py`. Avoids executable code:

```ini
[metadata]
name = mypackage
version = attr: mypackage.__version__
author = AK Developer
description = My package
long_description = file: README.md
long_description_content_type = text/markdown
license = MIT
classifiers =
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.11

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.9
install_requires =
    requests>=2.28
    click>=8.0

[options.packages.find]
where = src

[options.extras_require]
dev =
    pytest>=7.0
    black
    mypy

[options.entry_points]
console_scripts =
    mycli = mypackage.cli:main
```

### 2.9 pyproject.toml — The Modern Standard

`pyproject.toml` is the unified configuration file for Python projects, now the de facto standard. It consolidates what used to be split across `setup.py`, `setup.cfg`, `MANIFEST.in`, `tox.ini`, `.flake8`, `mypy.ini`, etc.

```toml
# pyproject.toml

# --- Build system declaration (PEP 517/518) ---
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

# --- Project metadata (PEP 621) ---
[project]
name = "mypackage"
version = "1.0.0"
description = "My awesome package"
readme = "README.md"
license = {file = "LICENSE"}
authors = [{name = "AK", email = "ak@example.com"}]
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black", "mypy"]
docs = ["sphinx", "furo"]

[project.scripts]
mycli = "mypackage.cli:main"

[project.urls]
Homepage = "https://github.com/ak/mypackage"
Documentation = "https://mypackage.readthedocs.io"

# --- Tool-specific sections ---
[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.ruff]
select = ["E", "F", "I"]
```

### 2.10 PEPs Overview

Understanding key PEPs is essential for Python packaging literacy.

#### PEP 517 — A build-system independent format for source trees

**Problem:** Before PEP 517, `pip install` always ran `python setup.py ...`. This:
- Required setuptools even for non-setuptools projects
- Executed arbitrary code during install
- Made alternative build backends impossible

**Solution:** PEP 517 defines a standard interface (`build_wheel()`, `build_sdist()`) that any build backend must implement. pip now calls the backend's API, not `setup.py` directly.

```toml
# The [build-system] table is the PEP 517 declaration
[build-system]
requires = ["poetry-core"]       # what to install to run the backend
build-backend = "poetry.core.masonry.api"  # the backend API entrypoint
```

#### PEP 518 — Specifying Minimum Build System Requirements

**Problem:** How does pip know what to install to build a project before it can parse the project's own requirements?

**Solution:** `pyproject.toml` must exist and must have a `[build-system]` table with `requires`. pip installs those packages into a temporary build environment before building.

#### PEP 621 — Storing project metadata in pyproject.toml

Standardizes the `[project]` table in `pyproject.toml`. Before PEP 621, each build backend had its own way of specifying metadata. Now there's a single standard.

```toml
[project]                          # PEP 621 standard
name = "mypackage"
version = "1.0.0"
dependencies = ["requests>=2.28"]
```

#### PEP 660 — Editable installs via PEP 517

**Editable install:** Installing a package such that the source code IS the installed package — no copy to `site-packages`. Changes to source are immediately reflected without reinstalling.

```bash
pip install -e .          # Editable install
pip install --editable .  # Same thing
```

Before PEP 660: editable installs required `setup.py develop`, only worked with setuptools.
After PEP 660: any PEP 517 build backend can support editable installs via `build_editable()`.

---

## 3. The Python Build Tools Landscape

### 3.1 Quick Reference Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    Python Tools Ecosystem                       │
│                                                                 │
│  Simple Scripts    pip + venv          ──► you manage manually  │
│  App Development   Pipenv              ──► Pipfile + .lock      │
│  Library + App     Poetry              ──► pyproject.toml + .lock│
│  Modern/Fast       uv                  ──► drop-in pip upgrade  │
│  Data Science      Conda               ──► non-Python deps too  │
│  Enterprise/Mono   PDM or Hatch        ──► PEP-native, flexible │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 pip + venv (Baseline)

The foundation everything else builds on.

**When to use:** Simple scripts, learning Python, legacy projects, when you want zero magic.

**Workflow:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install flask sqlalchemy
pip freeze > requirements.txt
```

**Pain points:**
- No dependency resolution beyond "latest compatible"
- `pip freeze` captures EVERYTHING including dev tools
- Manually split dev/prod deps
- No lock file with hashes by default
- No environment auto-management

**Enhancement: pip-tools**

`pip-tools` is the missing piece between raw `pip` and full tools like Poetry:

```bash
pip install pip-tools

# requirements.in (abstract dependencies)
flask>=2.3
sqlalchemy>=2.0

# Compile to pinned lock
pip-compile requirements.in
# Produces requirements.txt with ALL transitive deps pinned + hashes

# Sync your environment
pip-sync requirements.txt

# Dev deps
# dev-requirements.in
-r requirements.txt
pytest
black

pip-compile dev-requirements.in -o dev-requirements.txt
```

### 3.3 Hatch

Hatch is a modern, PEP-native project manager from the PyPA (Python Packaging Authority).

```bash
pip install hatch

# New project
hatch new mypackage

# Run tests
hatch run test

# Build
hatch build

# Publish
hatch publish
```

**Key feature: environment matrix testing**
```toml
[tool.hatch.envs.test]
dependencies = ["pytest", "coverage"]

[[tool.hatch.envs.test.matrix]]
python = ["3.9", "3.10", "3.11", "3.12"]
```

**When to use:** Library development, tox replacement, projects needing matrix testing.

### 3.4 PDM (Python Dependency Manager)

PDM is a modern tool that follows all packaging standards (PEP 517, 518, 621, 660) strictly.

```bash
pip install pdm

# Initialize project
pdm init

# Add dependency
pdm add requests

# Add dev dependency
pdm add -dG dev pytest black

# Install
pdm install

# Run script
pdm run python app.py

# Build
pdm build
```

`pyproject.toml` with PDM:
```toml
[project]
name = "myapp"
dependencies = ["requests>=2.28"]

[tool.pdm.dev-dependencies]
dev = ["pytest", "black"]

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

**When to use:** When you want strict PEP compliance, no lock file surprises, and a clean alternative to Poetry.

### 3.5 uv — The Modern Fast Tool

`uv` is a Rust-based drop-in replacement for pip, pip-tools, and virtualenv. Built by Astral (same team as `ruff`). It is 10–100x faster than pip.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate environment
uv venv
source .venv/bin/activate

# Install packages (10-100x faster than pip)
uv pip install flask

# Sync from requirements
uv pip sync requirements.txt

# Compile lock file (like pip-compile)
uv pip compile requirements.in -o requirements.txt

# Run script with auto-managed environment
uv run python app.py

# Full project management (Poetry-like)
uv init myproject
uv add requests
uv add --dev pytest
uv lock
uv sync
```

**uv project workflow:**
```toml
# pyproject.toml managed by uv
[project]
name = "myapp"
version = "0.1.0"
dependencies = ["requests>=2.28"]

[dependency-groups]
dev = ["pytest>=7.0", "black"]
```

**When to use:** New projects, when speed matters (CI/CD), as a pip replacement in any existing project. uv is quickly becoming the recommended default.

**Benchmark:**
```
pip install django:          ~8 seconds
uv pip install django:       ~0.3 seconds  (26x faster)
```

### 3.6 Conda (Brief)

Conda is a cross-platform package and environment manager from Anaconda. Unlike pip, it manages non-Python packages (C libraries, CUDA, etc.).

```bash
# Create environment with specific Python
conda create -n myenv python=3.11

# Activate
conda activate myenv

# Install packages (from conda repos)
conda install numpy pandas scipy

# Install Python packages not on conda
conda install pip
pip install myspecialpackage

# Export environment
conda env export > environment.yml

# Recreate from file
conda env create -f environment.yml
```

**When to use:** Data science, ML/AI (GPU drivers, CUDA, MKL), scientific computing with complex C/Fortran dependencies (NumPy with BLAS, etc.).

**Why NOT for web development:** Slower, heavier, overkill for pure-Python web apps.

### 3.7 Build Backend vs Frontend

A key conceptual distinction:

**Build Frontend** (what the user runs):
- `pip install`, `pip build`, `uv pip install`, `build` (the `build` package)
- Talks to the backend via the PEP 517 interface
- Handles downloading, caching, environment bootstrapping

**Build Backend** (actually builds the package):
- `setuptools`, `flit-core`, `hatchling`, `poetry-core`, `pdm-backend`, `maturin`
- Implements `build_wheel()`, `build_sdist()`, `build_editable()`
- Declared in `pyproject.toml [build-system]`

```toml
[build-system]
# backend is installed by the frontend before building:
requires = ["hatchling"]
# frontend calls: hatchling.build.build_wheel(wheel_directory, ...)
build-backend = "hatchling.build"
```

---

## 4. Pipenv — Complete Deep Dive

### 4.1 What Is Pipenv?

Pipenv was created by Kenneth Reitz (author of the `requests` library) in 2017. It combines:
- **pip** for package installation
- **virtualenv** for environment isolation
- **Pipfile** (TOML-based) as the dependency spec
- **Pipfile.lock** for reproducible installs

**Core philosophy:** Developers specify *intent* (Pipfile). The lock file captures the resolved *reality* (Pipfile.lock). CI/CD installs from the lock file.

```
Developer workflow:
  pipenv install requests           → updates Pipfile + Pipfile.lock
  pipenv install --dev pytest       → updates Pipfile [dev-packages] + lock

CI/CD workflow:
  pipenv sync                       → installs exactly what's in Pipfile.lock
  pipenv sync --dev                 → includes dev deps too
```

### 4.2 Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Pipenv                                                 │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │   Pipfile    │    │ Pipfile.lock │                   │
│  │  (intent)    │    │   (reality)  │                   │
│  └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                           │
│         ▼                   ▼                           │
│  ┌──────────────────────────────────────────────┐      │
│  │           Resolver (pip-resolve)             │      │
│  │   Takes Pipfile deps + existing lock         │      │
│  │   Resolves full dependency tree              │      │
│  │   Produces new lock (with hashes)            │      │
│  └──────────────────┬───────────────────────────┘      │
│                     │                                   │
│                     ▼                                   │
│  ┌──────────────────────────────────────────────┐      │
│  │              virtualenv                      │      │
│  │   ~/.local/share/virtualenvs/project-hash/   │      │
│  └──────────────────────────────────────────────┘      │
│                     │                                   │
│                     ▼                                   │
│  ┌──────────────────────────────────────────────┐      │
│  │                  pip                         │      │
│  │   Installs packages into the virtualenv      │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

**Key design decision:** Pipenv stores virtualenvs OUTSIDE the project directory (by default). This is different from `.venv/` in the project root. Use `PIPENV_VENV_IN_PROJECT=1` to change this.

### 4.3 Installation

```bash
# Install Pipenv (use pipx for isolation)
pip install pipx
pipx install pipenv

# Or directly
pip install --user pipenv

# Verify
pipenv --version
# pipenv, version 2023.x.x
```

### 4.4 Core Files

#### Pipfile

The human-edited, TOML-formatted dependency specification:

```toml
# Pipfile

[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

# Optional: private registry
[[source]]
url = "https://my.nexus.internal/simple"
verify_ssl = true
name = "internal"

[packages]
# Production dependencies
flask = ">=2.3.0"
sqlalchemy = ">=2.0.0"
pydantic = ">=2.0"
celery = {version = ">=5.3", extras = ["redis"]}
requests = "*"             # any version (not recommended)
myinternallib = {version = ">=1.0", index = "internal"}

[dev-packages]
# Development-only dependencies
pytest = ">=7.0"
pytest-cov = "*"
black = "*"
mypy = "*"
ruff = "*"
ipdb = "*"

[requires]
python_version = "3.11"    # enforces Python version
# or: python_full_version = "3.11.5"
```

**Pipfile version specifiers:**

| Specifier | Meaning |
|---|---|
| `"*"` | Any version (avoid in production) |
| `">=2.0"` | At least 2.0 |
| `">=2.0,<3.0"` | 2.x range |
| `"~=2.3"` | Compatible release: >=2.3, <3.0 |
| `"==2.31.0"` | Exact version |

#### Pipfile.lock

Auto-generated. **NEVER edit manually.** Commit to version control.

```json
{
    "_meta": {
        "hash": {
            "sha256": "abc123..."
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.11"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "flask": {
            "hashes": [
                "sha256:2fb46f70...",
                "sha256:9a06....."
            ],
            "markers": "python_version >= '3.8'",
            "version": "==2.3.3"
        },
        "werkzeug": {
            "hashes": ["sha256:..."],
            "version": "==2.3.7"
        }
        // ... ALL transitive deps pinned with hashes
    },
    "develop": {
        "pytest": {
            "hashes": ["sha256:..."],
            "version": "==7.4.2"
        }
        // ...
    }
}
```

**Why hashes matter:** Hash verification ensures you get EXACTLY the file that was resolved. Without hashes, PyPI could serve a malicious package with the same version number. This is the supply chain attack defense.

### 4.5 Core Commands

```bash
# ── ENVIRONMENT SETUP ────────────────────────────────────────────

# Create/initialize Pipenv environment in current dir
pipenv install

# Install and activate with specific Python
pipenv --python 3.11

# Install from existing Pipfile.lock (exact, no resolution)
pipenv sync

# Install dev deps too
pipenv sync --dev

# ── ADDING/REMOVING PACKAGES ─────────────────────────────────────

# Install production dependency
pipenv install requests

# Install with version constraint
pipenv install "flask>=2.3"

# Install dev dependency
pipenv install --dev pytest black mypy

# Install package with extras
pipenv install "celery[redis]"

# Install from git
pipenv install "git+https://github.com/user/repo.git#egg=mypackage"

# Uninstall package
pipenv uninstall requests

# Uninstall all packages
pipenv uninstall --all

# ── ENVIRONMENT ACTIVATION ───────────────────────────────────────

# Spawn a shell inside the virtualenv
pipenv shell
# (to exit: exit or Ctrl+D)

# Run a command inside the virtualenv without activating shell
pipenv run python app.py
pipenv run pytest
pipenv run flask run

# ── LOCK FILE OPERATIONS ─────────────────────────────────────────

# Regenerate Pipfile.lock (full resolution)
pipenv lock

# Verify lock file is consistent with Pipfile
pipenv verify

# ── INSPECTION ───────────────────────────────────────────────────

# Show dependency graph
pipenv graph

# Show reverse dependency graph
pipenv graph --reverse

# Show where virtualenv is located
pipenv --venv

# Show Python interpreter being used
pipenv --py

# ── SECURITY ─────────────────────────────────────────────────────

# Check for known vulnerabilities
pipenv check

# ── CLEANUP ──────────────────────────────────────────────────────

# Remove packages not in Pipfile.lock
pipenv clean

# Remove the entire virtualenv
pipenv --rm

# ── UPDATES ──────────────────────────────────────────────────────

# Update a specific package (re-resolves)
pipenv update requests

# Update all packages
pipenv update

# Preview what would be updated (dry run)
pipenv update --dry-run
```

### 4.6 Dependency Resolution

Pipenv uses pip's resolver internally. When you run `pipenv install flask`:

1. Pipenv adds `flask = "*"` (or your specifier) to Pipfile
2. Starts pip's resolver with ALL current Pipfile constraints
3. Resolver builds a dependency graph:
   ```
   flask==2.3.3
   ├── Werkzeug>=2.3.7
   ├── Jinja2>=3.1.2
   │   └── MarkupSafe>=2.0
   ├── itsdangerous>=2.1.2
   └── click>=8.1.3
   ```
4. Checks for conflicts (if package A needs `click>=8.0` and package B needs `click<7.0`, conflict)
5. Selects the newest version satisfying all constraints
6. Downloads and verifies hashes
7. Writes resolved versions + hashes to Pipfile.lock

**SemVer and version pinning:**

```
flask = ">=2.3"     # Will resolve to latest 2.x or 3.x
flask = "~=2.3"     # Compatible release: >=2.3, <3.0 (safer!)
flask = "==2.3.3"   # Exact pin (very safe, can become stale)
```

**Conflict handling:**
```bash
# Pipenv will show conflict details:
# ERROR: flask 2.3.3 depends on Werkzeug>=2.3.7
# ERROR: myoldpackage 1.0 depends on Werkzeug<2.0
# Cannot resolve dependencies!

# Fix: upgrade myoldpackage, or find a compatible version
pipenv install "myoldpackage>=2.0"  # hope they fixed it
```

### 4.7 Virtual Environment Management

```bash
# Where does Pipenv store virtualenvs?
pipenv --venv
# Default: ~/.local/share/virtualenvs/myproject-AbCdEf12/
# (project name + hash of project path)

# Store venv INSIDE project (better for Docker, IDEs)
export PIPENV_VENV_IN_PROJECT=1
# Creates: ./project/.venv/

# Use specific Python interpreter
pipenv --python /usr/local/bin/python3.11

# Use pyenv-managed Python
pyenv local 3.11.5
pipenv install  # picks up .python-version

# Delete and recreate virtualenv
pipenv --rm
pipenv install

# Pipenv discovers virtualenv for you:
cd /path/to/project
pipenv run python  # automatically finds and uses the right venv
```

### 4.8 Dev vs Prod Dependencies — Best Practices

```toml
[packages]
# ONLY what runs in production
flask = ">=2.3"
sqlalchemy = ">=2.0"
pydantic = ">=2.0"
gunicorn = ">=21.0"

[dev-packages]
# Everything only needed locally / in CI
pytest = ">=7.0"
pytest-cov = "*"
pytest-asyncio = "*"
black = "*"
ruff = "*"
mypy = "*"
ipython = "*"
factory-boy = "*"     # test fixtures
responses = "*"       # HTTP mocking
```

**CI/CD patterns:**

```yaml
# GitHub Actions — Production install
- name: Install dependencies
  run: |
    pip install pipenv
    pipenv sync --bare   # no dev deps, exact from lock

# GitHub Actions — Test/CI install  
- name: Install all deps for testing
  run: |
    pip install pipenv
    pipenv sync --dev    # includes dev deps
    
- name: Run tests
  run: pipenv run pytest
```

```dockerfile
# Dockerfile — Production (no dev deps)
FROM python:3.11-slim

WORKDIR /app
COPY Pipfile Pipfile.lock ./

# Install pipenv, sync production deps, remove pipenv itself
RUN pip install pipenv \
    && pipenv sync --system --bare \
    && pip uninstall -y pipenv

COPY . .
CMD ["gunicorn", "app:app"]
```

### 4.9 Pipenv in Real Projects

**Flask Application:**
```bash
# Project setup
mkdir my-flask-api && cd my-flask-api
pipenv --python 3.11
pipenv install flask "flask-sqlalchemy>=3.0" "flask-migrate>=4.0" pydantic gunicorn
pipenv install --dev pytest pytest-cov black ruff mypy flask-testing

# Pipfile will look like:
# [packages]
# flask = "*"
# flask-sqlalchemy = ">=3.0"
# ... etc.

# Development
pipenv shell
flask run --debug

# OR without shell activation
pipenv run flask run
```

**FastAPI Application:**
```bash
mkdir my-fastapi && cd my-fastapi
pipenv --python 3.11
pipenv install "fastapi>=0.100" "uvicorn[standard]>=0.23" sqlalchemy pydantic-settings
pipenv install --dev pytest pytest-asyncio httpx black ruff mypy

# Run dev server
pipenv run uvicorn app.main:app --reload

# Makefile integration
# Makefile:
# run:
#     pipenv run uvicorn app.main:app --reload
# test:
#     pipenv run pytest -v
# lint:
#     pipenv run ruff check .
#     pipenv run black --check .
```

**Environment variables with Pipenv:**
```bash
# Pipenv auto-loads .env file!
# .env file:
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=my-secret-key-here
DEBUG=True

# .env is automatically loaded when using:
pipenv run python app.py
pipenv shell  # also loads it
```

### 4.10 Common Problems & Fix Strategies

#### Problem 1: Resolver hangs or is very slow

```bash
# Root cause: Pipenv's pip resolver tries ALL versions of ALL deps
# Fix 1: Set PIPENV_RESOLVER to use newer pip resolver
export PIPENV_RESOLVER=backtracking  # (now default in newer pipenv)

# Fix 2: Pre-constrain versions to narrow search space
pipenv install "flask==2.3.3"  # exact pin reduces resolution work

# Fix 3: Use PIPENV_TIMEOUT
export PIPENV_TIMEOUT=900  # seconds

# Fix 4: Update pipenv (resolver improved significantly in 2023+)
pip install --upgrade pipenv
```

#### Problem 2: Broken lock file

```bash
# Symptom: pipenv sync fails with hash mismatch or missing package

# Fix: Regenerate lock file from scratch
pipenv lock --clear         # clears pip cache first
# OR
pipenv install --skip-lock  # install without updating lock (temp)
# THEN
pipenv lock                 # regenerate fresh
```

#### Problem 3: Cross-platform issues

```bash
# Problem: Pipfile.lock generated on macOS won't work on Linux
# Root cause: Platform-specific wheels have different hashes

# Fix: Pipenv handles this via "markers" in lock file:
# "markers": "sys_platform == 'win32'"
# BUT only if you specify markers in Pipfile:

[packages]
pywin32 = {version = ">=306", markers = "sys_platform == 'win32'"}
uvloop = {version = ">=0.17", markers = "sys_platform != 'win32'"}
```

#### Problem 4: "No module named X" after activation

```bash
# Diagnose: verify you're in the right environment
pipenv run python -c "import sys; print(sys.path)"
pipenv --venv  # confirm venv path

# Check if package is actually installed
pipenv run pip list | grep requests

# Nuclear option: rebuild environment
pipenv --rm
pipenv install --dev
```

#### Problem 5: Pipenv conflicts with system Python or other tools

```bash
# Always use pipx to install Pipenv (isolated installation):
pipx install pipenv

# Check PATH isn't interfering
which pipenv
which python  # should point to venv when activated

# Ensure VIRTUAL_ENV is not set before creating new environment
unset VIRTUAL_ENV
pipenv install
```

---

## 5. Poetry — Complete Deep Dive

### 5.1 What Is Poetry?

Poetry (by Sébastien Eustace, 2018) is a complete Python dependency management and packaging tool. Unlike Pipenv, Poetry:
- Is also a **build backend** (via `poetry-core`)
- Can **publish packages to PyPI**
- Uses `pyproject.toml` as its single config file
- Has a faster, more robust dependency resolver
- Supports complex **dependency groups**

Poetry is the tool of choice for library development and professional applications.

### 5.2 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Poetry Architecture                                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  pyproject.toml                                     │   │
│  │  [tool.poetry]        ← project metadata           │   │
│  │  [tool.poetry.dependencies]  ← dep intent          │   │
│  │  [tool.poetry.group.dev.dependencies]              │   │
│  │  [build-system] → poetry-core                      │   │
│  └────────────────────────────┬────────────────────────┘   │
│                               │                             │
│                               ▼                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Poetry Resolver (PubGrub algorithm)                │   │
│  │  • Reads all constraints                            │   │
│  │  • Resolves full dep tree                           │   │
│  │  • Handles extras, markers, python version          │   │
│  └────────────────────────────┬────────────────────────┘   │
│                               │                             │
│                               ▼                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  poetry.lock  ← pinned full dep tree with hashes    │   │
│  └────────────────────────────┬────────────────────────┘   │
│                               │                             │
│                               ▼                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  .venv/ (or system venv path)                       │   │
│  │  Poetry installs packages into isolated venv        │   │
│  └─────────────────────────────────────────────────────┘   │
│                               │                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Build & Publish (poetry-core backend)              │   │
│  │  poetry build → .whl + .tar.gz                      │   │
│  │  poetry publish → push to PyPI or private registry  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**PubGrub Algorithm:** Poetry uses the PubGrub dependency resolution algorithm (also used by Dart's pub). It's a backtracking solver that finds solutions efficiently and gives clear error messages when conflicts exist. This is superior to pip's naive greedy resolver.

### 5.3 Installation

```bash
# Official installer (recommended — uses its own isolated environment)
curl -sSL https://install.python-poetry.org | python3 -

# macOS with Homebrew
brew install poetry

# via pipx (cleanest for developers)
pipx install poetry

# Verify
poetry --version
poetry self --version

# Enable shell completions (bash)
poetry completions bash >> ~/.bash_completion

# Update Poetry itself
poetry self update
```

### 5.4 pyproject.toml — Detailed Explanation

Poetry's `pyproject.toml` is the single source of truth for everything:

```toml
# pyproject.toml

# ─── BUILD SYSTEM ────────────────────────────────────────────────
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# ─── PROJECT METADATA ─────────────────────────────────────────────
[tool.poetry]
name = "my-fastapi-app"
version = "1.2.0"
description = "A production FastAPI application"
authors = ["AK <ak@gosprox.com>"]
maintainers = ["AK <ak@gosprox.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://gosprox.com"
repository = "https://github.com/sproxhrms/my-fastapi-app"
documentation = "https://docs.gosprox.com"
keywords = ["fastapi", "hrms", "saas"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Framework :: FastAPI",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
]
packages = [{include = "my_app", from = "src"}]
include = ["CHANGELOG.md"]
exclude = ["tests/", "docs/"]

# ─── PRODUCTION DEPENDENCIES ─────────────────────────────────────
[tool.poetry.dependencies]
python = ">=3.11,<4.0"
fastapi = ">=0.100.0"
uvicorn = {version = ">=0.23.0", extras = ["standard"]}
sqlalchemy = {version = ">=2.0.0", extras = ["asyncio"]}
pydantic = ">=2.0.0"
pydantic-settings = ">=2.0.0"
httpx = ">=0.25.0"
celery = {version = ">=5.3.0", extras = ["redis"]}
redis = ">=5.0.0"
alembic = ">=1.12.0"

# Optional dependencies (not installed by default)
sentry-sdk = {version = ">=1.30", optional = true}
prometheus-client = {version = ">=0.17", optional = true}

# ─── OPTIONAL EXTRAS (user-selectable) ───────────────────────────
[tool.poetry.extras]
monitoring = ["sentry-sdk", "prometheus-client"]
all = ["sentry-sdk", "prometheus-client"]

# ─── DEPENDENCY GROUPS (dev/test/etc.) ───────────────────────────
[tool.poetry.group.dev.dependencies]
black = ">=23.0"
ruff = ">=0.1.0"
mypy = ">=1.5"
ipython = ">=8.0"
ipdb = ">=0.13"

[tool.poetry.group.test.dependencies]
pytest = ">=7.4"
pytest-asyncio = ">=0.21"
pytest-cov = ">=4.1"
httpx = ">=0.25"          # for TestClient
factory-boy = ">=3.3"
respx = ">=0.20"          # async HTTP mocking

[tool.poetry.group.docs]
optional = true           # not installed by default
[tool.poetry.group.docs.dependencies]
mkdocs = ">=1.5"
mkdocs-material = ">=9.0"
mkdocstrings = {version = ">=0.23", extras = ["python"]}

# ─── SCRIPTS / CLI ENTRY POINTS ──────────────────────────────────
[tool.poetry.scripts]
myapp-cli = "my_app.cli:main"
myapp-worker = "my_app.worker:start"

# ─── PLUGINS ─────────────────────────────────────────────────────
[tool.poetry.plugins."poetry.application.plugin"]
my-plugin = "my_plugin.application:MyPlugin"

# ─── SOURCE REPOSITORIES ─────────────────────────────────────────
[[tool.poetry.source]]
name = "internal"
url = "https://nexus.internal/repository/pypi-proxy/simple/"
priority = "primary"       # check this first

[[tool.poetry.source]]
name = "PyPI"
priority = "supplemental"  # fallback to PyPI

# ─── TOOL CONFIGS ────────────────────────────────────────────────
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
select = ["E", "F", "I", "N", "W"]
line-length = 88

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "--cov=my_app --cov-report=term-missing"
```

### 5.5 poetry.lock — In Depth

```toml
# poetry.lock (excerpt — auto-generated, commit to git)

[[package]]
name = "fastapi"
version = "0.103.2"
description = "FastAPI framework, high performance, easy to learn, fast to code, ready for production"
optional = false
python-versions = ">=3.7"
files = [
    {file = "fastapi-0.103.2-py3-none-any.whl", hash = "sha256:3ef0573ab..."},
    {file = "fastapi-0.103.2.tar.gz", hash = "sha256:1a2b3c..."},
]

[package.dependencies]
pydantic = ">=1.7.4,<1.8 || >=1.8.2,<2.0.0 || >=2.0.1,<3.0.0"
starlette = ">=0.27.0,<0.28.0"
typing-extensions = ">=4.5.0"

[package.extras]
all = ["email-validator (>=2.0.0)", "httpx (>=0.23.0)", ...]

[[package]]
name = "starlette"
version = "0.27.0"
# ... (transitive dep, also fully pinned)
```

**Key facts about `poetry.lock`:**
- Contains ALL packages (direct + transitive) with exact versions AND hashes
- Poetry verifies hashes on install (supply chain security)
- The `[metadata]` section at the bottom captures content hashes for ALL packages
- It is safe to delete and regenerate with `poetry lock` (will re-resolve)
- Always commit to version control for applications (not libraries)
- Resolution logic: PubGrub backtracking SAT solver — faster and more predictable than pip's

### 5.6 Core Commands

```bash
# ── PROJECT INITIALIZATION ────────────────────────────────────────

# New project (scaffolds directory)
poetry new mypackage
# Creates:
# mypackage/
# ├── pyproject.toml
# ├── README.md
# ├── mypackage/
# │   └── __init__.py
# └── tests/
#     └── __init__.py

# Initialize in existing directory
cd existing-project
poetry init
# Interactive wizard, generates pyproject.toml

# ── DEPENDENCY MANAGEMENT ─────────────────────────────────────────

# Add production dependency
poetry add requests

# Add with version constraint
poetry add "fastapi>=0.100"

# Add with extras
poetry add "uvicorn[standard]"
poetry add "sqlalchemy[asyncio]"

# Add to a specific group
poetry add pytest --group test
poetry add black --group dev

# Add optional dependency
poetry add sentry-sdk --optional

# Remove dependency
poetry remove requests
poetry remove pytest --group test

# Update specific package
poetry update requests

# Update all packages (re-resolve, within pyproject.toml constraints)
poetry update

# Update and re-lock without installing
poetry lock --no-update   # re-lock keeping existing versions
poetry lock               # full re-resolution

# ── INSTALLATION ─────────────────────────────────────────────────

# Install all deps (from pyproject.toml, updates lock if needed)
poetry install

# Install including specific groups
poetry install --with test,docs

# Install ONLY production deps (exclude all groups)
poetry install --only main

# Install from lock file exactly (no resolution, for CI/CD)
poetry install --frozen  # or --no-update

# Sync: install lock file EXACTLY and remove extras
poetry install --sync

# Export to requirements.txt (for pip-based deployments)
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --with dev --output dev-requirements.txt
poetry export --without-hashes  # for simple use cases

# ── INSPECTION ────────────────────────────────────────────────────

# List installed packages
poetry show

# Show dependency tree
poetry show --tree

# Show specific package details + tree
poetry show fastapi --tree

# Check pyproject.toml for issues
poetry check

# Show outdated packages
poetry show --outdated

# ── ENVIRONMENT ────────────────────────────────────────────────────

# Run command in Poetry's virtualenv
poetry run python app.py
poetry run pytest
poetry run uvicorn main:app --reload

# Activate shell (like pipenv shell)
poetry shell

# Show venv info
poetry env info

# List all virtualenvs for this project
poetry env list

# Use specific Python version
poetry env use python3.11
poetry env use /usr/local/bin/python3.11

# Remove a virtualenv
poetry env remove python3.11

# ── PACKAGING ─────────────────────────────────────────────────────

# Build wheel + sdist
poetry build

# Publish to PyPI
poetry publish

# Publish to private registry
poetry publish --repository internal

# Build then publish in one step
poetry publish --build

# ── CONFIGURATION ─────────────────────────────────────────────────

# Configure virtualenvs to be in project directory
poetry config virtualenvs.in-project true

# Set PyPI token (store securely)
poetry config pypi-token.pypi your-token-here

# Add private repo credentials
poetry config http-basic.internal username password
```

### 5.7 Version Constraints — Complete Guide

```toml
[tool.poetry.dependencies]
# EXACT VERSION — maximally reproducible, must manually update
requests = "2.31.0"

# CARET CONSTRAINT (^) — allows compatible updates
# ^1.2.3  means >=1.2.3, <2.0.0  (safe: minor/patch upgrades)
# ^0.2.3  means >=0.2.3, <0.3.0  (when major is 0: patch only)
# ^0.0.3  means >=0.0.3, <0.0.4  (when major+minor are 0: exactly this)
requests = "^2.28.0"         # >=2.28.0, <3.0.0
pydantic = "^1.10"           # >=1.10.0, <2.0.0
pydantic = "^2.0"            # >=2.0.0, <3.0.0 (explicitly want v2)

# TILDE CONSTRAINT (~) — allows patch-level updates only
# ~1.2.3  means >=1.2.3, <1.3.0
# ~1.2    means >=1.2.0, <1.3.0
requests = "~2.31.0"         # >=2.31.0, <2.32.0

# WILDCARD — flexible, not recommended for production
requests = "2.*"             # >=2.0.0, <3.0.0
requests = "2.28.*"          # >=2.28.0, <2.29.0

# INEQUALITY RANGES
python = ">=3.9,<4.0"
django = ">=4.0,<5.0"

# MULTIPLE RANGES — complex compatibility
pydantic = ">=1.7.4,<1.8 || >=1.8.2,<2.0.0 || >=2.0.1,<3.0.0"

# PRERELEASE — opt into alpha/beta
numpy = {version = "^2.0.0", allow-prereleases = true}

# GIT DEPENDENCY
mylib = {git = "https://github.com/user/mylib.git", branch = "main"}
mylib = {git = "https://github.com/user/mylib.git", tag = "v1.2.0"}
mylib = {git = "https://github.com/user/mylib.git", rev = "abc1234"}

# LOCAL PATH DEPENDENCY
mysharedlib = {path = "../my-shared-lib", develop = true}

# URL DEPENDENCY
mypackage = {url = "https://example.com/mypackage-1.0.0-py3-none-any.whl"}

# PLATFORM-SPECIFIC
pywin32 = {version = ">=306", markers = "sys_platform == 'win32'"}
uvloop = {version = ">=0.17", markers = "sys_platform != 'win32'"}

# PYTHON VERSION-SPECIFIC
tomllib = {version = ">=2.0", python = "<3.11"}  # stdlib in 3.11+
```

**Recommended strategy:**
- Use `^` for most dependencies (safe, allows security patches)
- Use `>=X.Y` when downstream compatibility is most important
- Pin exact versions (`==X.Y.Z`) only when a specific version is known-good and you control updates via automation (Dependabot/Renovate)

### 5.8 Dependency Groups

```bash
# Define groups in pyproject.toml:
[tool.poetry.group.dev.dependencies]
black = "^23.0"
ruff = "^0.1"

[tool.poetry.group.test.dependencies]
pytest = "^7.4"
pytest-cov = "^4.1"

[tool.poetry.group.docs]
optional = true  # Not installed by default even with --with docs
[tool.poetry.group.docs.dependencies]
mkdocs = "^1.5"
```

```bash
# Install patterns:
poetry install                          # main + all non-optional groups
poetry install --with test              # + test group
poetry install --with test,docs         # + test and docs
poetry install --without dev            # skip dev group
poetry install --only main              # ONLY production (no groups)
poetry install --only test              # ONLY test group

# CI/CD pattern — minimal production install:
poetry install --only main --no-interaction

# Test CI pattern:
poetry install --with test --no-interaction
```

### 5.9 Packaging and Publishing

```bash
# ── BUILD ────────────────────────────────────────────────────────

# Build wheel and sdist
poetry build

# Output in dist/:
# dist/
# ├── my_app-1.2.0-py3-none-any.whl    (binary distribution)
# └── my-app-1.2.0.tar.gz              (source distribution)

# ── PUBLISH TO PyPI ───────────────────────────────────────────────

# Configure token (one time, stored in keyring)
poetry config pypi-token.pypi pypi-YOURTOKEN

# Publish
poetry publish --build   # build + publish in one step

# ── PRIVATE REGISTRIES ────────────────────────────────────────────

# Nexus / Artifactory / Azure Artifacts / AWS CodeArtifact

# 1. Add source to pyproject.toml:
[[tool.poetry.source]]
name = "internal-nexus"
url = "https://nexus.internal/repository/pypi-proxy/simple/"
priority = "primary"

# 2. Store credentials:
poetry config http-basic.internal-nexus username mytoken

# 3. Publish to internal:
poetry publish --repository internal-nexus

# ── VERSIONING ────────────────────────────────────────────────────

# Bump version (updates pyproject.toml)
poetry version patch    # 1.2.0 → 1.2.1
poetry version minor    # 1.2.0 → 1.3.0
poetry version major    # 1.2.0 → 2.0.0
poetry version prepatch # 1.2.0 → 1.2.1a0
poetry version prerelease # 1.2.0 → 1.3.0a0

# Show current version
poetry version
```

### 5.10 Scripts & CLI Apps

```toml
# pyproject.toml
[tool.poetry.scripts]
# name = "module.path:function"
myapp = "my_app.cli:app"
myapp-worker = "my_app.worker:main"
myapp-admin = "my_app.admin.cli:admin_app"
```

```python
# my_app/cli.py
import click

@click.group()
def app():
    """My Application CLI."""
    pass

@app.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8000, type=int)
def serve(host, port):
    """Start the application server."""
    import uvicorn
    uvicorn.run("my_app.main:app", host=host, port=port, reload=True)

@app.command()
def migrate():
    """Run database migrations."""
    from my_app.db import run_migrations
    run_migrations()
```

```bash
# After poetry install, the script is available:
poetry run myapp serve --port 9000
poetry run myapp migrate

# After pip install (e.g., production):
myapp serve
```

### 5.11 Monorepo & Enterprise Usage

```
my-platform/
├── pyproject.toml         ← root Poetry config (optional)
├── packages/
│   ├── shared-models/     ← shared data models library
│   │   └── pyproject.toml
│   ├── auth-service/      ← auth microservice
│   │   └── pyproject.toml
│   ├── hr-service/        ← HR microservice
│   │   └── pyproject.toml
│   └── api-gateway/       ← API gateway
│       └── pyproject.toml
```

**Internal shared library pattern:**
```toml
# packages/shared-models/pyproject.toml
[tool.poetry]
name = "my-shared-models"
version = "0.3.1"
packages = [{include = "shared_models"}]

# packages/hr-service/pyproject.toml
[tool.poetry.dependencies]
my-shared-models = {path = "../../packages/shared-models", develop = true}
```

**Publishing internal packages:**
```bash
# In packages/shared-models/:
poetry build
poetry publish --repository internal-nexus

# In packages/hr-service/pyproject.toml:
[[tool.poetry.source]]
name = "internal-nexus"
url = "https://nexus.internal/repository/pypi/simple/"
priority = "primary"

[tool.poetry.dependencies]
my-shared-models = "^0.3.0"  # installed from internal Nexus
```

### 5.12 Poetry in CI/CD

**GitHub Actions:**
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: latest
          virtualenvs-create: true
          virtualenvs-in-project: true   # stores venv in .venv/
      
      - name: Cache virtualenv
        uses: actions/cache@v3
        with:
          path: .venv
          key: ${{ runner.os }}-py${{ matrix.python-version }}-${{ hashFiles('poetry.lock') }}
      
      - name: Install dependencies
        run: poetry install --with test --no-interaction --frozen
      
      - name: Run tests
        run: poetry run pytest --cov --cov-report=xml
      
      - name: Lint
        run: |
          poetry run black --check .
          poetry run ruff check .
          poetry run mypy src/

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      - uses: snok/install-poetry@v1
      - name: Publish to PyPI
        run: poetry publish --build
        env:
          POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
```

**Dockerfile with Poetry:**
```dockerfile
FROM python:3.11-slim as builder

ENV POETRY_VERSION=1.7.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/poetry-cache

# Install Poetry in its own isolated venv
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${POETRY_VENV}/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install ONLY production deps, no dev
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --frozen

COPY src/ ./src/

# ── FINAL IMAGE ────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.13 Troubleshooting Poetry

```bash
# ── LOCK FILE CONFLICTS ────────────────────────────────────────────

# Problem: "Unable to find compatible versions"
# Diagnosis:
poetry show --tree        # see the tree
poetry why some-package   # why is it installed?

# Fix: Narrow the conflicting constraint, or
poetry add "package==specific.version"
# Then re-run poetry lock

# ── BROKEN CACHE ──────────────────────────────────────────────────

# Clear ALL Poetry caches
poetry cache clear --all pypi

# Clear specific cache
poetry cache clear pypi --all
poetry cache list         # show what's cached

# ── INCOMPATIBLE TRANSITIVE DEPS ─────────────────────────────────

# Find what requires the problematic dep
poetry show dep-name --tree

# Force a specific version of a transitive dep
# (add it directly, Poetry will constrain it)
poetry add "problematic-dep==1.2.3"

# ── MIGRATION FROM setup.py ────────────────────────────────────────

# Poetry can import from requirements.txt
poetry add $(cat requirements.txt | grep -v '#' | xargs)

# Or manually: run poetry init and add packages interactively

# ── DEBUGGING RESOLUTION ──────────────────────────────────────────

# Verbose output during install
poetry install -vvv

# Show what Poetry sees
poetry debug info
poetry debug resolve package-name
```

---

## 6. Pipenv vs Poetry — Detailed Comparison

### 6.1 Feature Comparison Table

| Feature | Pipenv | Poetry |
|---|---|---|
| **Primary Use Case** | Application development | Apps + Library development |
| **Config File** | `Pipfile` (TOML) | `pyproject.toml` (TOML) |
| **Lock File** | `Pipfile.lock` (JSON) | `poetry.lock` (TOML) |
| **Resolver Algorithm** | pip's resolver | PubGrub (faster, more accurate) |
| **Resolver Speed** | Slow (improving) | Fast |
| **Dependency Groups** | Dev vs Default | Unlimited named groups |
| **Build Backend** | No (uses pip) | Yes (poetry-core) |
| **Package Publishing** | No | Yes |
| **PyPI Publishing** | No | Yes |
| **Private Registries** | Yes (via source) | Yes (via source) |
| **Environment Auto-mgmt** | Yes | Yes |
| **venv Location** | `~/.local/share/virtualenvs/` (default) | `~/.cache/pypoetry/virtualenvs/` or `.venv/` |
| **Hash Verification** | Yes | Yes |
| **Extras Support** | Limited | Full |
| **Platform Markers** | Basic | Full |
| **Scripts/CLI** | Limited (`pipenv run`) | Full entry points |
| **Monorepo Support** | Weak | Moderate (path deps) |
| **Editable Installs** | Yes | Yes |
| **Enterprise Readiness** | Moderate | High |
| **CI/CD Experience** | Good | Excellent |
| **Learning Curve** | Low | Medium |
| **Maturity** | 2017, stable | 2018, very active |
| **Community** | Smaller (slowed) | Large, very active |
| **GitHub Stars** | ~24k | ~27k |
| **Security Scanning** | `pipenv check` | `pip-audit` (external) |
| **Migration Ease** | Medium | Medium |

### 6.2 Resolution Quality

```
Scenario: Package A needs requests>=2.28, Package B needs requests<2.29

Pipenv (pip resolver):
  → May install requests==2.28.x (correct)
  → Or fail with unhelpful error

Poetry (PubGrub):
  → Correctly finds requests==2.28.x
  → If impossible, gives clear explanation:
     "No versions of Package B are compatible with requests>=2.29"
```

### 6.3 Lock File Comparison

**Pipfile.lock (JSON):**
```json
{
    "default": {
        "flask": {
            "hashes": ["sha256:abc..."],
            "version": "==2.3.3"
        }
    }
}
```

**poetry.lock (TOML):**
```toml
[[package]]
name = "flask"
version = "2.3.3"
files = [
    {file = "flask-2.3.3-py3-none-any.whl", hash = "sha256:abc..."},
    {file = "flask-2.3.3.tar.gz", hash = "sha256:def..."},
]
[package.dependencies]
Werkzeug = ">=2.3.7"
```

Poetry's lock format is more informative — it captures the full dependency graph edges, not just version + hash.

### 6.4 When to Choose Each

**Choose Pipenv when:**
- Team is already using it and migration cost is high
- Project is a pure application (no library publishing)
- Team prefers simpler tooling with lower learning curve
- You want automatic `.env` loading (Pipenv does this natively)
- Working on legacy projects already using Pipfile

**Choose Poetry when:**
- Starting a new project (greenfield)
- You need to publish a package (library or internal package)
- You need fine-grained dependency groups (test, docs, etc.)
- Working with monorepos and internal package registries
- You want the best resolver (fewer conflicts, clearer errors)
- CI/CD caching and speed matter
- Long-term project with evolving dep graph

**Choose uv when:**
- Speed is the top priority (10-100x faster)
- You want a modern, actively developed tool
- Drop-in pip replacement (low migration cost)
- Building Docker images where install time matters

**Don't use either when:**
- Data science / ML: Use Conda or Conda + pip for complex binary deps
- Quick scripts: `venv` + `pip` is simpler and fine
- Already have a well-configured pip-tools setup: migration ROI may be low

---

## 7. Python Dependency Security & Vulnerability Management

> This is the most critical section for long-term project health. Treat dependency security as an ongoing operational concern, not a one-time checkbox.

### 7.1 Why Python Library Vulnerabilities Happen

#### Direct vs Transitive Dependencies

```
Your project
  └── requests==2.28.0          ← direct dependency (you chose it)
       └── urllib3==1.26.14     ← transitive (requests chose it)
            └── certifi==2022.9  ← transitive of transitive

A CVE is found in urllib3==1.26.14.
You never explicitly installed urllib3.
But your project IS vulnerable.
```

This is the #1 source of vulnerability blindness: **you only think about packages you explicitly chose**.

#### Supply Chain Attacks

Types of supply chain attacks in Python:

1. **Typosquatting:** Publishing `requets`, `reqeusts`, `request` to PyPI, hoping developers mistype
2. **Dependency confusion:** Publishing a public package with the same name as your internal package (pip prefers PyPI over internal by default — or did before explicit source configuration)
3. **Account takeover:** Attacker compromises a maintainer's PyPI account, publishes malicious version
4. **Malicious maintainer:** Package author intentionally introduces backdoor (`event-stream` npm incident — Python has had similar)
5. **Build poisoning:** Malicious code in `setup.py` executed during install

#### CVEs and Severity Scoring

**CVE (Common Vulnerabilities and Exposures):** A unique identifier for a publicly known vulnerability.
Format: `CVE-YEAR-NUMBER` (e.g., `CVE-2023-43804`)

**CVSS (Common Vulnerability Scoring System):** A numerical score 0-10 indicating severity:

| Score Range | Severity | Action |
|---|---|---|
| 9.0 - 10.0 | Critical | Fix immediately, within hours |
| 7.0 - 8.9 | High | Fix within 24-72 hours |
| 4.0 - 6.9 | Medium | Fix within next sprint |
| 0.1 - 3.9 | Low | Fix in scheduled maintenance |
| 0.0 | None | Informational |

**Reading a CVE:**
```
CVE-2023-43804 — urllib3 HTTP header injection

Severity: HIGH (7.5)
Affected: urllib3 < 1.26.17 and < 2.0.5
Fixed in: urllib3 == 1.26.17 or >= 2.0.5

Attack vector: Network
Attack complexity: Low
Privileges required: None
User interaction: None

Description: urllib3 does not strip the X-Forwarded-For header
when following redirects, which may lead to header injection.

Exploitability: The vulnerability can be triggered remotely
without authentication on HTTP requests that follow redirects.
```

### 7.2 Security Scanners — Hands-On

#### pip-audit (Recommended)

`pip-audit` queries the Python Advisory Database and OSV database:

```bash
# Install
pip install pip-audit
# or (isolated):
pipx install pip-audit

# Audit current environment
pip-audit

# Audit from requirements file
pip-audit -r requirements.txt

# Audit a specific package
pip-audit --package requests

# Output as JSON (for CI/CD integration)
pip-audit -o json -r requirements.txt > audit-report.json

# Fix automatically (upgrade to safe version)
pip-audit --fix

# Dry run fix (show what would be changed)
pip-audit --fix --dry-run

# Ignore specific vulnerability (with documented reason)
pip-audit --ignore-vuln PYSEC-2023-123

# Audit with Poetry
pip-audit --requirement <(poetry export -f requirements.txt)

# Audit with Pipenv
pip-audit --requirement <(pipenv requirements)

# Sample output:
# Found 2 known vulnerabilities in 2 packages
# Package       Version  ID                  Fix versions
# urllib3       1.26.12  PYSEC-2023-212      1.26.17, 2.0.5
# certifi       2022.9.24 PYSEC-2022-42987   2022.12.7
```

#### safety

```bash
# Install
pip install safety

# Scan environment
safety check

# Scan requirements file
safety check -r requirements.txt

# Output JSON
safety check -r requirements.txt --json > safety-report.json

# With Pipenv
pipenv check
# (pipenv check internally calls safety)

# Ignore specific vulnerability
safety check --ignore 12345

# Policy file (team-wide ignore list with documented reasons)
# .safety-policy.yml:
security:
  ignore-cvss-severity-below: 4.0   # ignore Low severity
  ignore-cvss-unknown-severity: false
  ignore-vulnerabilities:
    - id: 12345
      reason: "Only exploitable in web context, we use CLI mode"
      expires: "2024-03-01"

safety check --policy-file .safety-policy.yml
```

#### pipenv check

```bash
# Pipenv's built-in security check
pipenv check

# In CI:
pipenv check --output json > vuln-report.json

# pipenv check uses Safety's database under the hood
```

#### poetry audit (via plugin)

```bash
# Official Poetry security plugin
poetry self add poetry-audit-plugin

# Run audit
poetry audit

# Output formats
poetry audit --json
poetry audit --output-format json

# Ignore specific vulnerabilities
poetry audit --ignore-code PYSEC-2023-123
```

### 7.3 SCA (Software Composition Analysis) Tools

For enterprise-grade vulnerability management:

#### Snyk

```bash
# Install Snyk CLI
npm install -g snyk

# Authenticate
snyk auth

# Scan Python project
snyk test --file=requirements.txt
snyk test --file=Pipfile
snyk test --file=pyproject.toml

# Monitor (continuous scanning in Snyk dashboard)
snyk monitor

# Fix (shows upgrade recommendations)
snyk wizard
```

#### Dependabot (GitHub)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"         # or "daily"
    open-pull-requests-limit: 10
    groups:
      dev-dependencies:
        dependency-type: "development"
      production-dependencies:
        dependency-type: "production"
    ignore:
      - dependency-name: "some-package"
        versions: ["4.x"]        # ignore major version

  - package-ecosystem: "pip"
    directory: "/services/auth"  # monorepo: scan each service
    schedule:
      interval: "weekly"
```

Dependabot automatically opens PRs when vulnerabilities are found or new versions are available.

#### Renovate Bot (Alternative to Dependabot)

```json
// renovate.json
{
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchManagers": ["pip_requirements", "poetry"],
      "groupName": "python dependencies",
      "schedule": ["before 9am on monday"]
    },
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true         // auto-merge patch updates
    }
  ],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  }
}
```

#### Mend (formerly WhiteSource)

Enterprise SCA tool with:
- Continuous monitoring in CI/CD
- License compliance checking
- Fix PRs
- Policy enforcement
- Integration with Azure DevOps, GitHub, GitLab

### 7.4 Long-Term Vulnerability Management Strategy

This is the enterprise-grade approach for managing dependencies over a project's lifetime.

#### A. Versioning Strategy

**Layer 1: Abstract constraints (pyproject.toml / Pipfile)**
```toml
# Intentionally loose to allow security patches:
requests = "^2.28"           # allows 2.28.x → 2.31.x (security patches flow in)
cryptography = "^41.0"       # caret allows minor/patch upgrades

# NOT overly pinned:
requests = "==2.28.0"        # BAD: security patch 2.28.2 won't flow in
```

**Layer 2: Lock files (poetry.lock / Pipfile.lock)**
- Provides exact reproducibility
- Updated deliberately (not on every run)
- Governed by team process (reviewed in PRs)

**Controlled upgrade policy:**
```
Patch releases (1.x.Y): Update weekly, auto-approve if tests pass
Minor releases (1.Y.0):  Update monthly, require human review
Major releases (X.0.0):  Update quarterly, dedicated migration sprint
Security patches:         Update ASAP, SLA of 72h for Critical, 1 week for High
```

#### B. Dependency Hygiene

```bash
# 1. Remove unused libraries regularly
pip-extra list   # experimental: find unused imports

# Manual process:
# a) Check if package is used in code
grep -r "import requests" src/
# b) Remove if not found
poetry remove requests

# 2. Minimize dependency count
# Don't add a library for 3 lines of utility code you can write yourself

# 3. Review transitive deps
poetry show --tree
pip-audit --tree    # show vuln in context of who depends on it

# 4. Check license compatibility
pip-licenses --format=markdown   # list all licenses
pip-licenses --fail-on="GPL"     # fail if GPL dep found
```

#### C. Upgrade Strategy

```bash
# Weekly patch upgrades (Poetry):
poetry update    # re-resolve within current constraints

# Check what would update:
poetry show --outdated

# Monthly minor upgrades:
# 1. Update constraints in pyproject.toml
poetry add "fastapi>=0.104"

# 2. Run poetry update
poetry update

# 3. Run full test suite
pytest

# 4. Update lock file
# (done automatically by poetry update)

# 5. Create PR for team review
git add poetry.lock pyproject.toml
git commit -m "chore: update dependencies (monthly)"
```

#### D. CI/CD Security Gates

**GitHub Actions — Security gate:**
```yaml
name: Security Scan
on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 8 * * 1'   # Every Monday at 8am UTC

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install Poetry
        uses: snok/install-poetry@v1
      
      - name: Install dependencies
        run: poetry install --only main
      
      - name: Run pip-audit
        run: |
          pip install pip-audit
          poetry export -f requirements.txt | pip-audit \
            --requirement /dev/stdin \
            --output json \
            --strict \
            --vulnerability-service osv \
            > audit-results.json
          cat audit-results.json | python -c "
          import json, sys
          results = json.load(sys.stdin)
          vulns = results.get('vulnerabilities', [])
          critical_high = [v for v in vulns 
                          if v.get('severity', '') in ('CRITICAL', 'HIGH')]
          if critical_high:
              print(f'FAIL: {len(critical_high)} Critical/High vulnerabilities found')
              for v in critical_high:
                  print(f'  - {v[\"name\"]} {v[\"version\"]}: {v[\"id\"]}')
              sys.exit(1)
          print(f'PASS: {len(vulns)} total vulns, none Critical/High')
          "
      
      - name: Upload audit results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: audit-results
          path: audit-results.json
```

**Severity thresholds policy:**
```yaml
# security-policy.yml
thresholds:
  fail_on_critical: true      # CVSS >= 9.0: fail the build
  fail_on_high: true          # CVSS >= 7.0: fail the build
  fail_on_medium: false       # CVSS >= 4.0: warn only
  fail_on_low: false          # CVSS < 4.0: ignore

exceptions:
  - id: "PYSEC-2023-123"
    reason: "Only affects CLI mode, we use as library"
    approved_by: "security-team"
    expires: "2024-06-01"
```

#### E. Private Artifact Strategy

For enterprise environments, proxy/mirror PyPI through an internal artifact repository:

**Tools:** Nexus Repository, Artifactory, AWS CodeArtifact, Azure Artifacts, Devpi

**Benefits:**
- All packages cached internally (no PyPI outage impact)
- Only approved packages can be installed (allowlist)
- License compliance enforced at install time
- Audit trail of what was installed and when
- Internal packages published to same endpoint

```bash
# Poetry with internal Nexus:
[[tool.poetry.source]]
name = "nexus"
url = "https://nexus.internal/repository/pypi-proxy/simple/"
priority = "primary"

[[tool.poetry.source]]
name = "PyPI"
priority = "supplemental"   # only if not in Nexus

# Configure credentials
poetry config http-basic.nexus jenkins "$NEXUS_TOKEN"

# Package allowlist in Nexus: only approved packages can be downloaded
# Non-approved packages get 403 — build fails immediately
```

**Dependency confusion protection:**
```toml
# Tell Poetry to NEVER go to PyPI for internal packages
[[tool.poetry.source]]
name = "internal"
url = "https://nexus.internal/repository/pypi-private/simple/"
priority = "explicit"   # ONLY use this source for packages that request it

[tool.poetry.dependencies]
my-internal-lib = {version = "^1.0", source = "internal"}
```

#### F. Docker + Python Security

```dockerfile
# ── VULNERABLE: fat image, runs as root, outdated base ────────────
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# ── SECURE: slim, non-root, pinned base, no cache ─────────────────
FROM python:3.11.6-slim-bookworm          # ← pin exact image + OS version

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy lock file first for layer caching
COPY pyproject.toml poetry.lock ./

# Install Poetry + deps in one layer, clean up cache
RUN pip install poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi \
    && pip uninstall -y poetry \
    && pip cache purge \
    && rm -rf /root/.cache

# Copy source
COPY --chown=appuser:appuser src/ ./src/

# Switch to non-root user
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Image rebuild strategy:**
```yaml
# Scheduled rebuild workflow (rebuilds weekly even if no code changes)
# Picks up OS patches in the base image
name: Scheduled Image Rebuild
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday 6am

jobs:
  rebuild:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        run: |
          docker build --no-cache -t myapp:latest .
          docker push myapp:latest
```

**Scan Docker image for OS vulnerabilities:**
```bash
# Trivy — scans image for OS + Python vulns
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myapp:latest

# Grype
grype myapp:latest

# In CI:
- name: Scan image with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    format: sarif
    exit-code: 1            # fail on critical/high
    severity: HIGH,CRITICAL
```

### 7.5 Real-World Vulnerability Fix Workflow

**End-to-end example: CVE found in production**

```
Scanner flags: urllib3==1.26.12 → CVE-2023-43804 (HIGH, 7.5)
```

**Step 1: Identify the vulnerability**
```bash
pip-audit -r requirements.txt
# Output:
# urllib3  1.26.12  PYSEC-2023-212  1.26.17, 2.0.5
```

**Step 2: Identify the transitive dependency path**
```bash
poetry show urllib3 --tree
# urllib3 1.26.12
# ├── Dependent by: requests 2.28.2
# │   ├── Dependent by: httpx 0.24.1
# │   └── Dependent by: boto3 1.26.0
# └── Dependent by: botocore 1.29.0
```

So `urllib3` is a transitive dep of `requests`, `httpx`, and `boto3`.

**Step 3: Check the fix version**
```bash
# Fix: urllib3 >= 1.26.17 or >= 2.0.5
# Can requests 2.28.2 work with urllib3 1.26.17?
pip index versions urllib3    # see available versions
```

**Step 4: Upgrade safely**

*Option A: Update parent package (preferred)*
```bash
# If requests has already pinned urllib3 correctly in newer versions:
poetry update requests
# This will also pull in the safe urllib3 version
```

*Option B: Pin the transitive dep directly (override)*
```bash
# In pyproject.toml — add explicit constraint:
[tool.poetry.dependencies]
urllib3 = ">=1.26.17"   # force safe version

# Then lock and install:
poetry lock
poetry install
```

*Option C: For requirements.txt projects:*
```bash
# Add constraint to requirements.txt
urllib3>=1.26.17

# Or use constraints file:
echo "urllib3>=1.26.17" >> constraints.txt
pip install -c constraints.txt -r requirements.txt
```

**Step 5: Verify the fix**
```bash
# Confirm version is updated
pip show urllib3
# Version: 1.26.17

# Run audit again — should be clean
pip-audit -r requirements.txt
# No known vulnerabilities found

# Run full test suite
pytest -v
```

**Step 6: Re-lock**
```bash
# For Poetry:
poetry lock   # already done by poetry update
git add poetry.lock pyproject.toml

# For Pipenv:
pipenv lock
git add Pipfile.lock

# Commit with context:
git commit -m "fix(security): upgrade urllib3 to 1.26.17 (CVE-2023-43804)

CVE-2023-43804 (HIGH, CVSS 7.5) - HTTP header injection vulnerability.
urllib3 1.26.12 → 1.26.17 (transitive dep via requests, httpx)

Ref: https://github.com/advisories/GHSA-v845-jxx5-vc9f"
```

**Step 7: Deploy**
```bash
# Normal deployment pipeline:
# PR → CI (tests + audit pass) → merge → CD pipeline → staging → prod

# For Critical CVEs: expedited process
# PR → emergency approval → merge → hotfix release → prod
```

**Step 8: Monitor**
```bash
# Add to your monitoring:
# - pip-audit runs nightly in CI
# - Dependabot weekly scans
# - Snyk continuous monitoring dashboard
# - Alert on any new Critical/High vulnerability
```

### 7.6 Hands-On Vulnerability Fix Examples

**Fixing with Poetry:**
```bash
# 1. See all outdated/vulnerable packages
poetry show --outdated
pip-audit --requirement <(poetry export -f requirements.txt)

# 2. Fix specific package
poetry add "cryptography>=41.0.5"   # to address CVE in 41.0.0-4

# 3. Or update all within constraints
poetry update cryptography

# 4. Verify
poetry run pip show cryptography
# Version: 41.0.5

# 5. Lock and commit
git add poetry.lock
git commit -m "fix(security): upgrade cryptography (CVE-2023-49083)"
```

**Fixing with Pipenv:**
```bash
# 1. Check
pipenv check

# 2. Update specific package
pipenv update cryptography

# 3. Or if it's a transitive dep, pin it explicitly:
# In Pipfile:
[packages]
cryptography = ">=41.0.5"

# 4. Re-lock
pipenv lock

# 5. Sync environment
pipenv sync

# 6. Verify and commit
git add Pipfile Pipfile.lock
git commit -m "fix(security): pin cryptography to >=41.0.5 (CVE-2023-49083)"
```

**Fixing in requirements.txt:**
```bash
# 1. Audit
pip-audit -r requirements.txt

# 2. Update requirements.txt
# Old: cryptography==41.0.0
# New: cryptography==41.0.5

# Or regenerate with pip-tools:
# requirements.in: cryptography>=41.0.5
pip-compile requirements.in

# 3. Reinstall
pip install -r requirements.txt

# 4. Verify
pip show cryptography

# 5. Commit
git add requirements.txt
git commit -m "fix(security): upgrade cryptography to 41.0.5"
```

**Fixing a transitive dep that won't upgrade:**
```bash
# Problem: packageA==2.0 requires vulnerable_lib==1.0 (no fix available)
# Resolution options:

# Option 1: Upgrade packageA (hope newer version fixes dep)
poetry update packageA

# Option 2: Find alternative
poetry remove packageA
poetry add betterAlternative   # does the same thing, safer deps

# Option 3: Fork and patch (nuclear option)
# Fork the repo, apply CVE patch, publish to internal Nexus
# Use internal version in pyproject.toml:
packageA = {version = "^2.0.1", source = "internal-patched"}

# Option 4: Accept risk + document
# If it's truly unexploitable in your context:
# Add to .safety-policy.yml or pip-audit ignore list WITH documented reason
```

---

## 8. Migration Guides

### 8.1 pip + requirements.txt → Pipenv

```bash
# Step 1: Install Pipenv
pipx install pipenv

# Step 2: Initialize (reads requirements.txt if present)
cd my-project
pipenv install -r requirements.txt

# Step 3: Move dev deps
pipenv install --dev -r dev-requirements.txt

# Step 4: Verify
pipenv graph
pipenv run python -c "import flask; print(flask.__version__)"

# Step 5: Commit new files, remove old
git add Pipfile Pipfile.lock
git rm requirements.txt dev-requirements.txt  # if you want clean break
# OR keep requirements.txt as export:
# pipenv requirements > requirements.txt  (keep for backward compat)
git commit -m "chore: migrate to Pipenv from pip+requirements.txt"

# Step 6: Update .gitignore
echo ".venv" >> .gitignore  # if using PIPENV_VENV_IN_PROJECT=1
```

### 8.2 pip + requirements.txt → Poetry

```bash
# Step 1: Install Poetry
pipx install poetry

# Step 2: Initialize (interactive wizard)
cd my-project
poetry init

# Step 3: Add dependencies from requirements.txt
cat requirements.txt | grep -v "^#" | grep -v "^-" | while read dep; do
    poetry add "$dep"
done

# Step 4: Add dev deps
cat dev-requirements.txt | grep -v "^#" | while read dep; do
    poetry add --group dev "$dep"
done

# Step 5: Verify
poetry show --tree
poetry run pytest

# Step 6: Commit
git add pyproject.toml poetry.lock
git commit -m "chore: migrate to Poetry"
```

### 8.3 Pipenv → Poetry

```bash
# Step 1: Export current Pipfile.lock to requirements format
pipenv requirements > requirements.txt
pipenv requirements --dev > dev-requirements.txt

# Step 2: Initialize Poetry
poetry init

# Step 3: Add dependencies
# Read Pipfile for version constraints (don't use the frozen lock versions)
cat Pipfile   # note your [packages] and [dev-packages]
poetry add flask "sqlalchemy>=2.0" pydantic   # add main deps
poetry add --group dev pytest black mypy       # add dev deps

# Step 4: Test
poetry install
poetry run pytest

# Step 5: Clean up
git add pyproject.toml poetry.lock
git rm Pipfile Pipfile.lock
git commit -m "chore: migrate from Pipenv to Poetry"

# Step 6: Update CI/CD
# Replace: pipenv sync && pipenv run pytest
# With:    poetry install && poetry run pytest
```

### 8.4 Legacy setup.py → pyproject.toml

```python
# OLD: setup.py
from setuptools import setup, find_packages
setup(
    name="mypackage",
    version="1.0.0",
    install_requires=["requests>=2.28", "click>=8.0"],
    extras_require={"dev": ["pytest"]},
    entry_points={"console_scripts": ["mycli=mypackage.cli:main"]},
)
```

```toml
# NEW: pyproject.toml (using Poetry)
[tool.poetry]
name = "mypackage"
version = "1.0.0"

[tool.poetry.dependencies]
python = ">=3.9"
requests = ">=2.28"
click = ">=8.0"

[tool.poetry.group.dev.dependencies]
pytest = ">=7.0"

[tool.poetry.scripts]
mycli = "mypackage.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

```bash
# Verify the migration:
poetry build   # should produce dist/*.whl and dist/*.tar.gz
pip install dist/mypackage-1.0.0-py3-none-any.whl
mycli --help   # entry point should work
```

---

## 9. Best Practices Cheat Sheet

### 9.1 Do's

```
✅ Always commit lock files (Pipfile.lock / poetry.lock) to version control
✅ Use specific version constraints (^, ~=, >=X.Y) in pyproject.toml / Pipfile
   NOT wild pins (==X.Y.Z) for direct deps — those prevent security patches
✅ Separate dev, test, and production dependencies
✅ Run security scans in CI on every PR
✅ Set severity thresholds: fail on Critical/High
✅ Use virtualenvs always, even for personal projects
✅ Pin your Python version (in pyproject.toml or .python-version)
✅ Use `poetry install --frozen` or `pipenv sync` in CI (no re-resolution)
✅ Use `--only main` (Poetry) or `--bare` (Pipenv) for production Docker builds
✅ Store virtualenvs in-project (.venv/) for reproducible Docker builds
✅ Use Dependabot or Renovate for automated dependency PR creation
✅ Document WHY you're ignoring a vulnerability (expire date, reason, approver)
✅ Rebuild Docker images weekly to pick up OS patches
✅ Regularly prune unused dependencies (every quarter)
✅ Use private artifact repository (Nexus/Artifactory) in enterprise
✅ Add hash verification to any requirements.txt used in production
✅ Use pipx to install CLI tools (pipenv, poetry, pip-audit) — keeps them isolated
```

### 9.2 Don'ts

```
❌ Don't use `pip install` globally (outside a virtualenv) for project deps
❌ Don't commit virtualenv directories (.venv/, venv/) to git
❌ Don't ignore lock file merge conflicts — resolve them deliberately
❌ Don't pin transitive deps without documenting why
❌ Don't silence all vulnerability warnings without review
❌ Don't run containers as root (use USER nonroot in Dockerfile)
❌ Don't use FROM python:3.11 (no pin) in production — use python:3.11.6-slim-bookworm
❌ Don't skip the test suite when doing security upgrades
❌ Don't use `pip freeze > requirements.txt` as your primary dep management
   (captures dev tools, no grouping, no intent separation)
❌ Don't put secrets (.env files with real values) in version control
❌ Don't have thousands of transitive deps — regularly audit with `poetry show --tree`
```

### 9.3 Enterprise Recommendations

```
1. Standardize on ONE tool per team (Poetry recommended for new projects)
2. Mandate lock file governance: all lock file changes require PR review
3. Run pip-audit/Snyk in CI as a blocking quality gate
4. Implement Dependabot/Renovate for automated PRs
5. Use internal Nexus/Artifactory — proxy PyPI, enforce allowlists
6. Define SLAs: Critical CVE = 72h, High = 7 days, Medium = next sprint
7. Document the dependency update process in team runbooks
8. Keep a security exceptions register with expiry dates
9. Regular (quarterly) dependency audits: remove unused, upgrade majors
10. Scan Docker images with Trivy/Grype in CI before pushing to registry
```

### 9.4 Command Cheat Sheet

```bash
# ── PIPENV ──────────────────────────────────────────────────────────
pipenv install                    # Install from Pipfile
pipenv install requests           # Add + install package
pipenv install --dev pytest       # Add dev package
pipenv sync                       # Install EXACTLY from lock (CI/CD)
pipenv sync --dev                 # Include dev deps
pipenv shell                      # Activate venv
pipenv run pytest                 # Run without activating
pipenv lock                       # Regenerate lock file
pipenv update requests            # Update specific package
pipenv update                     # Update all packages
pipenv graph                      # Show dependency tree
pipenv check                      # Security scan
pipenv --venv                     # Show venv path
pipenv --rm                       # Delete venv

# ── POETRY ──────────────────────────────────────────────────────────
poetry new myproject              # Create new project
poetry init                       # Initialize in existing dir
poetry install                    # Install from pyproject.toml
poetry install --only main        # Production only (no dev groups)
poetry install --with test        # Include test group
poetry install --frozen           # Exact from lock (CI/CD)
poetry add requests               # Add package
poetry add pytest --group test    # Add to test group
poetry remove requests            # Remove package
poetry update                     # Update all (within constraints)
poetry update requests            # Update specific package
poetry lock                       # Re-resolve and update lock
poetry show --tree                # Show dependency tree
poetry show --outdated            # Show outdated packages
poetry run pytest                 # Run in venv
poetry shell                      # Activate venv
poetry build                      # Build wheel + sdist
poetry publish                    # Publish to PyPI
poetry env info                   # Show environment info
poetry cache clear --all pypi     # Clear cache
poetry export -f requirements.txt # Export to requirements.txt

# ── SECURITY ────────────────────────────────────────────────────────
pip-audit                         # Audit current environment
pip-audit -r requirements.txt     # Audit requirements file
pip-audit --fix                   # Auto-fix (upgrade to safe versions)
pip-audit --output json           # JSON output for CI
safety check                      # Safety DB scan
safety check -r requirements.txt  # Scan requirements file
pipenv check                      # Pipenv security check
poetry audit                      # Poetry audit plugin

# Export for auditing:
poetry export -f requirements.txt | pip-audit -r /dev/stdin
pipenv requirements | pip-audit -r /dev/stdin

# ── UV (FAST MODERN ALTERNATIVE) ────────────────────────────────────
uv venv                           # Create .venv
uv pip install flask              # Install (10-100x faster than pip)
uv pip sync requirements.txt      # Sync from file
uv pip compile requirements.in    # Compile lock
uv add requests                   # Add to project (Poetry-like)
uv run pytest                     # Run in venv
```

### 9.5 Interview Questions

**Conceptual:**
1. What's the difference between a virtual environment and a Docker container for Python isolation?
2. Explain the difference between `Pipfile` and `Pipfile.lock`. Why do we need both?
3. What is PEP 517 and why was it important for Python packaging?
4. What is a transitive dependency and why does it matter for security?
5. Explain hash verification in lock files — what attack does it prevent?
6. What is the PubGrub algorithm and why is it superior to greedy resolution?

**Practical:**
7. How would you structure dependencies for a FastAPI app with dev, test, and production separation using Poetry?
8. A colleague reports "works on my machine" but CI fails. What's your first debugging step?
9. A CVE is found in a transitive dependency. Walk me through your fix process.
10. What's your strategy for keeping dependencies up to date across 50 microservices?
11. How do you handle platform-specific dependencies (Windows vs Linux) in poetry.lock?
12. Explain the difference between `poetry install` and `poetry install --frozen`.

**Security-focused:**
13. What is a supply chain attack? Give 3 Python-specific examples.
14. How does a private artifact repository (Nexus) improve dependency security?
15. What CVSS score threshold would you use to fail a CI/CD build? Why?
16. Explain dependency confusion attacks and how to prevent them.
17. How would you implement automated vulnerability management for a team of 20 developers?

---

*These notes were compiled for engineering excellence. For the latest tool versions and CVE databases, always check the official documentation: [pip-audit](https://github.com/pypa/pip-audit), [Poetry](https://python-poetry.org/docs/), [Pipenv](https://pipenv.pypa.io/).*
