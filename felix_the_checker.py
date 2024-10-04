import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

README_FILE = "README.md"
LINK_PATTERN = re.compile(r'<a href="([^"]*)">([🟩🟥])</a>')

def check_link_status(url):
    if not url:
        return "🟥"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)
        if driver.title:
            return "🟩"
        else:
            return "🟥"
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return "🟥"
    finally:
        driver.quit()

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
