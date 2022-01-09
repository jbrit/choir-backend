from rest_framework import serializers
from rehearsals.models import Rehearsal

class RehearsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rehearsal
        fields = "__all__"
        read_only_fields = ("id",)

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['end_time'] and data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("finish must occur after start")
 
        return super().validate(data)