from rest_framework import serializers
from .models import Gioco, Partita, Proprieta, ValoreProprietaPartita

class GiocoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gioco
        fields = '__all__'

class ProprietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proprieta
        fields = '__all__'

class PartitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partita
        fields = '__all__'

class ValoreProprietaPartitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValoreProprietaPartita
        fields = '__all__'

    def validate(self, data):
        tipo = data['proprieta'].tipo_valore
        valore = data['valore']

        try:
            if tipo == 'int':
                int(valore)
            elif tipo == 'float':
                float(valore)
            elif tipo == 'string':
                str(valore)
            else:
                raise serializers.ValidationError("Tipo di valore non supportato.")
        except ValueError:
            raise serializers.ValidationError(f"Valore '{valore}' non è valido per il tipo {tipo}.")

        return data
