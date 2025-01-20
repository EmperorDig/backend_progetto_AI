from django.db import models
from pydub import AudioSegment

class Audio(models.Model):
    name = models.CharField(max_length=30)
    audio_file = models.FileField(upload_to='audio_files/')
    length = models.FloatField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.audio_file:
            audio = AudioSegment.from_file(self.audio_file.path)
            self.length = len(audio) / 1000.0  # Length in seconds
        super(Audio, self).save(*args, **kwargs)

    def __str__(self):
        return self.audio_file.name