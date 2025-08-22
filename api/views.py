from rest_framework import viewsets, status, mixins, generics
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import request

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate

# Meals (create, retrieve, update, partial_update, destroy, list) + Stars (create or update)
# using viewsets & routers
class MealViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes= [IsAuthenticatedOrReadOnly]

    queryset= Meal.objects.all()
    serializer_class= MealSerializer

    """
    - Basic role of the CreateOrUpdate_stars_meal method :
    ** Update or create a rate for a specific Meal
    - Endpoint :
    ** 172.0.0.1/meals/<str:pk>/CreateOrUpdate_stars_meal
    - Requirements :
    ** stars + username from request (because we are not filtering, we'll create or update)
    ** pk from url
    
    """
    @action(methods=['put','post'], detail=True) # detail=True because we want to get one instance
    def CreateOrUpdate_stars_meal(self, request, pk=None):
        if "stars" in request.data :
                try:
                    meal = Meal.objects.get(id=pk)
                except Meal.DoesNotExist:
                    return Response({'error': 'Meal not found!'}, status=status.HTTP_404_NOT_FOUND)
        
                user=request.user

                stars= request.data["stars"]
                if not '1' <= stars <= '5':
                    return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    rating = Rating.objects.get(meal=meal.id, user=user.id)
                    rating.stars= stars
                    rating.save() # to update 
                    serializer= RatingSerializer(rating, many=False) # ,many= True when we have more than one entry
                    return Response({
                        "message":"Rating Updated !",
                        "result": serializer.data
                        }, status=status.HTTP_200_OK)
                except Rating.DoesNotExist:
                    rating= Rating.objects.create(meal=meal, user=user,stars=stars)
                    serializer= RatingSerializer(rating, many=False) 
                    return Response({
                        "message":"New Rating Created !",
                        "result": serializer.data
                        }, status=status.HTTP_201_CREATED)
        return Response({"message":"Body not provided !"}, status=status.HTTP_400_BAD_REQUEST)
  
    """
    - Basic role of the stats method :
    ** Get stats and records of a meal
    - Endpoint :
    ** 172.0.0.1/meals/<str:pk>/stats
    - Requirements :
    ** pk from url
    
    """
    @action(methods=['get'], detail=True)
    def stats(self, request, pk=None):
        meal= Meal.objects.get(id=pk)
        serializer= MealSerializer(meal, many=False)
        ratings= Rating.objects.filter(meal=meal)
        serializer2= RatingSerializer(ratings,many=True)
        return Response({
            "count": serializer.data["ratings_count"],
            "avg": serializer.data["avg_ratings"],
            "records":serializer2.data,
        })
            

# list, retrieve and destroy 
class RatingViewSet(viewsets.ModelViewSet):
    
    authentication_classes=[TokenAuthentication]
    permission_classes= [IsAuthenticated]


    queryset= Rating.objects.all()
    serializer_class= RatingSerializer

    # override
    def update(self, request, *args, **kwargs):
        return Response({"mesage":"Can't update a Rating from this endpoint !"},
                        status=status.HTTP_403_FORBIDDEN)
    
    # override
    def create(self, request, *args, **kwargs):
        return Response({"mesage":"Can't create a Rating from this endpoint !"},
                        status=status.HTTP_403_FORBIDDEN)

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes= [AllowAny]

    queryset= User.objects.all()
    serializer_class= UserSerializer

    # override
    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
                return super().list(request, *args, **kwargs)
        return Response(
                {"message": "You can't see the users list of the app!"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    # override
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response({"message": "Deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"message": "Denied Access!"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # override
    def update(self, request, *args, **kwargs):
        instance = self.get_object()  
        if request.user == instance or request.user.is_superuser:
            return super().update(request, *args, **kwargs)

        return Response(
            {"message": "Denied Access!"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # override
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  
        if request.user == instance or request.user.is_superuser:
            return super().retrieve(request, *args, **kwargs)

        return Response(
            {"message": "Denied Access!"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    @action(methods=['post'], detail=False) 
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials !"}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.id,
            "username": user.username,
            "token": token.key
        }, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete() 
        return Response({"message": "Successfully logged out !"},
                        status=status.HTTP_200_OK)