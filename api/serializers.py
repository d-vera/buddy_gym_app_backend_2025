from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Muscle, Exercise, Training


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate_email(self, value):
        """Validate that email doesn't already exist."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        """Validate that username (nickname) is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this nickname already exists.")
        return value
    
    def validate_password(self, value):
        """Validate password requirements."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # Use Django's built-in password validators
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        
        return value
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login with email or username."""
    
    email_or_username = serializers.CharField(
        required=True,
        help_text="Enter your email or username (nickname)"
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class MuscleSerializer(serializers.ModelSerializer):
    """Serializer for muscle groups."""
    
    class Meta:
        model = Muscle
        fields = ['id', 'name']


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for exercises."""
    
    muscle_name = serializers.CharField(source='muscle.name', read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'muscle', 'muscle_name', 'name', 'note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate that the exercise name is unique for this user and muscle."""
        user = self.context['request'].user
        muscle = data.get('muscle')
        name = data.get('name')
        
        # Check if we're updating an existing exercise
        if self.instance:
            # Exclude the current instance from the uniqueness check
            if Exercise.objects.filter(
                user=user,
                muscle=muscle,
                name=name
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({
                    'name': 'An exercise with this name already exists for this muscle.'
                })
        else:
            # Creating a new exercise
            if Exercise.objects.filter(user=user, muscle=muscle, name=name).exists():
                raise serializers.ValidationError({
                    'name': 'An exercise with this name already exists for this muscle.'
                })
        
        return data


class TrainingSerializer(serializers.ModelSerializer):
    """Serializer for training sessions."""
    
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    muscle_name = serializers.CharField(source='exercise.muscle.name', read_only=True)
    
    class Meta:
        model = Training
        fields = ['id', 'exercise', 'exercise_name', 'muscle_name', 'weight', 'sets', 'repetitions', 'datetime']
        read_only_fields = ['id', 'datetime']
    
    def validate_exercise(self, value):
        """Validate that the exercise belongs to the current user."""
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("You can only create trainings for your own exercises.")
        return value
    
    def validate_weight(self, value):
        """Validate that weight is positive."""
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0.")
        return value
    
    def validate_sets(self, value):
        """Validate that sets is positive."""
        if value <= 0:
            raise serializers.ValidationError("Sets must be greater than 0.")
        return value
    
    def validate_repetitions(self, value):
        """Validate that repetitions is positive."""
        if value <= 0:
            raise serializers.ValidationError("Repetitions must be greater than 0.")
        return value


class TrainingStatsSerializer(serializers.Serializer):
    """Serializer for training statistics."""
    
    exercise_id = serializers.IntegerField()
    exercise_name = serializers.CharField()
    muscle_name = serializers.CharField()
    low_weight = serializers.DecimalField(max_digits=6, decimal_places=2)
    high_weight = serializers.DecimalField(max_digits=6, decimal_places=2)
    last_weight = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_sessions = serializers.IntegerField()
