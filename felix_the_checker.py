import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

README_FILE = "README.md"
LINK_PATTERN = re.compile(r'<a href="([^"]*)">([🟩🟥])</a>')

def check_link_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)
        status_code = driver.execute_script("return document.readyState;")
        
        if status_code == "complete":
            return "🟩"
        else:
            return "🟥"
    except Exception:
        return "🟥"
    finally:
        driver.quit()

def check_link_status(url):
    if not url:
        return "🟥"

    return check_link_with_selenium(url)

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
