import requests
import re

README_FILE = "README.md"

def check_link_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def update_readme():
    with open(README_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    link_pattern = re.compile(r'(\[.*?\]\((.*?)\))\s*(🟩|🟥)')
    
    updated_content = content
    for match in link_pattern.finditer(content):
        link_text, url, status_symbol = match.groups()
        is_link_accessible = check_link_status(url)

        if not is_link_accessible and status_symbol == "🟩":
            updated_content = updated_content.replace(f"{link_text} {status_symbol}", f"{link_text} 🟥")
        elif is_link_accessible and status_symbol == "🟥":
            updated_content = updated_content.replace(f"{link_text} {status_symbol}", f"{link_text} 🟩")

    with open(README_FILE, "w", encoding="utf-8") as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()
