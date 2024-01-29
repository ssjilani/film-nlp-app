from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
import logging
import re
from urls import urls
import csv


def set_drivers():
    chrome_options = Options()
    # Ensure GUI is off
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument('--no-sandbox')

    # Silent download of drivers
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    os.environ['WDM_LOG'] = 'False'

    # Create service

    webdriver_service = Service(ChromeDriverManager().install())

    # Create driver
    driver = webdriver.Chrome(service = webdriver_service, options = chrome_options)
    
    return driver
    
driver = set_drivers()
    

def mcu_scrape(transcript_link, driver, output_file):
    driver.get(transcript_link)

    film_name = transcript_link.split('/')[-2]

    content_divs = driver.find_elements(By.CLASS_NAME, 'mw-parser-output')

    # keep track of character line number
    dialogue_count = {}
    script = []
    script_a = []

    # Define a list of XPATH expressions to try
    xpath_list = ['.//p', './/li']

    for content_div in content_divs:
        lines = None  # Initialize lines to None

        # Iterate through the XPATH expressions
        for xpath_expression in xpath_list:
            lines = content_div.find_elements(By.XPATH, xpath_expression)

            # Check if the length of lines is greater than or equal to 50
            if len(lines) >= 100:
                break  # Break the loop if the condition is met

        # Check if any lines were found and the length is greater than or equal to 50
        if lines and len(lines) >= 100:
            for index, line in enumerate(lines):
                try:
                    character_element = line.find_element(By.XPATH, './/b')
                    character_name = character_element.text
                    dialogue = line.text.replace(character_name, '').strip()
                    dialogue = re.sub(r'\[.*?\]', '', dialogue)
                    dialogue = dialogue.strip()
                    dialogue = dialogue.replace(':', '')
                    character_name = character_name.replace(':', '')
                    character_name = re.sub(r'\[.*?\]', '', character_name)
                    character_name = character_name.strip()
                    

                    if character_name in dialogue_count:
                        dialogue_count[character_name] += 1
                    else:
                        dialogue_count[character_name] = 1
                    if len(dialogue) >= 2 and '\n' not in dialogue and len(character_name) <= 100:
                        script.append((character_name, dialogue, dialogue_count[character_name], film_name, transcript_link, 'MCU'))
                except NoSuchElementException:
                    # Split the line at ':' if <b> element is not found
                    split_line = line.text.split(': ', 1)
                    if len(split_line) == 2:
                        character_name = split_line[0].strip()
                        character_name = re.sub(r'\[.*?\]', '', character_name)
                        character_name = character_name.strip()
                        dialogue = split_line[1].strip()
                        dialogue = re.sub(r'\[.*?\]', '', dialogue)
                        dialogue = dialogue.strip()
                        dialogue = dialogue.replace(':', '')

                        if character_name in dialogue_count:
                            dialogue_count[character_name] += 1
                        else:
                            dialogue_count[character_name] = 1

                        if len(dialogue) >= 2 and '\n' not in dialogue and len(character_name) <= 100:
                            script_a.append((character_name, dialogue, dialogue_count[character_name], film_name, transcript_link, 'MCU'))
                    continue

    final_script = script_a if len(script_a) > len(script) else script

    # Write the header only once at the beginning of the file
    with open(output_file, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty
            csv_writer.writerow(['CharacterName', 'Dialogue', 'CharacterLineNumber', 'FilmName', 'URL', 'Franchise'])  # Write header
        csv_writer.writerows(final_script)

# Example usage
output_file = 'script_data.csv'
for url in urls:
    mcu_scrape(url, driver, output_file)


# Example usage
output_file = 'script_data.csv'
for url in urls:
    mcu_scrape(url, driver, output_file)
