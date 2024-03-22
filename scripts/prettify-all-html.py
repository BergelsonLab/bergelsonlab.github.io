from pathlib import Path

from git import Repo
from bs4 import BeautifulSoup
import pyprojroot

# Find all non-ignored HTML-files in the repository
root_dir = pyprojroot.here()
repo = Repo(root_dir)
tracked_files = repo.git.ls_files().splitlines()
html_files = [f for f in tracked_files if f.endswith(".html")]


# Read, prettify, and write the HTML-files
errors = []
for file in html_files:
    path = Path(root_dir) / file
    try:
        with open(path, "r", encoding='utf-8') as f:
            soup = BeautifulSoup(f, "html.parser")
    except UnicodeDecodeError:
        errors.append(file)
        continue
    with open(path, "w", encoding='utf-8') as f:
        f.write(soup.prettify())
