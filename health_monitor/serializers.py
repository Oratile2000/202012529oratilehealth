from rest_framework.serializers import ModelSerializer
from .models import Health

# model serializer
class HealthSerializer(ModelSerializer):

    class Meta:
        model = Health
        fields = ['id', 'Gender', 'Age', 'Height', 'Weight',
         'Family_history_overweight', 'FAVC', 'FCVC','NCP', 'CAEC', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC',
         'Smoke', 'MTRANS', 'date_added', 'Health_Status']