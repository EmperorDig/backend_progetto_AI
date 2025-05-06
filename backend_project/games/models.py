from django.db import models

class Gioco(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Proprieta(models.Model):
    TIPO_VALORE_CHOICES = [
        ('string', 'Stringa'),
        ('int', 'Intero'),
        ('float', 'Virgola mobile'),
    ]

    nome = models.CharField(max_length=100)
    tipo_valore = models.CharField(max_length=10, choices=TIPO_VALORE_CHOICES)
    descrizione = models.TextField(blank=True, null=True)
    giochi = models.ManyToManyField('Gioco', related_name="proprieta")

    def __str__(self):
        return self.nome

class Partita(models.Model):
    gioco = models.ForeignKey(Gioco, on_delete=models.CASCADE, related_name="partite")
    punteggio = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Partita {self.id} di {self.gioco.nome}"

class ValoreProprietaPartita(models.Model):
    partita = models.ForeignKey(Partita, on_delete=models.CASCADE, related_name="valori_partita")
    proprieta = models.ForeignKey(Proprieta, on_delete=models.CASCADE, related_name="valori_propieta")
    valore = models.CharField(max_length=255)  # Puoi adattare il tipo in base a `tipo_valore`

    def __str__(self):
        return f"{self.partita} - {self.proprieta.nome}: {self.valore}"
