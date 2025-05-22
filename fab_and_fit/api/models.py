from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from .constants import ACTIVITY_LEVEL_CHOICES, FITNESS_GOAL_CHOICES

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='other', help_text="User's self-identified gender")
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField()  # in cm
    weight = models.FloatField()  # in kg
    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES  # Use imported choices
    )
    
    fitness_goal = models.CharField(
        max_length=20,
        choices=FITNESS_GOAL_CHOICES,  # Use imported choices
        default='maintenance',
        null=False
    )
    vegan_preference = models.BooleanField(default=False)
    dietary_preferences = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class MealPlan(models.Model):
    # Preferences
    ACTIVITY_LEVELS = [
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active'),
        ('Extra Active', 'Extra Active'),
    ]
    
    FITNESS_GOALS = [
        ('Weight Loss', 'Weight Loss'),
        ('Muscle Gain', 'Muscle Gain'),
        ('Maintenance', 'Maintenance'),
        ('General Fitness', 'General Fitness'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    age = models.IntegerField(null=True)
    weight = models.FloatField(help_text="Weight in kg") 
    height = models.FloatField(help_text="Height in cm")
    created_at = models.DateTimeField(auto_now_add=True)
    dietary_preferences = models.CharField(max_length=255)
    fitness_goal = models.CharField(max_length=20, choices=FITNESS_GOALS)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS)
    vegan_preference = models.BooleanField(default=False)
    bmi = models.FloatField(null=True, blank=True)
    bmr = models.FloatField(null=True, blank=True)
    plan_data = models.JSONField(help_text="Stores generated meal plan structure")
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"MealPlan #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

class FoodNutrition(models.Model):
    food_name = models.CharField(max_length=255, unique=True)
    nutrition_data = models.JSONField(help_text="Stores calories, protein, carbs, fat, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['food_name']),
        ]
        verbose_name_plural = "Food Nutrition Data"

    def __str__(self):
        return f"{self.food_name} Nutrition Data"

class ImageAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_analyses')
    image = models.ImageField(upload_to='analysis_images/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)
    analysis_result = models.JSONField(help_text="Raw analysis from AI model", null=True,blank=True)
    nutrition_data = models.JSONField( help_text="Processed nutrition information", null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['uploaded_at']),
            models.Index(fields=['user']),
        ]
        verbose_name_plural = "Image Analyses"

    def __str__(self):
        return f"Image Analysis #{self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if self.analysis_result and not self.analyzed_at:
            self.analyzed_at = timezone.now()
        super().save(*args, **kwargs)