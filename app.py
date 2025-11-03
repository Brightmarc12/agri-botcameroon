# app.py (Corrected and Improved Version)

from flask import Flask, request, jsonify

app = Flask(__name__)

# --- AGENT'S EXPANDED KNOWLEDGE BASE ---

# English keys are our "master" keys
market_prices = {
    "cocoa": "1,500 XAF per kg", "coffee": "1,200 XAF per kg",
    "plantain": "500 XAF per bunch", "maize": "250 XAF per kg",
    "cassava": "150 XAF per kg", "yams": "400 XAF per tuber"
}
crop_problems = {
    ("cocoa", "pods"): "This could be Black Pod disease. Recommendation: Remove and destroy affected pods. Ensure proper tree spacing for air circulation.",
    ("maize", "yellow leaves"): "Indicates a nitrogen deficiency. Recommendation: Apply a nitrogen-rich fertilizer like Urea.",
    ("plantain", "black spots"): "Might be Black Sigatoka disease. Recommendation: Remove infected leaves and consider a recommended fungicide.",
    ("coffee", "rust"): "Likely Coffee Leaf Rust. Recommendation: Prune affected branches and apply a copper-based fungicide.",
    ("cassava", "mosaic"): "Cassava Mosaic Disease shows distorted leaves. Recommendation: Use resistant varieties and remove infected plants to prevent spread."
}
weather_data = {
    "douala": "Today: Cloudy with a 70% chance of rain. High of 29°C.",
    "yaounde": "Today: Partly sunny with scattered thunderstorms in the afternoon. High of 28°C.",
    "buea": "Today: Light rain throughout the day. High of 24°C.",
    "bamenda": "Today: Sunny with some clouds. High of 26°C."
}
farming_tips = {
    "storage": "To reduce post-harvest loss, ensure crops are dried properly before storage. Store in a cool, dry, and well-ventilated place away from pests.",
    "irrigation": "For most crops, water early in the morning to reduce evaporation. Drip irrigation is highly efficient for saving water.",
    "cocoa": "Tip for Cocoa: Regular pruning of your cocoa trees helps prevent diseases and increases pod yield.",
    "maize": "Tip for Maize: Plant maize at the start of the rainy season for best results. Spacing should be approximately 75cm between rows."
}
soil_info = {
    "littoral": "The soil in the Littoral region is mainly fertile sandy loam, excellent for plantains, cassava, and yams.",
    "south-west": "The South-West region has rich volcanic soils, ideal for cash crops like cocoa, coffee, and rubber.",
    "north-west": "The North-West has volcanic soils on its highlands, great for coffee, maize, and beans."
}
fertilizer_guide = {
    "maize": "Maize benefits greatly from NPK 20-10-10 fertilizer at planting, followed by a top dressing of Urea after a few weeks.",
    "cocoa": "For young cocoa trees, use a balanced NPK fertilizer. For mature trees, a fertilizer low in nitrogen but high in potassium is recommended to boost pod production.",
    "yams": "Yams require potassium-rich soil. Use NPK 15-15-15 or similar balanced fertilizers."
}

# NEW: Keyword Translation Dictionary (French -> English Master Key)
keyword_translations = {
    "cacao": "cocoa", "café": "coffee", "plantain": "plantain", 
    "maïs": "maize", "manioc": "cassava", "ignames": "yams",
    "gousses": "pods", "feuilles jaunes": "yellow leaves", "taches noires": "black spots",
    "rouille": "rust", "mosaïque": "mosaic", "stockage": "storage", "irrigation": "irrigation",
    "sud-ouest": "south-west", "littoral": "littoral", "nord-ouest": "north-west"
}

# French Response Templates
translations = {
    "price_info": "Le prix actuel du marché pour {crop} est de {price}.",
    "price_inquiry": "Je peux vous donner les prix pour: cacao, café, plantain, maïs, manioc, ignames. Lequel vous intéresse?",
    "help_menu": "Aide Agri-Bot:\n1. Demandez le 'prix' d'une culture.\n2. Décrivez un 'problème' agricole.\n3. Demandez la 'météo' pour une ville.\n4. Demandez des 'conseils' sur l'agriculture.\n5. Demandez des 'infos sol' pour une région.\n6. Demandez un 'guide engrais' pour une culture.",
    "unknown_command": "Désolé, je ne comprends pas. Tapez 'aide' pour voir ce que je peux faire.",
    "weather_info": "Météo pour {city}: {forecast}",
    "weather_inquiry": "Pour quelle ville souhaitez-vous la météo? (ex: Douala, Yaounde)",
    "tip_info": "Conseil agricole: {tip}",
    "tip_inquiry": "Demandez des conseils sur 'stockage', 'irrigation', 'cacao', ou 'maïs'.",
    "soil_info": "Infos sur le sol pour la région {region}: {info}",
    "soil_inquiry": "Je peux donner des infos sur le sol pour les régions: Littoral, Sud-Ouest, Nord-Ouest.",
    "fertilizer_info": "Guide d'engrais pour {crop}: {guide}",
    "fertilizer_inquiry": "Je peux fournir un guide d'engrais pour: maïs, cacao, ignames."
}


