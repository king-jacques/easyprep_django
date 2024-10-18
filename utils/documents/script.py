from .utils import Pdf
import code
from termcolor import colored
import readline #this import will fix issue of [[D^[[D^[[
import re
import json
import os
PATTERN_1 = r'\nQuestion ?\d+'
PATTERN_2 = r'\nPhrase ?\d+ ?:\nA'
PATTERN_3 = r'\nPhrase ?\d+\nA'

TEXT_TITLE = r'Texte ?\d+ ?'
COLON = r':'
NEWLINE = r'\n'


MIN_LENGTH = 5
def main():
    #print('something')
    pdf = Pdf()
    titles = find(pdf.pages)
    q = pdf.group_questions()

    print(colored("Running main function...", "green"))
    # Add some initial functionality here
    # Drop into the Python interpreter
    vars = globals().copy()  # Copy the current global variables
    vars.update(locals())    # Update with the current local variables
    shell = code.InteractiveConsole(vars)
    shell.interact("You can now interact with the code. Type exit() or Ctrl-D to quit.")

def find(pages:dict, pattern=None):
    titles = {}
    for page, text in pages.items():
        colon = re.search(COLON, text)
        newline = re.search(NEWLINE, text)
        texte = re.search(TEXT_TITLE, text)
        if colon.start() == 0: #COLON is at beginning of text
            #first \n = end of title.
            #newline = re.search(NEWLINE, text)
            title = text[2: newline.start()]
            #print(page, colored(title, 'green'))
        elif texte.start() == 0: #TITLE BEGINS AFTER FIRST COLON
                if newline.start() - texte.end() < MIN_LENGTH:
                    #print(colored('CONDITION ' + page, 'blue'))
                    newline = re.search(NEWLINE, text[newline.end():])
                title =text[colon.start()+2: newline.start()]

                #print(page, colored(title, 'green'))
        else:
            # Title is from beginning of text to Texte
            title = text[0:texte.start()]
            #print(page, colored(title, 'yellow'))
        titles[page] = title
    return titles


if __name__ == '__main__':
    print(colored('loading...', "red"))
    main()
    

# [
#     {
        
#        "questionGroup": {
#            "title": "this is the title",
#            "instruction": "this is the instruction",
#            "other_fields": "these are the other fields"
#        }
#        "questions": [
#                {
#                    "questionText": "what is your name",
#                     "options": [
#                           {
#                                "text": "Chinedu",
#                                 "isCorrectAnswer": false
#                            }
#                      ]
#                 }
#           ]
#      }
# ]


def json_to_dict(file_location='textes-a-trou.json'):
    with open(file_location, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def count(file_location='Tef_textes_Easyprrep.json'):
    # import json
    # with open(file_location, 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    data = json_to_dict(file_location)
    counter = 0
    indices = []
    questions = data['questions']
    for index, question in enumerate(questions):
        for option in question['questions']:
            if not option.get('questionText'):
                counter +=1
                indices.append(index)
    print(indices)
    print(counter)
    return (data, counter, indices)


def dict_to_json(dictionary, filename='tef_questions_combined.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(dictionary, json_file, ensure_ascii=False, indent=4)

def combine_json(json1, json2):
    combined = []
    for qg in json1:
        if 'texte à trous' in qg['questionGroup']['groupTitle']:
            #json 2 is textes a trou
            for qg2 in json2:
                if qg['questionGroup']['groupTitle'] == qg2['questionGroup']['groupTitle']:
                    #take qg2
                    combined.append(qg2)
        else:
            combined.append(qg)
    return 

imagelink = f"https://easyprepassets.s3.amazonaws.com/{{image_name}}"


def combine_jsons(folder_path, json_file_path=None, title=None):
    import random
    import string
    if not title:
        alphabets = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(1, 2)))
        digits = ''.join(random.choice(string.digits) for _ in range(5 - len(alphabets)))
        result = list(alphabets + digits)
        random.shuffle(result)
        title = ''.join(result)
    json_file_path = json_file_path or os.path.join(folder_path, f'{title}.json')
    json_files = {}
    file_titles = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if filename.endswith(('json',)):
                file_title = filename.removesuffix('.json')
                print(file_title)
                # while file_title in file_titles:
                #     file_title = file_title + 'Copy'

                file_titles.append(file_title)
                image_name = file_title.replace(" ", "-")
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # question_answer = {"questions": data, "image_link": imagelink.format(image_name=image_name)}
                    question_answer = {"questions": data}
                    json_files[file_title] = question_answer
        except Exception as e:
            print("an error occurred", e)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_files, json_file, indent=4)


file_titles_dict = {
    'Billing': 'Billing, Pricing and Support',
    'Concepts': 'Cloud Concepts',
    'Technology': 'Cloud Technology and Services',
    'Security': 'Security and Compliance'
}

def combine_multiple_jsons(folder_path, file_titles_dict=None, title=None, output_folder=None):
    import random
    import string
    
    if not title:
        alphabets = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(1, 2)))
        digits = ''.join(random.choice(string.digits) for _ in range(5 - len(alphabets)))
        result = list(alphabets + digits)
        random.shuffle(result)
        folder_name = os.path.basename(folder_path)
        title = folder_name + ''.join(result)

    keys = file_titles_dict.keys()
    
    json_files = {}
    file_titles = []
    output_folder = output_folder or os.path.join(folder_path, 'results')
    json_file_path = os.path.join(output_folder, f'{title}.json')
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if filename.endswith(('json',)):
                
                file_title = filename.removesuffix('.json')
                firstmatch = next((key for key in keys if key in file_title), None)
                category = file_titles_dict.get(firstmatch)
                print(file_title, '.....', category)
                file_titles.append(file_title)
                category = category or 'Unknown'
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    # if type(data) == list:
                    #     data = 
                    # question_answer = {"questions": data, "image_link": imagelink.format(image_name=image_name)}

                    # print(len(data))
                    if category in json_files:
                        json_files[category].extend(data)
                    else:
                        json_files[category] = data
        except Exception as e:
            print("an error occurred", e)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_files, json_file, indent=4)


'''
from utils.documents.script import combine_multiple_jsons
combine_multiple_jsons('utils/documents/env/aws_ccp')
'''