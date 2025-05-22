# api/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.meal_plan import generate_meal_plan as generate_plan_service, MealPlanGenerator, calculate_bmi, calculate_bmr
from api.utils import analyze_food_image, format_food_details, get_nutritional_data, UserProfile, display_info
#from rest_framework.permissions import IsAuthenticated
from .utils import (analyze_food_image,format_food_details,get_nutritional_data,UserProfile,display_info)
from .serializers import (ImageUploadSerializer,ManualEntrySerializer,MealPlanResponseSerializer,UserProfileSerializer,MealPlanGeneratorSerializer,MealPlanSerializer)
from .models import MealPlan 

class AnalyzeImageView(APIView):  
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            image_data = request.FILES['image'].read()
            analysis_result = analyze_food_image(image_data)
            if analysis_result:
                meal_name, serving_size, ingredients = format_food_details(analysis_result)
                nutrition = get_nutritional_data(meal_name, ingredients)
                return Response({
                    'meal_name': meal_name,
                    'serving_size': serving_size,
                    'ingredients': ingredients,
                    'nutrition': nutrition
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Image analysis failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AnalyzeManualView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ManualEntrySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = serializer.validated_data
            nutrition = get_nutritional_data(data['meal_name'], data['ingredients'])
            return Response({
                'meal_name': data['meal_name'],
                'serving_size': data['serving_size'],
                'nutrition': nutrition
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# api_views.py
class MealPlanCreateView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        # use new serializere
        serializer = MealPlanGeneratorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validated_data = serializer.validated_data
            # generate meal plan use userprofile data
            user_profile = UserProfile()
            user_profile.gender = validated_data['gender']
            user_profile.date_of_birth = validated_data['date_of_birth'].strftime("%Y-%m-%d")
            user_profile.height = validated_data['height']
            user_profile.weight = validated_data['weight']
            user_profile.activity_level = validated_data['activity_level']
            user_profile.fitness_goal = validated_data['fitness_goal']
            user_profile.vegan_preference = validated_data['vegan_preference']
            
            # calculate matrix
            user_profile.calculate_age(user_profile.date_of_birth)
            user_profile.calculate_bmi()
            user_profile.calculate_bmr()
            
            # generate meal plan
            meal_plan = user_profile.generate_personalized_meal_plan()
            
            # save informatation in database
            meal_plan = MealPlan.objects.create(
                user=request.user,
                age=user_profile.age,
                height=user_profile.height,
                weight=user_profile.weight,
                activity_level=user_profile.activity_level,
                fitness_goal=user_profile.fitness_goal,
                vegan_preference=user_profile.vegan_preference,
                plan_data=meal_plan
            )
            return Response({"id": meal_plan.id}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
            
        
class MealPlanRetrieveView(APIView):
    def get(self, request, plan_id):
        try:
            meal_plan = MealPlan.objects.get(id=plan_id)
            return Response({
                "id": meal_plan.id,
                "plan": meal_plan.plan_data,
                "created_at": meal_plan.created_at
            }, status=status.HTTP_200_OK)
        except MealPlan.DoesNotExist:
            return Response({"error": "Meal plan not found"}, status=status.HTTP_404_NOT_FOUND)
class MealPlanView(APIView):
    #permission_classes = [IsAuthenticated]
    # data validation
    def get(self, request):
        plans = MealPlan.objects.filter(user=request.user)
        serializer = MealPlanSerializer(plans, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
          return Response({
                "error": "Invalid data",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            # generate meal plan
            generator = MealPlanGenerator(serializer.validated_data)
            plan_data = generator.generate()
            # database entry
            meal_plan = MealPlan.objects.create(
                **serializer.validated_data,
                plan_data=plan_data
            )
            # response serialization
            response_serializer = MealPlanResponseSerializer(meal_plan)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # error handling
            return Response({
                "error": "Internal Server Error",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class NutritionView(APIView):
   # permission_classes = [IsAuthenticated]
    def get(self, request, food_name):
        try:
            nutrition = get_nutritional_data(food_name, [])
            return Response({'nutrition': nutrition}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


