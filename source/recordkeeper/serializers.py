from rest_framework import serializers

from recordkeeper.models import Person, PersonStatus, FormulaFields

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class PersonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonStatus
        fields = '__all__'

class FormulaFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaFields
        fields = '__all__'