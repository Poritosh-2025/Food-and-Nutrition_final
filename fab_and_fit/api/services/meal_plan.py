# fab_and_fit/api/services/meal_plan.py
import logging
import re
from datetime import datetime
from .food_analysis import gemini_model
from api.models import MealPlan 
logger = logging.getLogger(__name__)

def create_meal_plan(user_data, generated_plan):
    # Create and save a new MealPlan instance
    meal_plan = MealPlan.objects.create(
        plan_data=generated_plan,
        bmi=calculate_bmi(user_data['height'], user_data['weight']),
        bmr=calculate_bmr(user_data),
        age=user_data['age'],
        weight=user_data['weight'],
        height=user_data['height'],
        activity_level=user_data['activity_level'],
        fitness_goal=user_data['fitness_goal'],
        is_vegan=user_data['vegan_preference']
    )
    return meal_plan

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate Body Mass Index (BMI)"""
    return round(weight_kg / ((height_cm / 100) ** 2), 2)

def calculate_bmr(gender: str, weight_kg: float, height_cm: float, age: int) -> float:
    """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation"""
    if gender.lower() == 'male':
        return round((10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5, 2)
    return round((10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161, 2)

class MealPlanGenerator:
    def __init__(self, user_data):
        self.user_data = user_data
        
    #@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self):
        """Generate meal plan using Gemini model"""
        try:
            prompt = f"""Your meal plan generation prompt here"""
            response = gemini_model.generate_content(prompt)
            return self.parse_response(response.text)
        except Exception as e:
            logger.error(f"Meal plan generation failed: {str(e)}")
            raise

    def parse_response(self, response_text):
        """Parse Gemini response into structured format"""
        try:
            # Extract total calories
            total_match = re.search(r"Total Estimated Calories:\s*(\d+)", response_text)
            parsed_total = int(total_match.group(1)) if total_match else 0
            
            # Extract meals
            parsed_meals = []
            current_meal = {}
            
            for line in response_text.split('\n'):
                line = line.strip()
                if line.startswith("Meal Name:"):
                    current_meal["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("Key Ingredients:"):
                    current_meal["ingredients"] = [x.strip() for x in line.split(":", 1)[1].split(",")]
                elif line.startswith("Macronutrients:"):
                    macros = re.findall(r"(\w+):\s*([\d.]+)\s*g", line)
                    current_meal["macros"] = {k.lower(): float(v) for k, v in macros}
                elif line.startswith("Health Benefit:"):
                    current_meal["benefit"] = line.split(":", 1)[1].strip()
                    parsed_meals.append(current_meal)
                    current_meal = {}
            
            return {
                "total_calories": parsed_total,
                "meals": parsed_meals,
                "bmi": self.user_data.get('bmi'),
                "bmr": self.user_data.get('bmr')
            }
            
        except Exception as e:
            logger.error(f"Failed to parse meal plan: {str(e)}")
            return {
                "total_calories": 0,
                "meals": [],
                "error": "Failed to parse meal plan response"
            }

def generate_meal_plan(user_data: dict) -> dict:
    """Generate meal plan using calculated health metrics"""
    # Calculate health metrics
    bmi = calculate_bmi(user_data['height'], user_data['weight'])
    bmr = calculate_bmr(
        gender=user_data['gender'],
        weight=user_data['weight'],
        height=user_data['height'],
        age=user_data['age']
    )
    
    # Add to user data for meal planning
    user_data.update({
        'bmi': bmi,
        'bmr': bmr
    })
    generator = MealPlanGenerator(user_data)
    return generator.generate()
