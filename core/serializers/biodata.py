
from rest_framework import serializers
from core.models import Profile



class BiodataSerializer(serializers.ModelSerializer):

    reg_no = serializers.IntegerField(read_only=True)
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["level", "department", "part", "matric_no", "email", "reg_no", "birthday", "gender", "name"]

    def get_email(self, obj):
        return obj.user.email