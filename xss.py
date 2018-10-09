from selenium import webdriver
from selenium.webdriver.common.by import By

profile = webdriver.FirefoxProfile('/home/fake_batman_/.mozilla/firefox/x2n55od1.default')
driver = webdriver.Firefox(firefox_profile=profile)
# url = 'http://testphp.vulnweb.com/'
url = 'https://www.woodlandworldwide.com/'
destination_url = 'https://www.woodlandworldwide.com/'
# url = 'http://prompt.ml/0'
driver.get(url)
html = driver.page_source
input_counter = 0
text_counter = 0
button_counter = 0
id_name_counter = 0
# [text, 'id', number]
list_of_input_tags = []
while True:
    if html.find('<input') != -1:
        input_tags = html[html.find('<input'): html.find('>', html.find('<input') + 1)]
        if input_tags.find("search") != -1 and input_tags.find("text") != -1:
            search_id = input_tags.find("name")
            search_text = input_tags[search_id:]
            id = search_text[search_text.find("\"") + 1:]
            id = id[:id.find("\"")]
            if id == '':
                id_name_counter = 1
            if id_name_counter == 1:
                search_id = input_tags.find("id")
                search_text = input_tags[search_id:]
                id = search_text[search_text.find("\"") + 1:]
                id = id[:id.find("\"")]
            list_of_input_tags.append([input_counter, 'search', id, button_counter])
            button_counter = 0
            text_counter += 1
            input_counter += 1
            print("Search field found...")
        elif input_tags.find("text") != -1:
            text_id = input_tags.find("name")
            field_text = input_tags[text_id:]
            id = field_text[field_text.find("\"") + 1:]
            id = id[:id.find("\"")]
            if id == '':
                id_name_counter = 1
            if id_name_counter == 1:
                search_id = input_tags.find("id")
                search_text = input_tags[search_id:]
                id = search_text[search_text.find("\"") + 1:]
                id = id[:id.find("\"")]
            list_of_input_tags.append([input_counter, 'text', id, button_counter])
            button_counter = 0
            text_counter += 1
            input_counter += 1
            print("Text field found...")
        elif input_tags.find("button") != -1 or input_tags.find("submit") != -1:
            button_id = input_tags.find("name")
            button_text = input_tags[button_id:]
            id = button_text[button_text.find("\"") + 1:]
            id = id[:id.find("\"")]
            if id == '':
                id_name_counter = 1
            if id_name_counter == 1:
                search_id = input_tags.find("id")
                search_text = input_tags[search_id:]
                id = search_text[search_text.find("\"") + 1:]
                id = id[:id.find("\"")]
            list_of_input_tags.append([input_counter, 'button', id, text_counter])
            button_counter += 1
            text_counter = 0
            input_counter += 1
            print("Button field found...")
        html = html[html.find('<input') + 1:]
    else:
        if input_counter == 0:
            print("No input fields found!")
        break
print(list_of_input_tags)
counter_www = 0
# TODO: Send payload using this input tags. Check on atleast three websites.
text_field_counter = 0
for input_tag in list_of_input_tags:
    if input_tag[1] == 'search' or input_tag[1] == 'text':
        id = input_tag[0]
        name = input_tag[2]
        if id_name_counter ==1:
            nameField = driver.find_element_by_id(name)
        else:
            nameField = driver.find_element_by_name(name)
        text_field_counter += 1
        if driver.current_url == destination_url and counter_www == 0:
            driver.find_element_by_xpath('/html/body/nav/div/form/div').click()
            counter_www = 1
        nameField.send_keys("hello")
    elif input_tag[1] == 'button':
        name = input_tag[2]
        if id_name_counter ==1:
            buttonField = driver.find_element_by_id(name)
        else:
            buttonField = driver.find_element_by_name(name)
        if text_field_counter == input_tag[3]:
            text_field_counter = 0
            buttonField.click()
            if driver.page_source.find("hello") != -1:
                print("The value has been reflected...")
                break
            else:
                driver.get(url)
        else:
            print("Wrong button please check...")


# TODO: Use automated all kind of scripts in the payload
# TODO: Implement spidering and go to other pages and implement the same
driver.close()
