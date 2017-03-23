from django.db import models
from django.utils import timezone
import datetime

class Coordinates(models.Model):
	lat = models.DecimalField(max_digits=9, decimal_places=7)
	lon = models.DecimalField(max_digits=10, decimal_places=7)

class Units(models.Model):
	co_ordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
	capacity = models.DecimalField(max_digits=2, decimal_places=0)

	def as_dict(self):
		return {
			"id": self.id,
			"capacity": self.capacity,
			"co_ordinates": self.co_ordinates
        	}

class PowerExpected(models.Model):
	unit = models.ForeignKey(Units, on_delete=models.CASCADE)
	expected_dc = models.TextField(null=True)


class PowerActual(models.Model):
	unit = models.ForeignKey(Units, on_delete=models.CASCADE)
	stamp_date = models.DateField('stamp date')
	actual_dc = models.DecimalField(max_digits=8, decimal_places=3)

class Performance(models.Model):
	unit = models.ForeignKey(Units)
	performance_date = models.DateField() 
	hours = models.IntegerField(default=25)