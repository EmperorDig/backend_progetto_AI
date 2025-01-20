from django.db import models

class Audio(models.Model):
    name = models.CharField(max_length=30)
    audio_file = models.FileField(upload_to='audio_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.audio_file.name