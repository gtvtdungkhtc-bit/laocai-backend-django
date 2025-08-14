from django.db import models
from django.contrib.auth.models import User

class Road(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True, unique=False)
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=100, blank=True, null=True)
    owner_unit = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    commune = models.CharField(max_length=100, blank=True, null=True)
    start = models.CharField(max_length=255, blank=True, null=True)
    end = models.CharField(max_length=255, blank=True, null=True)
    length_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bn = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    road = models.ForeignKey(Road, on_delete=models.CASCADE, related_name='assets', null=True, blank=True)
    road_name = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.kind} - {self.road_name or (self.road.name if self.road else '')}"

class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255, blank=True, null=True)
    total_budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    planned_capital = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    disbursed = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    progress_pct = models.IntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    commune = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Chủ đầu tư'),
        ('commune', 'Xã/Phường'),
        ('viewer', 'Chỉ xem'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    unit = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
