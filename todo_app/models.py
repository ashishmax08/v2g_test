from django.db import models

# Create your models here.

class ToDo(models.Model):
	
	TASK_STATE = (
		('pending','PENDING'),
		('progress','IN-PROGRESS'),
		('done','DONE'),
		)
	date = models.DateField()
	text = models.CharField(max_length=500,null=False)
	state = models.CharField(max_length=10,choices = TASK_STATE)

	def __str__(self):
		return "{} - {}".format(self.id,self.date)