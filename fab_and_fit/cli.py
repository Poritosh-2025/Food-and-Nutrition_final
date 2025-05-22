# fab_and_fit/cli.py
from api.utils import (
    manual_entry,
    upload_image_path,
    analyze_food_image,
    format_food_details,
    get_nutritional_data,
    UserProfile,
    display_info
)

def cli_main():
    while True:
        choice = input("Upload a photo, enter items manually, or exit? (photo/manual/exit): ").lower()
        if choice == 'exit':
            print("Thank you for using Fab & Fit. Goodbye!")
            break
        if choice == 'photo':
            image_data = upload_image_path()
            if image_data:
                response = analyze_food_image(image_data)
                if response:
                    meal_name, serving_size, ingredients = format_food_details(response)
                    if ingredients:
                        nutritional_data = get_nutritional_data(meal_name, ingredients)
                        display_info(meal_name, serving_size, ingredients, nutritional_data)
                    else:
                        print("No ingredients found. Try manual entry.")
                else:
                    print("Image analysis failed. Try manual entry.")
            else:
                print("Failed to load image. Try again.")
            break
        elif choice == 'manual':
            meal_name, serving_size, ingredients = manual_entry()
            nutritional_data = get_nutritional_data(meal_name, ingredients)
            display_info(meal_name, serving_size, ingredients, nutritional_data)
            break
        else:
            print("Invalid choice. Choose 'photo', 'manual', or 'exit'.")
    
    # Meal plan generation
    while True:
        plan_choice = input("\nWould you like a personalized meal plan? (yes/no): ").lower()
        if plan_choice in ['yes', 'no']:
            if plan_choice == 'yes':
                user_profile = UserProfile()
                user_profile.get_user_info()
                meal_plan = user_profile.generate_personalized_meal_plan()
                print("\n--- Personalized Meal Plan ---")
                print(meal_plan)
            break
        print("Please answer with 'yes' or 'no'.")

if __name__ == "__main__":
    cli_main()