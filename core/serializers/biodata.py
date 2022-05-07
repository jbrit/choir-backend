
from rest_framework import serializers
from core.models import Profile



class BiodataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["level", "department", "part", "reg_no", "matric_no", "birthday", "gender"]