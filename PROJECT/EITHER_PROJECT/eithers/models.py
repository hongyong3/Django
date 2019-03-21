from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=100)
    issue_a = models.CharField(max_length=100)
    issue_b = models.CharField(max_length=100)
    image_a = ProcessedImageField(
            blank=True,
            upload_to='eithers/images',							# 저장 위치
            processors=[ResizeToFill(250,300)],		# 처리할 작업 목록
            format='JPEG',													# 저장 포맷
            options={'quality': 90},								# 옵션
            )
    image_b = ProcessedImageField(
            blank=True,
            upload_to='eithers/images',							# 저장 위치
            processors=[ResizeToFill(250,300)],		# 처리할 작업 목록
            format='JPEG',													# 저장 포맷
            options={'quality': 90},								# 옵션
            )
    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pick = models.IntegerField()
    comment = models.CharField(max_length=100)

    def __str__(self):
        return self.comment
    
