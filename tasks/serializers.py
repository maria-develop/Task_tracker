from rest_framework import serializers

from .models import Task, ParentTask
from .validators import TitleValidator


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[TitleValidator("title")])

    class Meta:
        model = Task
        fields = '__all__'
        # read_only_fields = ('user',)


class ParentTaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[TitleValidator("title")])

    class Meta:
        model = ParentTask
        fields = '__all__'
