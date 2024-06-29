from rest_framework import serializers
from personalize.models import Personalize

class PersonalizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalize
        fields = '__all__'
