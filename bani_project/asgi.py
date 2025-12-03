"""
ASGI config for bani_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
# Django 설정을 초기화하기 위해 django 모듈을 import 합니다.
import django 

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# import message.routing  <-- 이 라인은 Django 설정 후로 이동합니다.

# -------------------- 필수 수정 및 추가 부분 --------------------

# 1. 사용할 settings 모듈을 지정합니다. (기존 라인 유지)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bani_project.settings')

# 2. Django 환경을 초기화합니다. (AUTH_USER_MODEL 오류 해결)
# 이 라인이 없으면 get_user_model()이 실패합니다.
django.setup()

# 3. 설정 초기화가 완료된 후 message.routing을 import 합니다.
import message.routing

# -------------------------------------------------------------

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            message.routing.websocket_urlpatterns
        )
    ),
})