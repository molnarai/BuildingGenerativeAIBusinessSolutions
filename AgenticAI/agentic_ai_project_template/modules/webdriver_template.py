from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://example.com")

# Perform actions
search_box = driver.find_element("name", "q")
search_box.send_keys("Agentic AI Systems")
search_box.submit()

driver.quit()