from rest_framework import generics, permissions, status
from .models import Health
from .serializers import HealthSerializer
from rest_framework.response import Response
import joblib
from joblib import load
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

# health data post and view/get
class HealthApiView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    # Load the label encoder for the target variable
    label_encoder = LabelEncoder()
    label_encoder.classes_ = pd.read_pickle('./Notebooks/label_encoder') # when it was crying about no such file or directory, this was the problem


    # Load the saved model
    best_model = joblib.load('./SavedModels/best_model.joblib')

    def list(self, request): # this is also the GET method

        user = request.user
        queryset = Health.objects.all().filter(owner=user)
        serializer = HealthSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request): # posting health data from UI

        serializer = HealthSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.validated_data['owner'] = user
            gender = serializer.validated_data.get('Gender')
            age = float(serializer.validated_data.get('Age'))
            height = float(serializer.validated_data.get('Height'))
            weight = float(serializer.validated_data.get('Weight'))
            family_history = serializer.validated_data.get('Family_history_overweight')
            favc = serializer.validated_data.get('FAVC')
            fcvc = float(serializer.validated_data.get('FCVC'))
            ncp = float(serializer.validated_data.get('NCP'))
            caec = serializer.validated_data.get('CAEC')
            smoke =serializer.validated_data.get('Smoke')
            ch2o = float(serializer.validated_data.get('CH2O'))
            scc = serializer.validated_data.get('SCC')
            faf = float(serializer.validated_data.get('FAF'))
            tue = float(serializer.validated_data.get('TUE'))
            calc = serializer.validated_data.get('CALC')
            mtrans = serializer.validated_data.get('MTRANS')

            # Prepare input data
            data = pd.DataFrame({
                'Gender': [gender],
                'Age': [age],
                'Height': [height],
                'Weight': [weight],
                'family_history_with_overweight': [family_history],
                'FAVC': [favc],
                'FCVC': [fcvc],
                'NCP': [ncp],
                'CAEC': [caec],
                'SMOKE': [smoke],
                'CH2O': [ch2o],
                'SCC': [scc],
                'FAF': [faf],
                'TUE': [tue],
                'CALC': [calc],
                'MTRANS': [mtrans]
            })

            # Make prediction using the loaded model
            prediction = self.best_model.predict(data)
            #result_label.config(text="Predicted obesity level: {}".format(label_encoder.inverse_transform(prediction)[0]))
            result_label = "Predicted obesity level: " + format(self.label_encoder.inverse_transform(prediction)[0])

            serializer.validated_data['Health_Status'] = str(result_label)

            serializer.save()
            return Response(str(result_label), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)
            


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# health data detail view
class HealthDetailApiView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Health.objects.all()
    serializer_class = HealthSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_delete(self, instance):
        instance.delete()
