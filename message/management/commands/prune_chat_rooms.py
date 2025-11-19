import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from message.models import ChatRoom

class Command(BaseCommand):
    help = '7일 이상된 중고거래 채팅방을 삭제합니다.'

    def handle(self, *args, **options):
        # 7일 이전의 시간 계산
        seven_days_ago = timezone.now() - datetime.timedelta(days=7)

        # 7일 이상되었고, 이름이 'trade_'로 시작하는 채팅방 필터링
        old_rooms = ChatRoom.objects.filter(
            created_at__lt=seven_days_ago,
            name__startswith='trade_'
        )

        room_count = old_rooms.count()

        if room_count > 0:
            old_rooms.delete()
            self.stdout.write(self.style.SUCCESS(f'성공적으로 {room_count}개의 오래된 채팅방을 삭제했습니다.'))
        else:
            self.stdout.write(self.style.SUCCESS('삭제할 오래된 채팅방이 없습니다.'))
