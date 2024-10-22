from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('coach', 'Coach'),
        ('agent', 'Agent'),
        ('player', 'Football Player'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')  # Default role is 'player'

    def is_admin(self):
        return self.role == 'admin'

    def is_coach(self):
        return self.role == 'coach'

    def is_agent(self):
        return self.role == 'agent'

    def is_player(self):
        return self.role == 'player'


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
