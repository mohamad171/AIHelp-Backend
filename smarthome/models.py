from django.db import models
from django.utils import timezone

class Home(models.Model):
    HomeName = models.TextField(verbose_name="نام خانه")
    HomeAddress = models.TextField(verbose_name="آدرس خانه")

    def __str__(self):
        return self.HomeName
    class Meta():
        verbose_name = "خانه"
        verbose_name_plural="خانه ها"


class Bulb(models.Model):
    Home = models.ForeignKey(Home, on_delete=models.CASCADE)
    BulbName = models.TextField(verbose_name="نام لامپ")
    BublStatus = models.BooleanField(verbose_name="وضعیت لامپ")
    LastModify = models.DateTimeField(default=timezone.now, verbose_name="آخرین تغییر")
    def __str__(self):
        return self.BulbName
    class Meta():
        verbose_name = "لامپ"
        verbose_name_plural="لامپ ها"


