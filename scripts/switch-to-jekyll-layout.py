"""
Switching to using Jekyll and not repeating HTML between pages

This script removes everything from the HTML-files except the main content and adds Jekyll front matter that specifies
the layout, title, and navigation group of the page. The layout is set to "default" for all files, the title is read
from the <title>, and the group is extracted by looking at which navigation item has the class "current".
"""
from pathlib import Path

from bs4 import BeautifulSoup
import pyprojroot

# Find all HTML files skipping certain folders
to_skip = ("_site",  #
           "_layouts",  # Layouts are not pages
           "images",  # Image pages use a different format
           "seedlings")  # The seedlings folder contains the old website, which has a different format


def path_in_folder(path: Path, folder: str, relative_to: Path) -> bool:
    """Check if the path is in the folder in the root directory."""
    return str(path.relative_to(relative_to)).startswith(folder)


root_dir = pyprojroot.here()
html_files = [path for path in root_dir.rglob('*.html')
              if not any(path_in_folder(path, folder, root_dir) for folder in to_skip)]

FRONT_MATTER = (
    "---\n"
    "layout: default\n"
    "title: {title}\n"
    "group: {group}\n"
    "---\n"
)
GROUPS = {'Home', 'Join Us', 'Media', 'News', 'People', 'Research'}

for path in html_files:
    try:
        with path.open("r", encoding='utf-8') as f:
            soup = BeautifulSoup(f, "html.parser")

        # Skip already processed files - they should contain the front matter at the top
        if soup.contents[0].lstrip().startswith("---"):
            continue

        # Find page group - the highlighted item in the navigation bar.
        # In <nav id="nav"> find <li class="current">. In it, read the text of the <a>-tag.
        group = soup.find("nav", id="nav").find("li", class_="current").find("a").text.strip()
        assert group in GROUPS, 'Unknown navigation group "{group}"'

        # Find page title - the text in the <title>-tag.
        title = soup.title.text.strip()

        # Find the contents inside the <div class="container" id="main">
        main_container = soup.find("div", class_="container", id="main")

    except Exception:
        print(f"Error processing {path}")
        break

    # Overwrite the file with the front matter and the main container
    with path.open("w", encoding='utf-8') as f:
        f.write(FRONT_MATTER.format(title=title, group=group))
        f.write(main_container.prettify())
