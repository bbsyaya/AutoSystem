
起始操作：
获取youku上的playlist
http://127.0.0.1:8000/video/get_my_playlists

---
流程

1. 自动下载我youtube首页显示的订阅频道的视频信息，保存到本地数据库
http://127.0.0.1:8000/video/get_subscription_update_video/50

2. 人工-看哪个视频顺眼就点进去，添加youku信息, title必填
http://127.0.0.1:8000/admin/video/video/

3. 自动下载所有填写好youku model中title的video model的视频
http://127.0.0.1:8000/video/download_multi_youtube_video/2

4. 自动合并中英字幕，并将中英字幕合并到视频中

4. 自动根据youtube的channel所属的category设置填写了title的youku视频的category
http://127.0.0.1:8000/video/auto_set_youku_category

5. 自动上传所有填写好youku model中category的视频到youku
http://127.0.0.1:8000/video/auto_youku_upload