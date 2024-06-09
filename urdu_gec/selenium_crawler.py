from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import html
import excel_write_incorrect as i2c
from urllib.parse import urljoin

total_text = ''
current_count = 41

def download_page(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Page downloaded successfully to {save_path}")
    else:
        print(f"Failed to download page. Status code: {response.status_code}")


def extract_hidden_content(input_tag):
    # Extract the HTML-encoded data from the 'data-hidden' attribute
    encoded_data = input_tag.get('data-hidden', '')
    # Decode the HTML-encoded data
    decoded_data = html.unescape(encoded_data)
    return decoded_data


def get_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the input tag with the hidden content
    input_tag = soup.find('input', {'type': 'hidden'})

    if input_tag:
        # Extract and decode the hidden content
        hidden_content = extract_hidden_content(input_tag)

        # Now, you can use BeautifulSoup to parse the hidden content
        hidden_soup = BeautifulSoup(hidden_content, 'html.parser')

        # Example: Extract and print the text content of the paragraphs
        paragraphs = hidden_soup.find_all('p')
        for paragraph in paragraphs:
            i2c.generate_data(paragraph.get_text())
    

def get_string_from_html(html_content):
    global total_text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the input tag with the hidden content
    input_tag = soup.find('input', {'type': 'hidden'})

    if input_tag:
        # Extract and decode the hidden content
        hidden_content = extract_hidden_content(input_tag)

        # Now, you can use BeautifulSoup to parse the hidden content
        hidden_soup = BeautifulSoup(hidden_content, 'html.parser')

        # Example: Extract and print the text content of the paragraphs
        paragraphs = hidden_soup.find_all('p')
        for paragraph in paragraphs:
            total_text += paragraph.get_text()

    

def crawl_dynamic_page(url, num_links=600):
    global current_count
    driver = webdriver.Chrome()  # You need to have ChromeDriver installed and in your PATH
    driver.get(url)

    try:
        # Scroll down to load more content
        for _ in range(num_links // 10):  # Assuming 10 links load with each scroll
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loading-spinner')))

        # Extract links after all content is loaded
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Example: Extract and print all the links on the page
        links = soup.find_all('a')
        counter = 0
        for link in links:
            if('/children-s-stories/children-s-story/' in link.get('href')):
                counter += 1
                if(counter <= current_count):
                    continue
                file_path = './html_files/'+str(counter)+'.html'
                page_link = urljoin('https://www.rekhta.org', link.get('href'))
                download_page(page_link, file_path)
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    get_content_from_html(html_content)
                

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

def num_repetition_word(html_paths):
    for file_path in html_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(file_path)
            html_content = file.read()
            get_string_from_html(html_content)


# Generate corrent and incorrect pairs and store them in output.csv:
url_to_crawl = 'https://www.rekhta.org/tags/children-s-story/children-s-stories?lang=ur'
crawl_dynamic_page(url_to_crawl, num_links=10000)

# code for getting common words from the corpus

# html_files = ['./html_files/'+file for file in os.listdir('./html_files') if file.endswith(".html")]
# num_repetition_word(html_files)

# common_words = {}
# total_words = total_text.split(' ')

# for word in total_words:
#     if(word not in list(common_words.keys())):
#         common_words[word] = 1
#     else:
#         common_words[word] += 1
# print('here')

# sorted_items = sorted(common_words.items(), key=lambda x: x[1], reverse=True)

# # Print the top 30 most common words
# for word, count in sorted_items[:30]:
#     print(f"{word}: {count}")
