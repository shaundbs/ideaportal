from rest_framework import serializers

from .models import Idea, Department
from blog.models import Post
from organisations.models import Organisation

class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Department
        fields = ('id','department',)

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('id','name','description', 'created_on')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title', 'description', 'created_on', 'startDate', 'endDate', 'winner')

class IdeaSerializer(serializers.HyperlinkedModelSerializer):
    post = PostSerializer(read_only=True)
    org_tag = OrganisationSerializer(read_only=True, many=True)
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Idea
        fields = ('id', 'title', 'estimated_cost', 'description', 'post', 'stage', 'org_tag', 'department')
        read_only_fields = ('id', 'title', 'estimated_cost', 'description', 'post')