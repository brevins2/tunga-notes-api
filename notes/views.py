from django.shortcuts import render
from django.http import HttpResponse
from .models import Notes
from rest_framework.decorators import api_view
from .serializers import notesSerializers
from rest_framework import status
from rest_framework.response import Response


# read notes from the table
@api_view(['GET'])
def getAllNotes(request):
    notes = Notes.objects.all()
    serializer = notesSerializers(notes, many=True)
    return Response(serializer.data)


# Read one single notes 
@api_view(['GET'])
def getSingleNotes(request, pk=None):
    try:
        instance = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        return Response({'message': 'Notes not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = notesSerializers(instance)
    return Response(serializer.data)


# add notes to table
@api_view(['POST'])
def createNotes(request):
    serializer = notesSerializers(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# updata a notes in the table
@api_view(['PUT'])
def updateSingleNotes(request, notes_id):
    user = request.data.get('user')
    content = request.data.get('content')
    due_date = request.data.get('due_date')
    priority = request.data.get('priority')
    created_time = request.data.get('created_time')
    is_finished = request.data.get('is_finished')
    title = request.data.get('title')
    notes = Notes.objects.filter(id=notes_id).first()

    if notes is None:
        response_data = { "response": "Notes does not exist" }
        return Response(response_data, status = status.HTTP_404_NOT_FOUND)

    notes.title = title
    notes.user_id = user
    notes.content = content
    notes.due_date = due_date
    notes.priority = priority
    notes.created_time = created_time
    notes.is_finished = is_finished
    notes.save()
    response_data = { "response": "Item updated" }
    return Response(response_data, status = status.HTTP_200_OK)


# delete single notes from the table
@api_view(['DELETE'])
def deleteSingleNotes(request, notes_id):
    try:
        notes = Notes.objects.get(id=notes_id)
        notes.delete()
        # return HttpResponse('Notes deleted', status=204)
        response_data = { "response": "Notes deleted" }
        return Response(response_data, status = status.HTTP_200_OK)
    except Notes.DoesNotExist:
        return HttpResponse('Notes not found', status=404)
