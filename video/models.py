from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    title_cn = models.CharField(max_length=50)
    subtile_en = models.CharField(max_length=50)
    subtile_cn = models.CharField(max_length=50)
    youku = models.ForeignKey('Youku', null=True, blank=True)
    baiduy_yun = models.ForeignKey('BaiduYun', null=True, blank=True)

    remark = models.CharField(max_length=300, null=True, blank=True)



    def __str__(self):
        return self.title


    class Meta:
        verbose_name_plural = "videos"


class Youku(models.Model):
    video_id = models.CharField(max_length=50)

class BaiduYun(models.Model):
    uri = models.CharField(max_length=50)

