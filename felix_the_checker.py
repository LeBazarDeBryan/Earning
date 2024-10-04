import requests
import re

README_FILE = "README.md"
LINK_PATTERN = re.compile(r'<a href="([^"]*)">([🟩🟥])</a>')

def check_link_status(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return "🟩"
        else:
            return "🟥"
    except requests.RequestException:
        return "🟥"

def update_readme():
    with open(README_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    updated_content = content

    for match in LINK_PATTERN.finditer(content):
        url, status = match.groups()
        if url:
            new_status = check_link_status(url)
            updated_content = updated_content.replace(f'<a href="{url}">{status}</a>', f'<a href="{url}">{new_status}</a>')

    if updated_content != content:
        with open(README_FILE, "w", encoding="utf-8") as file:
            file.write(updated_content)

if __name__ == "__main__":
    update_readme()
