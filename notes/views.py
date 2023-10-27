import csv
from django.conf import settings
from django.core.mail import EmailMessage

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from users.models import User
from django.shortcuts import render
from django.http import HttpResponse
from .models import Notes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import notesSerializers
from rest_framework import status
from rest_framework.response import Response


# read notes from the table
@api_view(['GET'])
@permission_classes([AllowAny])
def getAllNotes(request):
    notes = Notes.objects.all()
    serializer = notesSerializers(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
@api_view(['POST'])
def updateSingleNotes(request, notes_id):
    activeuser = Notes.objects.filter(user_id = request.data['user'], id=request.data['id'])
    notes_id = request.data['id']

    if activeuser:
        user = request.data.get('user')
        content = request.data.get('content')
        due_date = request.data.get('due_date')
        category = request.data.get('category')
        priority = request.data.get('priority')
        created_time = request.data.get('created_time')
        is_finished = request.data.get('is_finished')
        title = request.data.get('title')
        notes = Notes.objects.filter(id=notes_id).first()

        # check the user given if exists in the user's table
        try:
            user_instance = User.objects.get(pk=user)
        except User.DoesNotExist:
            response_data = {"response": "User does not exist"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        notes = Notes.objects.filter(id=notes_id).first()

        if notes is None:
            response_data = { "response": "Notes does not exist" }
            return Response(response_data, status = status.HTTP_404_NOT_FOUND)

        notes.title = title
        notes.user = user_instance
        notes.content = content
        notes.due_date = due_date
        notes.priority = priority
        notes.created_time = created_time
        notes.is_finished = is_finished
        notes.category = category
        
        notes.save()
        response_data = { "response": "Item updated" }
        return Response(response_data, status = status.HTTP_200_OK)
    else:
        return Response("You are not the author, can't update these notes")


# delete single notes from the table by author
@api_view(['POST'])
def deleteSingleNotes(request, notes_id):
    user = Notes.objects.filter(user_id = request.data['user_id'], id=request.data['id'])
    notes_id = request.data['id']
    
    if user:
        try:
            notes = Notes.objects.get(id=notes_id)
            notes.delete()
            response_data = { "response": "Notes deleted" }
            return Response(response_data, status = status.HTTP_200_OK)
        except Notes.DoesNotExist:
            return HttpResponse('Not able to delete Notes', status=404)
    else:
        return Response('Your are not the author of these notes')


# get category notes from the db
@api_view(['GET'])
@permission_classes([AllowAny])
def categorysearch(request):
    notes = Notes.objects.filter(category=request.data['category'])
    if notes:
        serialize = notesSerializers(notes, many=True)
        return Response(serialize.data)
    else:
        return Response('category doesnot exist')
    
# get notes by due_date
@api_view(['GET'])
@permission_classes([AllowAny])
def categorysearch(request):
    notes = Notes.objects.filter(due_date=request.data['due_date'])
    if notes:
        serialize = notesSerializers(notes, many=True)
        return Response(serialize.data)
    else:
        return Response('due_date doesnot exist')


# get notes by priority
@api_view(['GET'])
@permission_classes([AllowAny])
def categorysearch(request):
    notes = Notes.objects.filter(priority=request.data['priority'])
    if notes:
        serialize = notesSerializers(notes, many=True)
        return Response(serialize.data)
    else:
        return Response('priority doesnot exist')

# read notes from the table
@api_view(['GET'])
@permission_classes([AllowAny])
def getReversNotes(request):
    notes = Notes.objects.order_by('-id')
    serializer = notesSerializers(notes, many=True)
    return Response({"message": "Notes in descending order", "data": serializer.data})


# download via csv
# @api_view(['POST'])
def download_csv(request):
    # Get the data you want to include in the CSV
    data = Notes.objects.all()

    # Create a response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notes.csv"'

    # Create a CSV writer and write the data
    writer = csv.writer(response)
    writer.writerow(['Title', 'Content', 'Owner'])
    for note in data:
        writer.writerow([note.title, note.content, note.user])

    return response


# export pdf file
@api_view(['POST'])
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="notes.pdf"'
    buffer = BytesIO()

    # Creates the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Defines the width and height of each row in the table
    row_height = 20
    column_width = 150

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

    # Create an HttpResponse with the PDF
    pdf_response = HttpResponse(content_type='application/pdf')
    pdf_response['Content-Disposition'] = 'attachment; filename="notes.pdf"'
    pdf_response.write(buffer.getvalue())
    buffer.close()

    activeuser = request.data['email']

    # Send an email with the PDF attachment
    subject = 'Your Notes PDF'
    message = 'Please find your Notes PDF attached.'
    from_email = settings.EMAIL_HOST_USER
    to_email = activeuser

    email = EmailMessage(subject, message, from_email, [to_email])
    email.attach('notes.pdf', response.getvalue(), 'application/pdf')
    email.send()

    return Response(pdf_response)
