# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .session_io import SessionService
from .session_io import SessionModel

from api.serializers import DeleteFilesSerializer
from api.serializers import ChatSerializer
from rag_engine.generator.answer_service import AnswerService
from sessions.manager import SessionManager
from services.file_service import FileService
from services.upload_service import UploadService
from django.utils.timezone import now
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile
from backend.realtime.progress_reporter import ProgressReporter

from django.conf import settings


def get_upload_service():
    return UploadService()


def get_answer_service():
    return AnswerService()


def get_file_service():
    return FileService()


session_manager = SessionManager()
session_service = SessionService()


@api_view(["GET"])
def health(request):
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
    uploaded_file = request.FILES.get("file")
    if uploaded_file is None:
        return Response(
            {"error": "No file uploaded."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    session = session_service.get_or_create_session(request)
    progress = ProgressReporter(session.session_id)
    progress.upload(
        "upload_started",
        "Upload request received.",
        0,
        preview=f"File: {uploaded_file.name}",
        after="File 2. 'abc abc   def  #'",
    )

    get_upload_service().upload(
        uploaded_file,
        session,
    )

    response = Response(
        {
            "filename": uploaded_file.name,
        },
        status=status.HTTP_201_CREATED,
    )

    return attach_session(response, session)


@api_view(["POST"])
def load_demo(request):

    session = session_service.get_or_create_session(request)
    progress = ProgressReporter(session.session_id)
    progress.upload(
        "demo_started",
        "Loading demo documents...",
        0,
    )

    demo_folder = Path(settings.BASE_DIR) / "demo_documents"

    files = [f for f in demo_folder.iterdir() if f.is_file()]
    total = len(files)

    for index, path in enumerate(files, start=1):

        base_progress = int((index - 1) / total * 100)
        progress.upload(
            "demo_loading",
            f"Loading {path.name} ({index}/{total})",
            base_progress,
        )

        with open(path, "rb") as f:
            uploaded_file = SimpleUploadedFile(
                name=path.name,
                content=f.read(),
            )

            get_upload_service().upload(
                uploaded_file,
                session,
            )

    response = Response(
        {"message": "Demo workspace loaded."},
        status=status.HTTP_200_OK,
    )

    progress.upload(
        "demo_finished",
        "Demo documents loaded successfully.",
        100,
    )

    return attach_session(response, session)


@api_view(["POST"])
def chat(request):
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        session = session_service.get_active_session(request)
        progress = ProgressReporter(session.session_id)

        question_text = serializer.validated_data.get("question", "")
        progress.chat(
            "question_received",
            "Question received.",
            5,
            preview=f"Query about {question_text}",
            after=f"Asking about {question_text}",
        )

    except FileNotFoundError:
        session = session_service.get_or_create_session(request)
        response = Response([])
        return attach_session(response, session)
    try:
        result = get_answer_service().answer(
            question=serializer.validated_data["question"],
            sources=serializer.validated_data.get("sources", []),
            session=session,
            progress=progress,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=503,
        )

    response = Response(result)
    return attach_session(response, session)


def attach_session(
    response: Response,
    session: SessionModel,
) -> Response:
    response["X-Session-ID"] = session.session_id
    session_service.refresh_session(response, session)
    return response


@api_view(["GET"])
def files(request):
    if session_service.get_session_id_from_request(request) is None:
        return Response([])

    try:
        session = session_service.get_active_session(request)
    except FileNotFoundError:
        session = session_service.get_or_create_session(request)

        response = Response([])
        return attach_session(response, session)

    files = get_file_service().list_files(session)

    response = Response(files)
    return attach_session(response, session)


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

    result = get_file_service().delete_files(
        session=session,
        filenames=serializer.validated_data["files"],
    )

    response = Response(result)
    return attach_session(response, session)


@api_view(["DELETE"])
def delete_all(request):

    try:
        session = session_service.get_active_session(request)
    except FileNotFoundError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    get_file_service().delete_all(session)

    response = Response(
        {
            "message": "Workspace cleared.",
        },
        status=status.HTTP_200_OK,
    )

    return attach_session(response, session)
