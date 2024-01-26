import requests
from bs4 import BeautifulSoup
import re


def extract_script_data(url):

    def clean_dialogue(dialogue):
    # Remove double quotes from the dialogue
        dialogue = dialogue.replace( "'", '')
        
        # Remove words from the end until a word that ends with '?', '!', or '.'
        words = dialogue.split()
        for i in range(len(words)-1, -1, -1):
            if words[i][-1] in ['?', '!', '.', ')']:
                break
            else:
                dialogue = ' '.join(words[:i])
        return dialogue

    dialogue_count = {}
    
    response = requests.get(url)
    
    if response.status_code == 200:
        html_script = response.text
        soup = BeautifulSoup(html_script, 'html.parser')
        
        underlined_text = soup.find_all('u')
        
        if len(underlined_text) > 0:
            for specific_instance in underlined_text:
                specific_instance.unwrap()
        
        # flatten the string after unwrapping to get rid of NavigableStrings
        final_soup = BeautifulSoup(str(soup), "html.parser")
    
        # Extract character names and spoken dialogue for the first 20 occurrences
        formatted_lines = []
    
        previous_character_name = None
    
        for bold_tag in final_soup.find_all('b'):
            character_name = bold_tag.text.strip()

            if character_name in dialogue_count:
                dialogue_count[character_name] += 1
            else:
                dialogue_count[character_name] = 1
    
            # Find the next sibling that is not a tag
            dialogue_tag = bold_tag.find_next_sibling(string=True)
    
            # Check if dialogue_tag is not None and not an empty string
            if len(character_name.split(' ')) <= 3:
                if dialogue_tag:
                    dialogue = str(dialogue_tag)
                    dialogue = re.sub(r'\s+', ' ', dialogue.replace('\r\n', ' ').strip())
        
                    parts = re.split(r'[A-Z]{2,}', dialogue)
                    dialogue = parts[0].strip()
        
                    # Check if '!' is in the character name
                    if '!' in character_name:
                        # Append character name to the previous dialogue
                        if formatted_lines and previous_character_name:
                            formatted_lines[-1] = (previous_character_name, f"{formatted_lines[-1][1]} {character_name}", dialogue_count.get(previous_character_name,1))
                    else:
                        # Check if the dialogue is not an empty string before appending
                        if ':' not in character_name and len(clean_dialogue(dialogue)) > 1:
                            formatted_lines.append((character_name, clean_dialogue(dialogue), dialogue_count.get(character_name,1)))
                            previous_character_name = character_name
                        else:
                            pass
    
    return formatted_lines
    
