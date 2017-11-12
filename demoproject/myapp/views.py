# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render , redirect
from datetime import datetime
from .forms import SignUpForm , LoginForm , PostForm, LikeForm , CommentForm
from .models import  UserModel , SessionToken , PostModel, LikeModel , CommentModel
from imgurpython import ImgurClient
from demoproject.settings import BASE_DIR
from uuid import uuid4
from django.contrib.auth.hashers import make_password , check_password
# Create your views here.


'''
the method is used to take data from the sign up webpage form and store it the database
'''
def signup_view(request):
    today  = datetime.now()
    if request.method == "GET":
        form = SignUpForm()
    else:
        #submit button the form should make a POST request
        form = SignUpForm(request.POST)
        #validations are met create a new record in the database for that user
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            hashed_password = make_password(password)
            user = UserModel(name = name , email = email , username = username , password = make_password(password))
            user.save()
            return render(request , "success.html")
    return render(request, "index.html", {
        "today": today,
        "method": request.method,
        "form": form
    })


'''
the mothod check the username and password of the login webpage form with the username and password fields of user model in database
'''
def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request , "login.html", {
            "form" : form
        })
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserModel.objects.filter(username = username).first()
            print "User ... " , user
            if user:
                #check if a user that exists with the username and password that has been provided as input
                if check_password(password , user.password):
                    session = SessionToken(user = user)
                    session.create_token()
                    session.save()
                    response  = redirect("/feed")
                    response.set_cookie(key = "session_token" , value = session.session_token)
                    return response
                    print "User Is Valid"
                else:
                    #error message saying that the user does not exist or the username/password combination is wrong
                    print "The username/password combination is Wrong"


'''
this method create a session for the user and insert the session id inside the cookie
'''
def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None


'''
the method make an entry in the database with the user id, image url and caption
'''
def post_view(request):
    user = check_validation(request)
    if user:
        print 'Authentic user'
    else:
        return redirect('/login')

    if request.method == "GET":
        form = PostForm()
        return render(request , "post.html" , {
            "form" : form
        })
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            post = PostModel(user = user , image = image , caption = caption)
            post.save()
            path = str(BASE_DIR + "\\" + post.image.url)
            client = ImgurClient("777a04d2c916ba3", "20842f7498c6e33da35f64042c6935247c0f71a9")
            post.image_url = client.upload_from_path(path, anon=True)['link']
            print "post was successfully created"
            post.save()
            return redirect("/feed")


'''
The method send the user to the /feeds/ page after log in
'''
def feed(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by("created_on")
        return render(request, 'feed.html', {
            "posts" : posts
        })
    else:
        return redirect('/login')

'''
the method check the perticular post and create entry for the post id in the like model(database)
'''
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')
    else:
     return redirect('/login/')



'''
the method check the perticular post and create entry comment time, user's name and post id for the post in the comment model(database)
'''
def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      post_id = form.cleaned_data.get('post').id
      comment_text = form.cleaned_data.get('comment_text')
      comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
      comment.save()
      return redirect('/feed/')
    else:
        return redirect('/feed/')
  else:
    return redirect('/login')