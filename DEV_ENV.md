## Development environment — `uv` workflow

This project is not intended to publish a Python package to PyPI. The goal is a **fast, reproducible, low-friction dev setup** with:

- **Per-project virtual environment** for isolation and reproducibility.
- **Global-ish CLI tools** (formatters, linters, etc.) installed in isolated environments so they do not conflict with project dependencies.

We use [`uv`](https://github.com/astral-sh/uv) as the main tool for environments and dependency installation.

---

## 1. Install `uv`

On your local machine:

- **Windows (PowerShell)**:

  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

After installation, restart your terminal so `uv` is on your `PATH`, then verify:

```powershell
uv --version
```

---

## 2. Create and use the project virtual environment

From the project root (this repository directory):

```powershell
cd path\to\project_serendib

# Create a virtual environment in .venv (only needed once per machine)
uv venv .venv
```

Activate the environment:

- **PowerShell**:

  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

You should see the venv name (e.g. `(.venv)`) in your prompt. All subsequent commands assume the venv is activated.

---

## 3. Install project dependencies with `uv`

This repo currently tracks dependencies in `requirements.txt`. To install everything into the active virtual environment:

```powershell
uv pip install -r requirements.txt
```

This will install:

- **Runtime + tooling** for dataset work (e.g. `jsonschema`, `tqdm`).
- **Optional ecosystem libraries** used by training/eval workflows (`datasets`, `transformers`, `accelerate`, `peft`, `trl`).
- **OCR utilities** for working with the proposal (`pymupdf`, `pillow`, `pytesseract`).
- **Dev tools** (`pytest`, `ruff`).
- **Optional tools** like `argilla` and `gradio`.

> Note: `requirements.txt` is treated as the **single source of truth** for dependencies. We do **not** auto-generate it from a freeze so that we can keep comments and structure.

---

## 4. Adding or upgrading dependencies

When you need a new library:

1. **Edit `requirements.txt`** and add or update the version specifier in the appropriate section (runtime, optional, dev, etc.).
2. **Re-install using `uv`**:

   ```powershell
   uv pip install -r requirements.txt
   ```

`uv` will resolve and install any new or upgraded packages into the current virtual environment.

If you only want to install a single package temporarily for experimentation, you can also do:

```powershell
uv pip install some-package
```

but remember to add it to `requirements.txt` if it becomes a permanent dependency.

---

## 5. Global CLI tools vs project-local installs

Some tools listed in `requirements.txt` (for example `ruff`, `pytest`) can also be installed as **global developer CLIs** so you can use them across projects without version conflicts.

You have two good options:

### Option A — Use `uv tool` (recommended if you already use `uv`)

```powershell
uv tool install ruff
uv tool install black
uv tool install pre-commit
```

This installs each tool into its own isolated environment and exposes a global shim on your `PATH` (similar idea to `pnpm` for CLI apps).

### Option B — Use `pipx`

If you prefer `pipx`:

```powershell
python -m pip install --user pipx
pipx ensurepath

pipx install ruff
pipx install black
pipx install pre-commit
```

Either approach:

- Keeps **project dependencies** controlled by `requirements.txt` and the venv.
- Keeps **global dev tools** isolated from each other and from project code.

You can keep `ruff` / `pytest` in `requirements.txt` for CI or project-local usage even if you also install them globally.

---

## 6. Typical day-to-day usage

From a fresh clone on a new machine:

```powershell
cd path\to\project_serendib

# One-time (per machine)
uv venv .venv

# Every new terminal session
.\.venv\Scripts\Activate.ps1

# Install or refresh dependencies
uv pip install -r requirements.txt
```

After that you can run any project scripts, tests, and tools inside the activated venv.

---

## 7. CI / automation (high level)

In CI, a minimal install sequence looks like:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Then run tests or tooling (e.g. `pytest`, `ruff`) as needed.

This keeps the workflow:

- **Simple**: venv + requirements file.
- **Fast**: `uv` for installation and caching.
- **Reproducible**: same dependency set across machines.

