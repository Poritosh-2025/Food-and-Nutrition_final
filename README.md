## Fab & Fit

Fab & Fit is a nutrition and meal analysis application that leverages Google Gemini AI to analyze food images or manual entries, extract meal details, and provide nutritional information. The project is built with Python and includes both a CLI and API for user interaction.

---

## Features

- Upload food images for AI-powered meal and ingredient recognition
- Manual meal entry with validation
- Automated nutritional data retrieval using Gemini AI
- User profile management
- Logging and error handling
- CLI interface for easy use

---

## Project Structure

```
fab_and_fit/
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── api_routes.py
│   ├── api_views.py
│   ├── apps.py
│   ├── constants.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── migrations/
│   └── services/
│
├── fab_and_fit/
│   └── __init__.py
│   └── asgi.py
│   └── ...
│   manage.py
│   requirements.txt
└── uploads/
```

---
## Installation

Follow these steps to set up the project:

1. **Install virtualenv :**
   ```sh
   pip install virtualenv
   ```

2. **Create and activate a virtual environment:**
   ```sh
   virtualenv nutritionvenv
   nutritionvenv\Scripts\activate   # On Windows
  
   ```

3. **Navigate to the project directory:**
   ```sh
   cd fab_and_fit
   ```

4. **Install project dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```sh
   python manage.py makemigrations api
   python manage.py migrate
   ```

6. **Create a superuser for the Django admin:**
   ```sh
   python manage.py createsuperuser
   ```
7.Running the server
python manage.py runserver

## Nutrition & Meal Plan Endpoints

| Method | Endpoint                                             | Description                        |
|--------|------------------------------------------------------|------------------------------------|
| POST | `http://127.0.0.1:8000/api/analyze-image/`         | Analyze nutrition from an image    |
| POST | `http://127.0.0.1:8000/api/analyze-manual/`        | Manually input data for analysis   |
| POST | `http://127.0.0.1:8000/api/meal-plan/`             | Generate or retrieve meal plans    |
| GET  | `http://127.0.0.1:8000/api/meal-plan/1/`           | Retrieve a specific meal plan (ID=1) |
| GET  | `http://127.0.0.1:8000/api/nutrition/matton/`      | Get nutrition info for "matton"    |
## Environment Variables

- `.env` file is used for storing sensitive information like API keys.
- Example:
  ```
  GEMINI_API_KEY=your_gemini_api_key_here
  ```

## Acknowledgements

- [Google Gemini AI](https://ai.google.dev/)
- [Pillow](https://python-pillow.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
