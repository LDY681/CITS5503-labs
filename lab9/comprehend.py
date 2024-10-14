import boto3

# AWS Comprehend client
REGION = "ap-southeast-2"
client = boto3.client('comprehend', region_name=REGION)

# Function to detect dominant language and print output
def detect_language(text):
    response = client.detect_dominant_language(Text=text)
    lang = response['Languages'][0]

    # Language code for mapping
    language_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'it': 'Italian',
    }
    
    # Convert results to message
    lang_code = lang['LanguageCode']
    confidence = round(lang['Score'] * 100, 2)
    language_name = language_map.get(lang_code, lang_code)
    print(f"{language_name} detected with {confidence}% confidence")

def detect_sentiment(text, language_code='en'):
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = response['Sentiment']
    sentiment_scores = response['SentimentScore']
    
    print(f"Sentiment: {sentiment} with scores: {sentiment_scores}")

def detect_entities(text, language_code='en'):
    response = client.detect_entities(Text=text, LanguageCode=language_code)
    entities = response['Entities']
    
    for entity in entities:
        print(f"Entity: {entity['Text']}, Type: {entity['Type']} with {round(entity['Score']*100, 2)}% confidence")

def detect_key_phrases(text, language_code='en'):
    response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    key_phrases = response['KeyPhrases']
    
    for phrase in key_phrases:
        print(f"Key Phrase: {phrase['Text']} with {round(phrase['Score']*100, 2)}% confidence")

def detect_syntax(text, language_code='en'):
    response = client.detect_syntax(Text=text, LanguageCode=language_code)
    syntax_tokens = response['SyntaxTokens']
    
    for token in syntax_tokens:
        print(f"Word: {token['Text']}, POS: {token['PartOfSpeech']['Tag']} with {round(token['PartOfSpeech']['Score']*100, 2)}% Confidence")

# Test in different languages
texts = [
    "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",
    "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas. En 1615 aparecería la segunda parte del Quijote de Cervantes con el título de El ingenioso caballero don Quijote de la Mancha.",
    "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",
    "L'amor che move il sole e l'altre stelle."
]

for text in texts:
    detect_language(text)
print("---------")
for text in texts:
    detect_sentiment(text)
print("---------")
for text in texts:
    detect_entities(text)
print("---------")
for text in texts:
    detect_key_phrases(text)
print("---------")
for text in texts:
    detect_syntax(text)