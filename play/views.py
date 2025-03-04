from django.shortcuts import render
from index.models import *
from django.http import StreamingHttpResponse
from django.db.models import F


# Create your views here.
def playView(request, id):
    # 热门搜索取前五个
    searches = Dynamic.objects.select_related('song').order_by('-search').all()[:5]
    # 获取当前歌曲的信息
    songs = Song.objects.get(id=int(id))
    # 播放列表
    play_list = request.session.get('play_list', [])
    # 定义exist标签，判断歌曲是否存在播放列表中
    exist = False
    if play_list:
        for i in play_list:
            if int(id) == i['id']:
                exist = True
    if exist == False:
        play_list.append({'id': int(id), 'singer': songs.singer, 'name': songs.name, 'time': songs.time})
    # 将列表信息存到session里
    request.session['play_list'] = play_list
    # 歌词
    if songs.lyrics != '暂无歌词':
        lyrics = str(songs.lyrics.url)[1::]
        with open(lyrics, 'r', encoding='utf-8') as f:
            lyrics = f.read()
    # 相关歌曲
    type = Song.objects.values('type').get(id=id)['type']
    relevant = Dynamic.objects.select_related('song').filter(song__type=type).order_by('-plays').all()[:6]
    # 添加歌曲播放次数
    p = Dynamic.objects.filter(song_id=int(id)).first()
    plays = p.plays + 1
    if p:
        Dynamic.objects.update_or_create(song_id=int(id), defaults={'plays': plays})
    return render(request, 'play.html', locals())


def downloadView(request, id):
    # 查找歌曲信息
    songs = Song.objects.get(id=int(id))
    file = songs.file.url[1::]
    # 添加加载次数
    p = Dynamic.objects.filter(song_id=int(id)).first()
    if p:
        download = p.download + 1
        Dynamic.objects.update_or_create(song_id=int(id), defaults={'download': download})

    # 下载歌曲
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # 将文件内容写入StreamingHttpResponse对象
    # 并以字节流方式返回给用户，实现文件下载
    f = str(id) + '.m4a'
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s"' % f
    return response
