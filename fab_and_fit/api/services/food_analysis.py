# api/services/food_analysis.py
import google.generativeai as genai
import io
import re
import os
import logging
import time
from PIL import Image
from dotenv import load_dotenv
from api.models import FoodNutrition 
from django.core.files.uploadedfile import InMemoryUploadedFile

load_dotenv()
print("API Key:", os.getenv('GEMINI_API_KEY'))
logger = logging.getLogger(__name__)
# Initialize Gemini
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)




#@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def analyze_image(image_file):
    """Process uploaded image file and return analysis"""
    try:
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')

        prompt = """Your image analysis prompt here"""
        
        response = gemini_model.generate_content([prompt, image])
        return parse_image_response(response.text)
    
    except Exception as e:
        logger.error(f"Image analysis failed: {str(e)}")
        raise

def parse_image_response(response_text):
    """Parse Gemini response for image analysis with error handling"""
    try:
        parsed_name = "Unknown Meal"
        parsed_size = "100"
        parsed_ingredients = []
        
        # Extract meal name and serving size
        name_match = re.search(r"Meal Name:\s*(.+?)\s*\((\d+)", response_text)
        if name_match:
            parsed_name = name_match.group(1).strip()
            parsed_size = name_match.group(2).strip()
        
        # Extract ingredients
        parsed_ingredients = [
            line.strip().replace('- ', '') 
            for line in response_text.split('\n') 
            if line.strip().startswith('-') and ':' in line
        ]
        
        return {
            "meal_name": parsed_name,
            "serving_size": parsed_size,
            "ingredients": parsed_ingredients
        }
    except Exception as e:
        logger.error(f"Error parsing image response: {str(e)}")
        return {
            "meal_name": "Unknown Meal",
            "serving_size": "100",
            "ingredients": []
        }
#@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_nutrition_data(meal_name, ingredients):
    """Get nutritional information from Gemini"""
    try:
        prompt = f"""Your existing nutrition prompt here"""
        
        response = gemini_model.generate_content(prompt)
        return parse_nutrition_response(response.text)
    except Exception as e:
        logger.error(f"Nutrition data error: {str(e)}")
        raise

def parse_nutrition_response(response_text):
    """Parse nutritional response with regex patterns"""
    nutrients = {
        "calories": 0,
        "protein": 0,
        "carbohydrates": 0,
        "fat": 0,
        "fiber": 0
    }
    
    patterns = {
        "calories": r"Calories:\s*(\d+)",
        "protein": r"Protein:\s*(\d+(?:\.\d+)?)",
        "carbohydrates": r"Carbohydrates:\s*(\d+(?:\.\d+)?)",
        "fat": r"Fat:\s*(\d+(?:\.\d+)?)",
        "fiber": r"Fiber:\s*(\d+(?:\.\d+)?)"
    }
    
    for nutrient, pattern in patterns.items():
        match = re.search(pattern, response_text)
        if match:
            nutrients[nutrient] = float(match.group(1))
    
    return nutrients
def get_nutrition_data(meal_name, ingredients):
    """Get nutritional information from Gemini with caching"""
    try:
        # Check cache first
        cached = FoodNutrition.objects.filter(food_name__iexact=meal_name).first()
        if cached:
            return cached.nutrition_data
            
        # Get from Gemini API
        prompt = f"""Your nutrition prompt for {meal_name} with ingredients: {', '.join(ingredients)}"""
        response = gemini_model.generate_content(prompt)
        
        # Parse and cache
        nutrition_data = parse_nutrition_response(response.text)
        FoodNutrition.objects.create(
            food_name=meal_name.lower(),
            nutrition_data=nutrition_data
        )
        return nutrition_data
        
    except Exception as e:
        logger.error(f"Nutrition data error: {str(e)}")
        return {"error": str(e)}