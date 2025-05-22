# api/api_routes.py
from django.urls import path
from .api_views import AnalyzeImageView,AnalyzeManualView, NutritionView, MealPlanCreateView,MealPlanRetrieveView

urlpatterns = [
        path('analyze-image/', AnalyzeImageView.as_view(), name='analyze-image'),
        path('analyze-manual/', AnalyzeManualView.as_view(), name='analyze-manual'),
        path('meal-plan/', MealPlanCreateView.as_view(), name='meal-plan-create'),
        path('meal-plan/<int:plan_id>/', MealPlanRetrieveView.as_view(), name='meal-plan-retrieve'),
        path('nutrition/<str:food_name>/', NutritionView.as_view(), name='nutrition-info'),
]
