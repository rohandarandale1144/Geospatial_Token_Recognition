from fuzzywuzzy import process
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_lg')

# Sample canonical tables
country_table = pd.read_csv("D:\\VS Code\\NLP Mini Project\\NLP_Mini_Project\\data\\countries.csv")
country_table = country_table["name"].tolist()

# print(country_table.head())

city_table = pd.read_csv("D:\\VS Code\\NLP Mini Project\\NLP_Mini_Project\\data\\cities.csv")
city_table = city_table["name"].tolist()

# print(city_table.head())
state_table = pd.read_csv("D:\\VS Code\\NLP Mini Project\\NLP_Mini_Project\\data\\states.csv")
state_table = state_table["name"].tolist()

# Sample input sentence
sentence = "The United Nations is an international organization founded in 1945.\
            Its headquarters are located in New York City.\
            India, officially the Republic of India, is a country in South Asia.\
            Its capital is New-Delhi and its largest city is Mumbai.\
            The Taj Mahal, a UNESCO World Heritage Site, is located in Agra, India.\
            Apple Inc. is an American multinational technology company headquartered in Cupertino, , California.\
            The company's best-known hardware products include the iPhone, iPad, Mac, and Apple Watch.\
            New-Zealand"

doc = nlp(sentence)
def show_ents(doc):
    list=[]
    if doc.ents:
        for ent in doc.ents:
            list.append(ent.text)
            print(ent.text +'-'+ ent.label_)
        return list
    else:
        return 0
    
tokens = show_ents(doc)
# Tokenize and preprocess the input sentence
# tokens = sentence.split()
# geospatial_tokens = [token for token in tokens if token.lower() not in ["the", "of", "in", "or", "entire", "a", "for"]]

# print(tokens)
# Function to perform fuzzy matching
def fuzzy_match(token, table):
    match, score = process.extractOne(token, table)
    return match, score

# Process each geospatial token
for token in tokens:
    canonical_name = None
    table_name = None

    # Fuzzy match with country names
    country_match, country_score = fuzzy_match(token, country_table)
    if country_score >= 95:  # Adjust threshold as needed
        canonical_name = country_match
        table_name = "Country"

    # Fuzzy match with city names
    city_match, city_score = fuzzy_match(token, city_table)
    if city_score >= 95:  # Adjust threshold as needed
        canonical_name = city_match
        table_name = "City"

    # Fuzzy match with state names
    state_match, state_score = fuzzy_match(token, state_table)
    if state_score >= 95:  # Adjust threshold as needed
        canonical_name = state_match
        table_name = "State"

    # Print the results
    if canonical_name:
        print("Token:", token, ", Canonical name:", canonical_name, ", Table:", table_name)
