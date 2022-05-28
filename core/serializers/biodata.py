
from rest_framework import serializers
from core.models import Profile



class BiodataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["level", "department", "part", "matric_no", "birthday", "gender"]