@app.route('/agent', methods=['POST'])
def telex_agent():
    incoming_data = request.get_json()
    user_message = incoming_data.get('message', '').lower()
    
    is_french = any(word in user_message for word in ['prix', 'météo', 'aide', 'problème', 'conseil', 'sol', 'engrais', 'quel', 'est'])
    
    response_text = ""

    if any(keyword in user_message for keyword in ['problem', 'problème', 'disease']):
        response_text = handle_problem(user_message) # Problem handler is language-agnostic for now
    elif any(keyword in user_message for keyword in ['price', 'prix']):
        response_text = handle_price(user_message, is_french)
    elif any(keyword in user_message for keyword in ['weather', 'météo']):
        response_text = handle_weather(user_message, is_french)
    elif any(keyword in user_message for keyword in ['tip', 'conseil']):
        response_text = handle_tips(user_message, is_french)
    elif any(keyword in user_message for keyword in ['soil', 'sol']):
        response_text = handle_soil(user_message, is_french)
    elif any(keyword in user_message for keyword in ['fertilizer', 'engrais']):
        response_text = handle_fertilizer(user_message, is_french)
    elif any(keyword in user_message for keyword in ['help', 'aide']):
        response_text = get_help_menu(is_french)
    else:
        response_text = translations['unknown_command'] if is_french else "Sorry, I don't understand. Type 'help' to see what I can do."

    return jsonify({"response": response_text})


def get_english_keyword(message):
    """Translates French keywords in a message to their English equivalent for logic processing."""
    for fr_word, en_word in keyword_translations.items():
        if fr_word in message:
            return en_word
    # If no French keyword found, search for a direct English keyword
    for en_word in market_prices.keys(): # Check against a list of English keywords
        if en_word in message:
            return en_word
    return None


def handle_price(message, is_french):
    # First, find the master English keyword for the crop
    crop_keyword = get_english_keyword(message)
    
    if crop_keyword and crop_keyword in market_prices:
        price = market_prices[crop_keyword]
        if is_french:
            # Find the French word for the crop to make the response sound natural
            french_crop_name = [fr for fr, en in keyword_translations.items() if en == crop_keyword][0] or crop_keyword
            return translations['price_info'].format(crop=french_crop_name, price=price)
        return f"The current market price for {crop_keyword} is {price}."
    
    return translations['price_inquiry'] if is_french else "I can give you prices for: cocoa, coffee, plantain, maize, cassava, yams. Which one are you interested in?"


# --- CORRECTED: handle_soil function ---
def handle_soil(message, is_french):
    # We check the original message, no more replacing hyphens.
    for region, info in soil_info.items():
        # A simple check is more robust here
        if region in message:
            return translations['soil_info'].format(region=region, info=info) if is_french else f"Soil Info for {region} region: {info}"
    return translations['soil_inquiry'] if is_french else "I can provide soil info for the following regions: Littoral, South-West, North-West."


# --- Other handlers remain the same for now, but could be improved with the keyword translation too ---
def handle_problem(message): # This could also be improved later
    for (crop, symptom), solution in crop_problems.items():
        if crop in message and symptom in message:
            return solution
    return "Please describe the problem by mentioning the crop and the symptom (e.g., 'My maize has yellow leaves')."

def handle_weather(message, is_french):
    for city, forecast in weather_data.items():
        if city in message:
            return translations['weather_info'].format(city=city, forecast=forecast) if is_french else f"Weather for {city}: {forecast}"
    return translations['weather_inquiry'] if is_french else "Which city's weather do you want? (e.g., Douala, Yaounde)"

def handle_tips(message, is_french):
    for topic, tip in farming_tips.items():
        if topic in message:
            return translations['tip_info'].format(tip=tip) if is_french else f"Farming Tip: {tip}"
    return translations['tip_inquiry'] if is_french else "Ask for tips on: 'storage', 'irrigation', 'cocoa', or 'maize'."

def handle_fertilizer(message, is_french):
    crop_keyword = get_english_keyword(message)
    if crop_keyword and crop_keyword in fertilizer_guide:
        guide = fertilizer_guide[crop_keyword]
        if is_french:
            french_crop_name = [fr for fr, en in keyword_translations.items() if en == crop_keyword][0] or crop_keyword
            return translations['fertilizer_info'].format(crop=french_crop_name, guide=guide)
        return f"Fertilizer Guide for {crop_keyword}: {guide}"
    return translations['fertilizer_inquiry'] if is_french else "I can provide a fertilizer guide for: maize, cocoa, yams."

def get_help_menu(is_french):
    if is_french:
        return translations['help_menu']
    return "Agri-Bot Help:\n1. Ask for 'price' of a crop.\n2. Describe a crop 'problem'.\n3. Ask for 'weather' in a city.\n4. Ask for 'tips' on farming.\n5. Ask for 'soil info' for a region.\n6. Ask for a 'fertilizer guide' for a crop."

# if __name__ == '__main__':
   # app.run(debug=True)