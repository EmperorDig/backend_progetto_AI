from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Manager personalizzato per gestire la creazione di utenti
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Crea e salva un utente normale."""
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Cripta la password
        user.save(using=self._db)  # Salva l'utente nel database
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=50, verbose_name='nome', blank=True)
    last_name = models.CharField(max_length=50, verbose_name='cognome', blank=True)
    birth_date = models.DateField(verbose_name='data di nascita', blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name='attivo')
    # Impostazioni per il manager personalizzato: questa riga lo collega
    objects = CustomUserManager()
    # Campo usato per il login
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modello per il paziente
class PatientUser(BaseUser):
    DISEASE_TYPES = [('visiva', 'Visiva'),
                     ('uditiva', 'Uditiva'),
                     ('tattile', 'Tattile')]
    disease_type = models.CharField(
        max_length=20,
        verbose_name='tipo di malattia',
        blank=True,
        null=True,
        choices=DISEASE_TYPES
    )

# Modello per il dottore
class DoctorUser(BaseUser):
    """
    in patients c'è la relazione coi pazienti, la relazione tra paziente
    e dottore è generata automaticamente nell'altro modello
    """
    patients = models.ManyToManyField(
        'PatientUser',
        related_name='doctors',
        blank=True,
        verbose_name='pazienti'
    )
