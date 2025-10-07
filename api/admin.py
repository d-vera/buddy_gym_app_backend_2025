from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Muscle, Exercise, Training


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Muscle)
class MuscleAdmin(admin.ModelAdmin):
    """Admin configuration for Muscle model."""
    
    list_display = ['name']
    search_fields = ['name']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin configuration for Exercise model."""
    
    list_display = ['name', 'muscle', 'user', 'created_at']
    list_filter = ['muscle', 'created_at']
    search_fields = ['name', 'user__email', 'user__username']
    date_hierarchy = 'created_at'


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    """Admin configuration for Training model."""
    
    list_display = ['exercise', 'user', 'weight', 'sets', 'repetitions', 'datetime']
    list_filter = ['datetime', 'exercise__muscle']
    search_fields = ['exercise__name', 'user__email', 'user__username']
    date_hierarchy = 'datetime'
