from rest_framework import serializers

from labster.models import UserSave, ErrorInfo, DeviceInfo


class LabSerializer(serializers.Serializer):

    id = serializers.Field(source='id')
    name = serializers.Field(source='name')
    description = serializers.Field(source='description')

    quizblocks = serializers.SerializerMethodField('get_quizblocks')

    def get_quizblocks(self, obj):
        return [qb.to_json() for qb in obj.quizblock_set.all()]


class LabProxySerializer(serializers.Serializer):

    id = serializers.Field(source='id')
    location_id = serializers.Field(source='location_id')

    lab = serializers.SerializerMethodField('get_lab')
    quizblocks = serializers.SerializerMethodField('get_quizblocks')

    def get_lab(self, obj):
        return obj.lab.to_json()

    def get_quizblocks(self, obj):
        return [qb.to_json() for qb in obj.quizblock_set.all()]


class UserSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSave
        fields = ('id', 'user', 'lab_proxy', 'save_file')


class ErrorInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ErrorInfo
        fields = ('id', 'user', 'lab_proxy', 'browser', 'os', 'message', 'date_encountered')


class DeviceInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceInfo
        fields = ('id', 'user', 'lab_proxy', 'device_id', 'frame_rate', 'machine_type', 'os',
                  'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate',
                  'shader_level', 'quality', 'misc', 'created_at')
