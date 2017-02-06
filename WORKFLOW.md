
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

---
流程update 2017-2-6

1.在youtube上浏览视频，将想下载的视频收藏到特定的playlist中

2.下载is_download属性设置为true的youtubeplaylist里的视频信息并保存到数据库中
http://127.0.0.1:8000/video/auto_get_youtube_playlist_video_info

3.在AutoSystem的youtube playlist页面中，访问playlist的视频页面填写视频的中文名称后，保存
http://127.0.0.1:8000/admin/video/youtubeplaylist/?channel__channel_id__exact=UCEQpJTOXGkvS1UQsdCm6lLA&is_download__exact=1

