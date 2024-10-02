import requests
import re

README_PATH = 'README.md'

def check_link_status(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False

def update_readme(readme_path):
    with open(readme_path, 'r') as file:
        content = file.read()

    pattern = r'(<a href="(http[s]?://[^\"]+)">)(🟩|🟥)(</a>)'
    matches = re.findall(pattern, content)

    for match in matches:
        full_match, url, current_symbol, _ = match
        if check_link_status(url):
            new_symbol = "🟩"
        else:
            new_symbol = "🟥"

        content = content.replace(f'{full_match}{current_symbol}</a>', f'{full_match}{new_symbol}</a>')

    with open(readme_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    update_readme(README_PATH)
