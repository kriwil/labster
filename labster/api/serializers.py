from rest_framework import serializers


class LabSerializer(serializers.Serializer):

    id = serializers.Field(source='id')
    name = serializers.Field(source='name')
    description = serializers.Field(source='description')

    quizblocks = serializers.SerializerMethodField('get_quizblocks')

    def get_quizblocks(self, obj):
        return [qb.to_json() for qb in obj.quizblock_set.all()]
