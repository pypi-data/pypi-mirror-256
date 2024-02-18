def dl(url: str):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    browser = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    target_path = "test.html"
    with open (target_path, "w") as file:
        file.write(soup.prettify())
    print(soup.prettify())

if __name__ == "__main__":
    import sys
    if sys.argv is None or len(sys.argv) < 2:
        print("No url given")
        sys.exit()
    url = sys.argv[1]
    dl(url)

