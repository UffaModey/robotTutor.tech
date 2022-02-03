
from django.db import models

class Program(models.Model):
    editorCode = models.CharField(max_length=30000, null=True)
    robotAPI = models.CharField(max_length=30000, null=True)
    passcodeguiapp = models.CharField(max_length=30000, null=True)
    passcodewebapp = models.CharField(max_length=30000, null=True)
    runid = models.IntegerField(null=True)

    def __str__(self):
        return self.editorCode
