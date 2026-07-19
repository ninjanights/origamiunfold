# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from session_io import SessionService

from api.serializers import ChatSerializer
from rag_engine.generator.answer_service import AnswerService
from sessions.manager import SessionManager

from services.upload_service import UploadService

upload_service = UploadService()
answer_service = AnswerService()
session_manager = SessionManager()
session_service = SessionService()


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

    session = session_service.get_or_create_session(request)

    upload_service.upload(
        uploaded_file,
        session,
    )

    response = Response(
        {
            "filename": uploaded_file.name,
        },
        status=status.HTTP_201_CREATED,
    )

    session_service.refresh_session(
        response,
        session,
    )

    return response


@api_view(["POST"])
def chat(request):
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        session = session_service.get_active_session(request)
    except FileNotFoundError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    result = answer_service.answer(
        question=serializer.validated_data["question"],
        session=session,
    )

    response = Response(result)

    session_service.refresh_session(
        response,
        session,
    )

    return response
