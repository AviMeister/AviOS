from pathlib import Path


MAX_LINES = 150
PROJECT_ROOT = Path(__file__).parent.parent
SKIPPED_FOLDERS = {"venv", "__pycache__", ".ruff_cache", ".git"}


def should_check_file(file_path):
    return not any(folder in file_path.parts for folder in SKIPPED_FOLDERS)


def test_python_files_stay_under_150_lines():
    long_files = []

    for file_path in PROJECT_ROOT.rglob("*.py"):
        if not should_check_file(file_path):
            continue

        line_count = len(file_path.read_text(encoding="utf-8").splitlines())

        if line_count > MAX_LINES:
            long_files.append(f"{file_path.name}: {line_count} lines")

    assert long_files == []
