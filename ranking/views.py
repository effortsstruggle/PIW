from django.shortcuts import render
from index.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def rankingView(request):
    # 获取歌曲分类类别
    labels = Label.objects.all()
    # 获取搜索量前四的歌曲
    searches = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
    # 获取所有歌曲，按播放量降序排序
    # 按标签分类
    t = request.GET.get('type', '')
    if t:
        dynamics = Dynamic.objects.select_related('song').filter(song__label=t).order_by('-plays').all()
    else:
        dynamics = Dynamic.objects.select_related('song').order_by('-plays').all()
    page = int(request.GET.get('page', '1'))
    # 分页
    paginator = Paginator(dynamics, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'ranking.html', locals())
