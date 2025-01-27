from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def create_superuser(self, email, password, **extra_fields):
        """Crea e salva un superuser."""
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self.create_user(email, password, **extra_fields)


# Modello personalizzato per l'utente
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modello utente personalizzato"""
    DISEASE_TYPES = [('visiva', 'Visiva'),
                     ('uditiva', 'Uditiva'),
                     ('tattile', 'Tattile')]
    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=50, verbose_name='nome', blank=True)
    last_name = models.CharField(max_length=50, verbose_name='cognome', blank=True)
    birth_date = models.DateField(verbose_name='data di nascita', blank=True, null=True)
    disease_type = models.CharField(
        max_length=20,
        verbose_name='tipo di malattia',
        blank=True,
        null=True,
        choices=DISEASE_TYPES
    )

    # Permessi
    is_active = models.BooleanField(default=True, verbose_name='attivo')
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    is_superuser = models.BooleanField(default=False, verbose_name='superuser')

    # Impostazioni per il manager personalizzato: questa riga lo collega
    objects = CustomUserManager()

    # Campo usato per il login
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
