from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_progress(
    session_id: str,
    event_type: str,
    stage: str,
    message: str,
    progress: int | None = None,
    preview: dict | None = None,
    after: str | None = None,
):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"progress_{session_id}",
        {
            "type": "progress_event",
            "payload": {
                "type": event_type,
                "stage": stage,
                "message": message,
                "progress": progress,
                "preview": preview,
                "after": after,
            },
        },
    )
