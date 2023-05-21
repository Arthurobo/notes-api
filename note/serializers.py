from rest_framework import serializers
from .models import Note
from accounts.models import Account, Profile
from .documents import NoteDocument
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class NotesListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = '__all__'


class NotesCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = ['title', 'content']


class NoteShareSerializer(serializers.ModelSerializer):
    invites = serializers.EmailField()
    class Meta:
        model = Note
        fields = ['invites']


# Note Serializer for ElasticSearch
class NoteDocumentSerializer(DocumentSerializer):
    class Meta(object):
        """ Meta Options """
        model = Note.objects.all()
        document = NoteDocument
        fields = '__all__'
     
        def get_location(self, obj):
            """ Represents location Value """
            try:
                return obj.location.to_dict()
            except:
                return {}
            