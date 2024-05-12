import time
from django.shortcuts import render, redirect, reverse
from index.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def commentView(request, id):
    # 获取搜索量前四首歌
    searches = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
    # 提交表单post请求
    if request.method == 'POST':
        # 获取评论内容
        text = request.POST.get('comment', '')
        # 判断当前是否有用户登录
        if request.user.username:
            user = request.user.username
        else:
            user = '匿名用户'
        # 评论时间
        now = time.strftime('%%Y-%m-%d', time.localtime(time.time()))
        # 如果评论不为空，则保存到数据库
        if text:
            comment = Comment()
            comment.text = text
            comment.user = user
            comment.date = now
            comment.song_id = id
            comment.save()
        return redirect(reverse('comment', kwargs={'id': str(id)}))
    # 请求为get
    else:
        # 获取当前歌曲信息
        songs = Song.objects.filter(id=id).first()
        # 获取当前歌曲评论信息
        comments = Comment.objects.filter(song_id=id).order_by('date').all()
        # 默认评论初始为第一页
        page = int(request.GET.get('page', '1'))
        # 评论分页, 传入需要分页的信息，并制定页显示数据的个数
        paginator = Paginator(comments, 2)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        return render(request, 'comment.html', locals())
