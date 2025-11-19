from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from board.models import Post as BoardPost, Comment as BoardComment
from trade.models import Product as TradePost

@login_required
def mypage_view(request):
    """
    마이페이지 뷰.
    로그인된 사용자가 작성한 게시글, 댓글, 판매 상품을 조회합니다.
    """
    user = request.user

    # 사용자가 작성한 board 앱의 게시글과 댓글 조회
    board_posts = BoardPost.objects.filter(user=user).order_by('-created_at')
    board_comments = BoardComment.objects.filter(user=user).order_by('-created_at')

    # 사용자가 작성한 trade 앱의 판매 상품 조회
    trade_posts = TradePost.objects.filter(author=user).order_by('-created_at')

    context = {
        'board_posts': board_posts,
        'board_comments': board_comments,
        'trade_posts': trade_posts,
        'user': user,
    }
    return render(request, 'mypage/mypage.html', context)
