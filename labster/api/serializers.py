from rest_framework import serializers

from labster.models import UserSave, ErrorInfo, DeviceInfo, UserAttempt


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

    save_file = serializers.FileField(required=True, allow_empty_file=True)

    class Meta:
        model = UserSave
        fields = ('id', 'user', 'save_file')
        read_only_fields = ('user',)


class UserAttemptSerializer(serializers.ModelSerializer):

    play = serializers.IntegerField(required=True)

    class Meta:
        model = UserAttempt
        fields = ('id', 'user', 'is_finished', 'play')
        read_only_fields = ('user', 'is_finished')


class FinishLabSerializer(serializers.ModelSerializer):

    is_finished = serializers.BooleanField(required=True)

    class Meta:
        model = UserAttempt
        fields = ('id', 'user', 'is_finished')
        read_only_fields = ('user',)

    def validate_is_finished(self, attrs, source):
        if attrs.get(source) is False:
            raise serializers.ValidationError("is_finished is required")
        return attrs


class ErrorInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ErrorInfo
        fields = (
            'id', 'user', 'browser', 'user_agent', 'os', 'message', 'created_at')
        read_only_fields = ('user', 'created_at')


class DeviceInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceInfo
        fields = (
            'id', 'user', 'device_id', 'frame_rate', 'machine_type', 'os',
            'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate',
            'shader_level', 'quality', 'misc', 'created_at')
        read_only_fields = ('user', 'created_at')
