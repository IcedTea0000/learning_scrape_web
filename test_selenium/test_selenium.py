from selenium import webdriver

driver = webdriver.Chrome(executable_path='C:\workspace\drivers\chromedriver.exe')
driver.get('https://www.redfin.com/city/4001/TX/Cleveland')

html = driver.page_source
print(html)

# note: success test to get html from single-webpage