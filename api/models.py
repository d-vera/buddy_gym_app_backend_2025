from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):
    """Custom user manager for User model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with email as the unique identifier."""
    
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150, unique=True, db_column='user')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email


class Muscle(models.Model):
    """Model representing muscle groups available for training."""
    
    MUSCLE_CHOICES = [
        ('back', 'Back'),
        ('biceps', 'Biceps'),
        ('chest', 'Chest'),
        ('triceps', 'Triceps'),
        ('shoulders', 'Shoulders'),
        ('abs', 'Abs'),
        ('legs', 'Legs'),
        ('glutes', 'Glutes'),
        ('arms', 'Arms'),
    ]
    
    name = models.CharField(max_length=50, choices=MUSCLE_CHOICES, unique=True)
    
    class Meta:
        db_table = 'muscles'
    
    def __str__(self):
        return self.get_name_display()


class Exercise(models.Model):
    """Model representing exercises created by users for specific muscles."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exercises'
        unique_together = ['user', 'muscle', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.muscle.name}) - {self.user.username}"


class Training(models.Model):
    """Model representing individual training sessions."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainings')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='trainings')
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    sets = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'training'
        ordering = ['-datetime']
    
    def __str__(self):
        return f"{self.exercise.name} - {self.weight}kg x {self.sets}x{self.repetitions} ({self.datetime})"
