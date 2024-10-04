import requests
import re

README_FILE = "README.md"
LINK_PATTERN = re.compile(r'<a href="([^"]*)">([🟩🟥])</a>')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def check_link_status(url):
    if not url:
        return "🟥"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True, verify=False)
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
        new_status = check_link_status(url)
        if new_status != status:
            updated_content = updated_content.replace(f'<a href="{url}">{status}</a>', f'<a href="{url}">{new_status}</a>')

    if updated_content != content:
        with open(README_FILE, "w", encoding="utf-8") as file:
            file.write(updated_content)
        print("README.md updated.")
    else:
        print("No updates needed.")

if __name__ == "__main__":
    update_readme()
