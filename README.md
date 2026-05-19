# LabWeb 🧪
LabWeb is a lightweight, ready-to-use Python interface library designed for small projects that prioritize fast development over extensive customization. It simulates the web development programing style, with separation of responsibilities and reusable components.

---

## 🚀 Features


---

## 🛠️ Installation & Development Setup

If you want to clone this repository to contribute to the code, run tests, or develop features locally, follow the steps below using **`uv`**, a fast Python package installer and environment manager.


### Windows

Open **PowerShell** and run:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternative:

```powershell
winget install astral-sh.uv
```

---

### Linux / macOS

Open a terminal and run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternative on macOS using Homebrew:

```bash
brew install uv
```

Alternative on Linux using pip:

```bash
pip install uv
```

After installation, restart your terminal so the `uv` command becomes available.

Verify installation:

```bash
uv --version
```

---

### Clone the Repository

Clone the project and enter its directory:

```bash
git clone https://github.com/your-username/labweb.git
cd labweb
```

---

### Install Dependencies & Create Environment

You do **not** need to manually create a virtual environment or run `pip install`.

Simply execute:

```bash
uv sync
```

This command automatically:

- Creates a local virtual environment (`.venv/`)
- Installs all project dependencies
- Installs LabWeb in editable mode
- Synchronizes dependencies from `pyproject.toml`

---

### Running the Project

Run your application inside the managed environment:

```bash
uv run <your_file>.py
```

This guarantees execution inside the project's environment and avoids dependency conflicts.

---

## 📂 Project Structure

```text
labweb/
├── pyproject.toml
├── README.md
└── src/
    └── labweb/
        ├── ...
```

---

## Example

A minimal interface example:

```python

```

---

## 📄 License

This project is licensed under the MIT License.

See the project files for additional details.