from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError

""" Elasticsearch Imports """
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
)

from accounts.models import Account, Profile
from .models import Note
from .documents import NoteDocument
from .serializers import (NotesListSerializer, 
                          NotesCreateSerializer, 
                          NoteShareSerializer, 
                          NoteDocumentSerializer
                        )


class NotesAPIView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NotesListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Note.objects.all()
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotesCreateSerializer
        else:
            return NotesListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        message = 'Success'
        status_code = 200
        return Response({'status': status_code, 'message': message, 'data': data}, status=status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.profile)
            message = 'Data saved successfully'
            status_code = 201
            data = serializer.data
            return Response({'status': status_code, 'message': message, 'data': data}, status=status_code)
        else:
            message = 'Data could not be saved'
            status_code = 400
            return Response({'status': status_code, 'message': message, 'errors': serializer.errors}, status=status_code)
        

class InvitedNotesAPIView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NotesListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(invites=user.profile)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        message = 'Success'
        status_code = 200
        return Response({'status': status_code, 'message': message, 'data': data}, status=status_code)


class NotesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NotesListSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return NotesCreateSerializer
        else:
            return NotesListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the authenticated user is the owner of the instance
        if instance.user != request.user.profile:
            raise PermissionDenied("You do not have permission to delete this object.")
        
        # Perform the deletion
        self.perform_destroy(instance)
        return Response("Object deleted successfully.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Check if the authenticated user is the owner of the instance
        if instance.user != request.user.profile:
            raise PermissionDenied("You do not have permission to update this object.")

        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class NoteShareAPIView(generics.RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteShareSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        invited_email = serializer.validated_data.get('invites')

        # Check if the authenticated user is the owner of the instance
        if instance.user != request.user.profile:
            raise PermissionDenied("You do not have permission to update this object.")
        
        else:
            try:
                # Check if the email exists in the Account model
                account = Account.objects.get(email=invited_email)
                print(account)

                # Check if the email has been invited
                invited_profile = Profile.objects.filter(user=account).first()

                if invited_profile in instance.invites.all():
                    raise ValidationError("Invitation already sent to this email, they already have access.")
                else:
                    account = Account.objects.get(email=invited_email)
                    profile = Profile.objects.filter(user=account).first()
                    instance.invites.add(profile)
                    print("Invitation sent successfully")
                    response_data = {
                        'status': 'success',
                        'message': 'Invitation sent successfully'
                        }
                    return Response(response_data, status=status.HTTP_200_OK)
                
            except Account.DoesNotExist:
                raise NotFound("The account you're trying to invite does not exist")


# ElasticSearch Serializer Search View
class NoteDocumentView(DocumentViewSet):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    document = NoteDocument
    serializer_class = NoteDocumentSerializer
    lookup_field = "title"
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = (
        "title",
        "content",
    )

    multi_match_search_fields = (
        "title",
        "content",
    )

    filter_fields = {
        "title": "title",
        "content": "content",
    }

    ordering_fields = {
        'id': None,
    }

    ordering = ("id",)