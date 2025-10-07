from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.db.models import Min, Max, Q
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import User, Muscle, Exercise, Training
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    MuscleSerializer,
    ExerciseSerializer,
    TrainingSerializer,
    TrainingStatsSerializer
)
from .authentication import generate_jwt_token


@extend_schema(
    tags=['Authentication'],
    request=UserRegistrationSerializer,
    responses={201: UserSerializer},
    description='Register a new user with email, password, first name, last name, and username (nickname)'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_serializer = UserSerializer(user)
        return Response({
            'user': user_serializer.data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Authentication'],
    request=UserLoginSerializer,
    responses={200: {
        'type': 'object',
        'properties': {
            'token': {'type': 'string'},
            'user': {'type': 'object'}
        }
    }},
    description='Login with email and password to receive a JWT token'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login a user and return JWT token."""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            token = generate_jwt_token(user)
            user_serializer = UserSerializer(user)
            return Response({
                'token': token,
                'user': user_serializer.data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Authentication'],
    responses={200: UserSerializer},
    description='Get current authenticated user profile'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(tags=['Muscles'])
class MuscleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing muscle groups."""
    
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Exercises'])
class ExerciseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing exercises."""
    
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return exercises for the current user only."""
        return Exercise.objects.filter(user=self.request.user).select_related('muscle')
    
    def perform_create(self, serializer):
        """Create an exercise for the current user."""
        serializer.save(user=self.request.user)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='muscle',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter exercises by muscle ID'
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """List all exercises for the current user, optionally filtered by muscle."""
        queryset = self.get_queryset()
        
        # Filter by muscle if provided
        muscle_id = request.query_params.get('muscle', None)
        if muscle_id:
            queryset = queryset.filter(muscle_id=muscle_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Training'])
class TrainingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing training sessions."""
    
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return trainings for the current user only."""
        return Training.objects.filter(user=self.request.user).select_related('exercise', 'exercise__muscle')
    
    def perform_create(self, serializer):
        """Create a training session for the current user."""
        serializer.save(user=self.request.user)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='period',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by time period: current_week, last_week, last_month, last_year',
                enum=['current_week', 'last_week', 'last_month', 'last_year']
            ),
            OpenApiParameter(
                name='exercise',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by exercise ID'
            ),
            OpenApiParameter(
                name='muscle',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by muscle ID'
            )
        ],
        description='Get training history with optional filters'
    )
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get training history with optional time period filter."""
        queryset = self.get_queryset()
        
        # Filter by time period
        period = request.query_params.get('period', None)
        if period:
            now = datetime.now()
            
            if period == 'current_week':
                # Get current week (Monday to Sunday)
                start_of_week = now - timedelta(days=now.weekday())
                start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(datetime__gte=start_date)
            
            elif period == 'last_week':
                # Get last week (Monday to Sunday)
                start_of_current_week = now - timedelta(days=now.weekday())
                end_of_last_week = start_of_current_week - timedelta(seconds=1)
                start_of_last_week = end_of_last_week - timedelta(days=6)
                start_of_last_week = start_of_last_week.replace(hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(
                    datetime__gte=start_of_last_week,
                    datetime__lte=end_of_last_week
                )
            
            elif period == 'last_month':
                # Get last 30 days
                start_date = now - timedelta(days=30)
                queryset = queryset.filter(datetime__gte=start_date)
            
            elif period == 'last_year':
                # Get last 365 days
                start_date = now - timedelta(days=365)
                queryset = queryset.filter(datetime__gte=start_date)
        
        # Filter by exercise
        exercise_id = request.query_params.get('exercise', None)
        if exercise_id:
            queryset = queryset.filter(exercise_id=exercise_id)
        
        # Filter by muscle
        muscle_id = request.query_params.get('muscle', None)
        if muscle_id:
            queryset = queryset.filter(exercise__muscle_id=muscle_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='exercise',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter stats by exercise ID'
            ),
            OpenApiParameter(
                name='muscle',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter stats by muscle ID'
            )
        ],
        responses={200: TrainingStatsSerializer(many=True)},
        description='Get training statistics including low, high, and last weight for each exercise'
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get training statistics (low, high, last weight) for each exercise."""
        queryset = self.get_queryset()
        
        # Filter by exercise
        exercise_id = request.query_params.get('exercise', None)
        if exercise_id:
            queryset = queryset.filter(exercise_id=exercise_id)
        
        # Filter by muscle
        muscle_id = request.query_params.get('muscle', None)
        if muscle_id:
            queryset = queryset.filter(exercise__muscle_id=muscle_id)
        
        # Get unique exercises from the filtered trainings
        exercises = Exercise.objects.filter(
            id__in=queryset.values_list('exercise_id', distinct=True)
        ).select_related('muscle')
        
        stats = []
        for exercise in exercises:
            exercise_trainings = queryset.filter(exercise=exercise)
            
            if exercise_trainings.exists():
                # Get min and max weights
                weight_stats = exercise_trainings.aggregate(
                    low_weight=Min('weight'),
                    high_weight=Max('weight')
                )
                
                # Get last weight (most recent training)
                last_training = exercise_trainings.first()
                
                stats.append({
                    'exercise_id': exercise.id,
                    'exercise_name': exercise.name,
                    'muscle_name': exercise.muscle.name,
                    'low_weight': weight_stats['low_weight'],
                    'high_weight': weight_stats['high_weight'],
                    'last_weight': last_training.weight,
                    'total_sessions': exercise_trainings.count()
                })
        
        serializer = TrainingStatsSerializer(stats, many=True)
        return Response(serializer.data)
