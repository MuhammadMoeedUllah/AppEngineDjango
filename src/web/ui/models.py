from django.db import models

# Create your models here.
class Scan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    scanned_at_local = models.DateTimeField()
    scanned_at_utc = models.DateTimeField()
    document = models.CharField(max_length=10)

class Dents(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)
    size_0_9 = models.IntegerField(default=0)
    size_10_19 = models.IntegerField(default=0)
    size_20_29 = models.IntegerField(default=0)
    size_30_39 = models.IntegerField(default=0)
    size_40_49 = models.IntegerField(default=0)
    size_50_59 = models.IntegerField(default=0)
    size_60_69 = models.IntegerField(default=0)
    size_70_79 = models.IntegerField(default=0)
    size_80_89 = models.IntegerField(default=0)
    size_90_100 = models.IntegerField(default=0)
    size_100_plus = models.IntegerField(default=0)
