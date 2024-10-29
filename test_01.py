import spacy
import pandas as pd
from fuzzywuzzy import process

# Load spaCy English model
nlp = spacy.load("en_core_web_lg")

known_entities = pd.read_csv("D:\\VS Code\\NLP Mini Project\\NLP_Mini_Project\\data\\cities.csv")
known_entities = known_entities['name'].tolist()
# Sample text with potential typos
text = "The United Nations is an international organization founded in 1945.\
        Its headquarters are located in New York City.\
        India, officially the Republic of India, is a country in South Asia.\
        Its capital is New-Delhi and its largest city is Mumbaii.\
        The Taj Mahal, a UNESCO World Heritage Site, is located in Agraa, India.\
        Apple Inc. is an American multinational technology company headquartered in Ccupertino, , California.\
        The company's best-known hardware products include the iPhone, iPad, Mac, and Apple Watch.\
        New-Zealand"

# Function to perform fuzzy matching with known entities
def fuzzy_match(token, table):
    match, score = process.extractOne(token, table)
    return match, score

# Process the text with spaCy
doc = nlp(text)

# Initialize a set to store recognized entities
recognized_entities = set()

print(doc.ents)
for ent in doc.ents:
    print(ent.text +'-'+ent.label_)

# Iterate over named entities recognized by spaCy
for ent in doc.ents:
    # Check if the entity text has already been recognized
    if ent.text.lower() not in recognized_entities:
        recognized_entities.add(ent.text.lower())
        
        # Perform fuzzy matching with known entities
        match, score = fuzzy_match(ent.text, known_entities)
        
        # If fuzzy match score is above a threshold, consider it as a recognized entity
        if score >= 90:
            print("Recognized Entity:", match, " (Original:", ent.text, ")")
        else:
            print("Unrecognized Entity:", ent.text)
