# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
# Create your models here.

'''
a model/table to store the email, name, username, password, created date/time and last updated date/time of each user
'''
class UserModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<UserModel : %s - %s>"%(self.username , self.id)

'''
a model/table to store the session token id and time that each user
'''
class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = str(uuid4())

'''
a model/table to store the image url caption, created date/time and last updated date/time that each user has submitted for different posts
create a new row in the database table with the comment for that particular post
'''
class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.likemodel_set.count()

    @property
    def comments(self):
        return self.commentmodel_set.order_by("created_on").all()

    def liked_by_user(self,user):
        l = self.likemodel_set.filter(user = user)
        return len(l) > 0


'''
a model/table to store the likes that each user has submitted for different posts
'''
class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

'''
a model with post_id as a reference key, comment text, user_id of the user who created the comment
'''
class CommentModel(models.Model):
  user = models.ForeignKey(UserModel)
  post = models.ForeignKey(PostModel)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)