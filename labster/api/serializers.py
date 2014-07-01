from rest_framework import serializers

from labster.models import Problem, UserSave


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


class ProblemSerializer(serializers.ModelSerializer):

    content_html = serializers.Field(source='content_html')

    class Meta:
        model = Problem
        fields = ('id', 'content_markdown', 'content_xml', 'content_html', 'quiz_block')
        write_only_fields = ('content_markdown',)


class UserSaveSerializer(serializers.ModelSerializer):        

    class Meta:
        model = UserSave
        fields = ('id', 'user', 'lab_proxy', 'save_file')        
        
