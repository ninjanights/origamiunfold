from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from services.upload_service import UploadService

upload_service = UploadService()


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload(request):
    print(request.FILES)
    print(request.data)

    uploaded_file = request.FILES.get("file")
    
    

    if uploaded_file is None:
        return Response(
            {"error": "No file uploaded."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    session = upload_service.upload(uploaded_file)

    return Response(
        {
            "session_id": session.session_id,
            "filename": uploaded_file.name,
        },
        status=status.HTTP_201_CREATED,
    )
