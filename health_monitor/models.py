from django.db import models
from django.conf import settings

#our explicit database which will handle data from user and ML model
class Health(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='user_health')
    Gender = models.CharField(max_length = 10,null=False, blank=False)
    Age = models.IntegerField()
    Height = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    Weight = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    Family_history_overweight = models.CharField(max_length = 10,null=False, blank=False)
    FAVC = models.CharField(max_length = 10,null=False, blank=False)
    FCVC = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    NCP = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    CAEC = models.CharField(max_length = 10)
    Smoke = models.CharField(max_length = 10)
    CH2O = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    SCC = models.CharField(max_length = 10)
    FAF = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    TUE = models.DecimalField(max_digits = 5, decimal_places = 2,null=False, blank=False)
    CALC = models.CharField(max_length = 10,null=False, blank=False)
    MTRANS = models.CharField(max_length = 50)
    Health_Status = models.CharField(max_length = 30,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner)
       # return self.Gender + "       " + self.Health_Status this one works
        #return  str(self.Gender, self.Health_Status) it raises error