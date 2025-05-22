from django.contrib import admin
from .models import MealPlan, FoodNutrition, ImageAnalysis

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'age', 'weight', 'height', 'fitness_goal', 'activity_level')
    list_filter = ('fitness_goal', 'activity_level', 'created_at')
    search_fields = ('dietary_preferences',)
    readonly_fields = ('created_at', 'bmi', 'bmr')
    
    fieldsets = (
        ('User Information', {
            'fields': ('age', 'weight', 'height')
        }),
        ('Preferences', {
            'fields': ('dietary_preferences', 'fitness_goal', 'activity_level', 'is_vegan')
        }),
        ('Calculations', {
            'fields': ('bmi', 'bmr'),
            'classes': ('collapse',)
        }),
        ('Plan Data', {
            'fields': ('plan_data',)
        }),
    )

@admin.register(FoodNutrition)
class FoodNutritionAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'created_at', 'updated_at')
    search_fields = ('food_name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fields = ('food_name', 'nutrition_data', 'created_at', 'updated_at')

@admin.register(ImageAnalysis)
class ImageAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'analysis_result', 'nutrition_data')
    
    fields = ('image', 'uploaded_at', 'analysis_result', 'nutrition_data')