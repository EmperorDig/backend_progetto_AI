from django.db import models

class AudioData(models.Model):
    #associeted_audio_id = models.IntegerField()
    stutter_percentage = models.FloatField(default=0)
    word_matches = models.JSONField(default=list, blank=True, null=True)
    syllable_matches = models.JSONField(default=list, blank=True, null=True)
    letter_matches = models.JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return str(self.id)

class Audio(models.Model):
    name = models.CharField(max_length=30)
    audio_file = models.FileField(upload_to='audio_files/')
    length = models.FloatField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    audio_data = models.OneToOneField(AudioData, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.audio_file.name