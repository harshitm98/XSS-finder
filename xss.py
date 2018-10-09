from selenium import webdriver
from selenium.webdriver.common.by import By

profile = webdriver.FirefoxProfile('/home/fake_batman_/.mozilla/firefox/x2n55od1.default')
driver = webdriver.Firefox(firefox_profile=profile)
driver.get('http://testphp.vulnweb.com/')
# driver.get('https://www.woodlandworldwide.com/')
html = driver.page_source
input_counter = 0
# [text, 'id', number]
list_of_input_tags = []
while True:
    if html.find('<input') != -1:
        input_tags = html[html.find('<input'): html.find('>', html.find('<input') + 1)]
        if input_tags.find("search") != -1 and input_tags.find("text") != -1:
            input_counter += 1
            search_id = input_tags.find("name")
            search_text = input_tags[search_id:]
            id = search_text[search_text.find("\"") + 1:]
            id = id[:id.find("\"")]
            list_of_input_tags.append([input_counter, 'search', id])
            print("Search field found...")
        elif input_tags.find("text") != -1:
            input_counter += 1
            text_id = input_tags.find("name")
            field_text = input_tags[text_id:]
            id = field_text[field_text.find("\"") + 1:]
            id = id[:id.find("\"")]
            list_of_input_tags.append([input_counter, 'text', id])
            print("Text field found...")
        elif input_tags.find("button") != -1 or input_tags.find("submit") != -1:
            input_counter += 1
            button_id = input_tags.find("name")
            button_text = input_tags[button_id:]
            id = button_text[button_text.find("\"") + 1:]
            id = id[:id.find("\"")]
            list_of_input_tags.append([input_counter, 'button', id])
            print("Button field found...")
        html = html[html.find('<input') + 1:]
    else:
        if input_counter == 0:
            print("No input fields found!")
        break
print(list_of_input_tags)

driver.close()
