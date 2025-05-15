import re
from rest_framework.serializers import ValidationError


def validate_video_link(value):
    """Проверка, что ссылка ведёт только на youtube.com."""
    youtube_patterns = [
        r'https?://(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?',
        r'https?://youtu\.be/[\w-]+(\?\S*)?',
    ]

    for pattern in youtube_patterns:
        if re.fullmatch(pattern, value):
            return

    raise ValidationError('Разрешены только ссылки на YouTube (youtube.com или youtu.be).')
