from rest_framework import serializers
from .models import Cure

class CureSerializer(serializers.ModelSerializer):
    # turtle = serializers.ReadOnlyField(source='turtle.email')

    class Meta:
        model = Cure
        fields = ['id','created','stretch','status','user_email']
