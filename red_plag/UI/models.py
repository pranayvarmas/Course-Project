from django.db import models
import os
class Profile(models.Model):
   #name = models.CharField(max_length = 50)
    picture = models.FileField(upload_to = '')
    def name(self):
        return os.path.basename(self.picture.name)

    class Meta:
      db_table = "profile"