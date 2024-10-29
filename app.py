from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import process
import pandas as pd
import spacy

app = Flask(__name__)

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Load sample data
country_table = pd.read_csv("countries.csv")["name"].tolist()
city_table = pd.read_csv("cities.csv")["name"].tolist()
state_table = pd.read_csv("states.csv")["name"].tolist()

# Function to perform entity extraction and fuzzy matching
def process_input(input_text):
    doc = nlp(input_text)
    entities = []
    for ent in doc.ents:
        entities.append(ent.text)
    results = []
    for token in entities:
        canonical_name = None
        table_name = None
        # Fuzzy match with country names
        country_match, country_score = process.extractOne(token, country_table)
        if country_score >= 95:
            canonical_name = country_match
            table_name = "Country"
        # Fuzzy match with city names
        city_match, city_score = process.extractOne(token, city_table)
        if city_score >= 95:
            canonical_name = city_match
            table_name = "City"
        # Fuzzy match with state names
        state_match, state_score = process.extractOne(token, state_table)
        if state_score >= 95:
            canonical_name = state_match
            table_name = "State"
        if canonical_name:
            results.append({"token": token, "canonical_name": canonical_name, "table_name": table_name})
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    input_text = request.form['inputText']
    results = process_input(input_text)
    return jsonify(results)

# if __name__ == '__main__':
#     app.run(debug=True)