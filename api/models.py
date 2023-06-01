# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import timedelta

from django.db import models
from django.utils import timezone


class Account(models.Model):
    email = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=50)
    password = models.TextField()
    gender = models.CharField(max_length=1)
    birth = models.DateField()
    job = models.ForeignKey('Job', models.DO_NOTHING)
    picture = models.ForeignKey('Picture', models.DO_NOTHING)
    is_notification = models.IntegerField(blank=True, default=True)
    is_quiz = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class Comment(models.Model):
    id = models.OneToOneField('Verdict', models.DO_NOTHING, db_column='id', primary_key=True)
    verdict_id = models.IntegerField()
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(default=timezone.now() + timedelta(hours=8))
    is_edit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class CommentDislike(models.Model):
    comment = models.OneToOneField(Comment, models.DO_NOTHING, primary_key=True)
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'comment_dislike'
        unique_together = (('comment', 'email'),)


class CommentLike(models.Model):
    comment = models.OneToOneField(Comment, models.DO_NOTHING, primary_key=True)
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'comment_like'
        unique_together = (('comment', 'email'),)


class Crime(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'crime'


class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'job'


class Like(models.Model):
    verdict = models.OneToOneField('Verdict', models.DO_NOTHING, primary_key=True)
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'like'
        unique_together = (('verdict', 'email'),)


class Picture(models.Model):
    id = models.IntegerField(primary_key=True)
    photo = models.TextField()

    class Meta:
        managed = False
        db_table = 'picture'


class Quiz(models.Model):
    question_id = models.IntegerField(primary_key=True)
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'quiz'
        unique_together = (('question_id', 'email'),)


class Reply(models.Model):
    comment = models.ForeignKey(Comment, models.DO_NOTHING)
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(default=timezone.now() + timedelta(hours=8))
    is_edit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reply'


class Saved(models.Model):
    verdict = models.OneToOneField('Verdict', models.DO_NOTHING, primary_key=True)
    email = models.ForeignKey(Account, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'saved'
        unique_together = (('verdict', 'email'),)


class Ver(models.Model):
    title = models.CharField(max_length=45)
    sub_title = models.CharField(max_length=30)
    ver_title = models.CharField(max_length=30)
    judgement_date = models.DateField()
    crime_id = models.IntegerField()
    url = models.TextField()
    incident = models.TextField()
    result = models.TextField()
    laws = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now() + timedelta(hours=8))

    class Meta:
        managed = False
        db_table = 'ver'


class Verdict(models.Model):
    title = models.CharField(max_length=45)
    sub_title = models.CharField(max_length=30)
    ver_title = models.CharField(max_length=30)
    judgement_date = models.DateField()
    crime = models.ForeignKey(Crime, models.DO_NOTHING)
    url = models.TextField()
    incident = models.TextField()
    incident_lite = models.TextField()
    result = models.TextField()
    laws = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now() + timedelta(hours=8))

    class Meta:
        managed = False
        db_table = 'verdict'


class VerificationCode(models.Model):
    email = models.CharField(max_length=100)
    code = models.CharField(max_length=8)
    create_time = models.DateTimeField(default=timezone.now() + timedelta(hours=8))

    class Meta:
        managed = False
        db_table = 'verification_code'
