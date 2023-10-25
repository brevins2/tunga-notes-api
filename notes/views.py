import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
from .permission import CustomAuthBackend
from django.shortcuts import render
from django.http import HttpResponse
from .models import Notes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import IsOwnerOrReadOnly
from .serializers import notesSerializers
from rest_framework import status
from rest_framework.response import Response


# read notes from the table
@api_view(['GET'])
@permission_classes([AllowAny])
def getAllNotes(request):
    notes = Notes.objects.all()
    serializer = notesSerializers(notes, many=True)
    return Response(serializer.data)


# Read one single notes 
@api_view(['GET'])
@permission_classes([AllowAny])
def getSingleNotes(request, pk=None):
    try:
        instance = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        return Response({'message': 'Notes not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = notesSerializers(instance)
    return Response(serializer.data)


# add notes to table
@api_view(['POST'])
@permission_classes([AllowAny])
def createNotes(request):
    serializer = notesSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# updata a notes in the table
@api_view(['PUT'])
@permission_classes([AllowAny])
def updateSingleNotes(request, notes_id):
    user = request.data.get('user')
    content = request.data.get('content')
    due_date = request.data.get('due_date')
    category = request.data.get('category')
    priority = request.data.get('priority')
    created_time = request.data.get('created_time')
    is_finished = request.data.get('is_finished')
    title = request.data.get('title')
    notes = Notes.objects.filter(id=notes_id).first()

    if notes is None:
        response_data = { "response": "Notes does not exist" }
        return Response(response_data, status = status.HTTP_404_NOT_FOUND)

    notes.title = title
    notes.user = user
    notes.content = content
    notes.due_date = due_date
    notes.priority = priority
    notes.created_time = created_time
    notes.is_finished = is_finished
    notes.category = category
    permission_classes = [IsOwnerOrReadOnly]
    # if user == CustomAuthBackend):
    notes.save()
    response_data = { "response": "Item updated" }
    return Response(response_data, status = status.HTTP_200_OK)


# delete single notes from the table
@api_view(['DELETE'])
@permission_classes([IsOwnerOrReadOnly])
def deleteSingleNotes(request, notes_id):
    try:
        notes = Notes.objects.get(id=notes_id)
        notes.delete()
        response_data = { "response": "Notes deleted" }
        return Response(response_data, status = status.HTTP_200_OK)
    except Notes.DoesNotExist:
        return HttpResponse('Notes not found', status=404)


# download via csv
def download_csv(request):
    # Get the data you want to include in the CSV
    data = Notes.objects.all()

    # Create a response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notes.csv"'

    # Create a CSV writer and write the data
    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Owner'])
    for note in data:
        writer.writerow([note.title, note.content, note.user])

    return response


# export pdf file
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="notes.pdf"'

    # Creates the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Defines the width and height of each row in the table
    row_height = 20
    column_width = 100

    # Defines the data to be printed in the table
    data = [
        ['ID', 'Title', 'Owner'],
    ]
    for obj in Notes.objects.all():
        data.append([obj.id, obj.title, obj.user])

    # Draw the table
    x = 50
    y = 750
    for row in data:
        for item in row:
            p.drawString(x, y, str(item))
            x += column_width
        x = 50
        y -= row_height

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response