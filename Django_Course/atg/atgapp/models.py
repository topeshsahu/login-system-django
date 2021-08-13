from django.db import models
class Information(models.Model):
	fname = models.CharField(max_length=20)
	lname = models.CharField(max_length=20)
	email = models.EmailField()

	def __str__(self):
		return f"{self.fname} ,{self.lname} ,{self.email}"
