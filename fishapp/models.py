from django.db import models

from investments_appraisal.models import UserModel


#-------------OPTIONS: FISH
class TankDesignParameters(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    num_of_tanks =  models.IntegerField(default=10)
    tank_length =  models.DecimalField(decimal_places=2, max_digits=10 , default=3.47)
    tank_width =  models.DecimalField(decimal_places=2, max_digits=10, default=3.47)
    depth =  models.DecimalField(decimal_places=2, max_digits=10 ,default=.91)
    sqm =  models.DecimalField(decimal_places=2, max_digits=10 ,default=0)
    volume_of_water =  models.DecimalField(decimal_places=2, max_digits=10, default=13285)
    density_per_cubic_metre =  models.DecimalField(decimal_places=2, max_digits=10, default=263)
    total_fish_per_tank_per_cycle =  models.IntegerField(default=3000)
    tank_num_of_months_per_cycle =  models.IntegerField(default=6)
    fish_per_tank_per_year =  models.IntegerField(default=7000)
