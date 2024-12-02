from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    no_of_enquires = models.PositiveIntegerField()
    
    def __str__(self):
        return self.username.username
    
class History(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    text = models.TextField()
    result = models.CharField(max_length=100)
    model_used = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username.username