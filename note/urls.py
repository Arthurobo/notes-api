from django.urls import path
from .views import (NotesAPIView, 
                    NotesRetrieveUpdateDestroyAPIView, 
                    NoteShareAPIView, 
                    NoteDocumentView,
                    InvitedNotesAPIView
                )

app_name = 'note'

urlpatterns = [
    path('notes/', NotesAPIView.as_view(), name='notes'),
    path('notes/<int:id>/', NotesRetrieveUpdateDestroyAPIView.as_view(), name='notes-update-delete'),
    path('notes/<int:id>/share/', NoteShareAPIView.as_view(), name='notes-share'),
    path('search/' , NoteDocumentView.as_view({'get': 'list'})),
    path('invited-notes/', InvitedNotesAPIView.as_view(), name='my-notes'),
]
