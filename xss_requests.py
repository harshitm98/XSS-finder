import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}

# url = 'http://testphp.vulnweb.com/'
url = 'https://www.woodlandworldwide.com/'
# url = 'http://prompt.ml/0'

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
result = session.get(url)
tree = html.fromstring(result.text)
html_page = result.text

input_counter = 0
text_counter = 0
button_counter = 0
id_name_counter = 0
# [text, 'id', number]
list_of_input_tags = []
while True:
    if html_page.find('<input') != -1:
        input_tags = html_page[html_page.find('<input'): html_page.find('>', html_page.find('<input') + 1)]
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
        elif input_tags.find("hidden") != -1:
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
            list_of_input_tags.append([input_counter, 'hidden', id, button_counter])
            button_counter = 0
            text_counter += 1
            input_counter += 1
            print("Hidden field found...")
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
        html_page = html_page[html_page.find('<input') + 1:]
    else:
        if input_counter == 0:
            print("No input fields found!")
        break
print(list_of_input_tags)
# TODO: Send payload using this input tags. Check on atleast three websites.
# text_field_counter = 0
# for input_tag in list_of_input_tags:


# TODO: Use automated all kind of scripts in the payload
# TODO: Implement spidering and go to other pages and implement the