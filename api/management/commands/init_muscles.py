from django.core.management.base import BaseCommand
from api.models import Muscle


class Command(BaseCommand):
    help = 'Initialize muscle groups in the database'

    def handle(self, *args, **kwargs):
        muscles = [
            'back',
            'biceps',
            'chest',
            'triceps',
            'shoulders',
            'abs',
            'legs',
            'glutes',
            'arms',
        ]
        
        created_count = 0
        for muscle_name in muscles:
            muscle, created = Muscle.objects.get_or_create(name=muscle_name)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created muscle: {muscle.get_name_display()}')
                )
        
        if created_count == 0:
            self.stdout.write(
                self.style.WARNING('All muscles already exist in the database')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} muscle groups')
            )
