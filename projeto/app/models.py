from django.db import models

# Create your models here.
class Station(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateField()

    def __str__(self):
	    return self.name 
    # Essa função vai alterar a forma como o nome da classe será
    # apresentado no site
