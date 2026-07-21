# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .session_io import SessionService

from api.serializers import DeleteFilesSerializer
from api.serializers import ChatSerializer
from rag_engine.generator.answer_service import AnswerService
from sessions.manager import SessionManager
from services.file_service import FileService
from services.upload_service import UploadService
from django.utils.timezone import now

upload_service = UploadService()
answer_service = AnswerService()
session_manager = SessionManager()
session_service = SessionService()
file_service = FileService()


@api_view(["GET"])
def status(request):
    return Response(
        {
            "status": "active",
            "service": "OrigamiUnfold Backend",
            "framework": "Django REST Framework",
            "time": now().isoformat(),
        }
    )




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

    try:
        result = answer_service.answer(
            question=serializer.validated_data["question"],
            sources=serializer.validated_data.get("sources", []),
            session_id=session,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=503,
        )

    response = Response(result)
    session_service.refresh_session(
        response,
        session_id,
    )
    return response


@api_view(["GET"])
def files(request):
    if request.COOKIES.get(session_service.COOKIE_NAME) is None:
        return Response([])

    try:
        session = session_service.get_active_session(request)
    except FileNotFoundError as error:
        return Response(
            {
                "error": (
                    "Session expired."
                    if str(error) == "Session expired."
                    else str(error)
                )
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    files = file_service.list_files(session)

    response = Response(files)

    session_service.refresh_session(
        response,
        session,
    )

    return response


@api_view(["DELETE"])
def delete_files(request):
    serializer = DeleteFilesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        session = session_service.get_active_session(request)
    except FileNotFoundError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    result = file_service.delete_files(
        session=session,
        filenames=serializer.validated_data["files"],
    )

    response = Response(result)

    session_service.refresh_session(
        response,
        session,
    )

    return response


@api_view(["DELETE"])
def delete_all(request):

    try:
        session = session_service.get_active_session(request)
    except FileNotFoundError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    file_service.delete_all(session)

    response = Response(
        {
            "message": "Workspace cleared.",
        },
        status=status.HTTP_200_OK,
    )

    session_service.refresh_session(
        response,
        session,
    )

    return response
