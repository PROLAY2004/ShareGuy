from django.db import models

# Create your models here.
class data_records(models.Model):
    id = models.AutoField
    file = models.FileField(upload_to="Files", default=0)
    code = models.CharField(max_length=6)
    qr = models.FileField(upload_to="QRcodes", default=0)
    inserttime = models.DateTimeField()

    def __str__(self):
        return self.code

