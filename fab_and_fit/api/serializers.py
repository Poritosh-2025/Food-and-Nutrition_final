from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, MealPlan, FoodNutrition, ImageAnalysis 
from .constants import ACTIVITY_LEVEL_CHOICES, FITNESS_GOAL_CHOICES

'''class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user'''
    
    # mealplan

class ImageAnalysisSerializer(serializers.Serializer):
    class Meta:
        model = ImageAnalysis
        fields = ['image']

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['id', 'plan_data', 'created_at']
        read_only_fields = ('created_at', 'bmi', 'bmr')
# serializers.py

class MealPlanGeneratorSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'])
    date_of_birth = serializers.DateField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    activity_level = serializers.ChoiceField(
        choices=['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active']
    )
    fitness_goal = serializers.ChoiceField(
        choices=['Weight Loss', 'Muscle Gain', 'Maintenance', 'General Fitness']
    )
    vegan_preference = serializers.BooleanField()

    class Meta:
        model = MealPlan
        fields = ['age', 'weight', 'height', 'activity_level', 'fitness_goal', 'vegan_preference']


class MealPlanResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'
        read_only_fields = ['plan_data']

class FoodNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodNutrition
        fields = ['food_name', 'nutrition_data', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

class NutritionRequestSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.CharField())

class UserProfileSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=['male', 'female'], required=True)
    activity_level = serializers.ChoiceField(
        choices=[choice[0] for choice in ACTIVITY_LEVEL_CHOICES])
    fitness_goal = serializers.ChoiceField(
        choices=[choice[0] for choice in FITNESS_GOAL_CHOICES])
    class Meta:
        model = UserProfile
        fields = [
            'gender', 'age', 'height', 'weight', 
            'activity_level', 'fitness_goal', 
            'vegan_preference', 'dietary_preferences'
        ]


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

class ManualEntrySerializer(serializers.Serializer):
    meal_name = serializers.CharField(max_length=255)
    ingredients = serializers.ListField(child=serializers.CharField())
    serving_size = serializers.IntegerField(default=100)

class UserProfileSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=['male', 'female'])
    date_of_birth = serializers.DateField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    activity_level = serializers.ChoiceField(
        choices=['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active']
    )
    fitness_goal = serializers.ChoiceField(
        choices=['Weight Loss', 'Muscle Gain', 'Maintenance', 'General Fitness']
    )
    vegan_preference = serializers.BooleanField()