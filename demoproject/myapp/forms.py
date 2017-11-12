from django import forms
from .models import UserModel , PostModel ,  LikeModel , CommentModel

'''
Class for sign up form having field username, email, name, new password
'''
class SignUpForm(forms.ModelForm):
  class Meta:
    model = UserModel
    fields=['email','username','name','password']

'''
Class for login page having the fields for username and password
'''
class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']

'''
class to store image url and caption for that particular post of each users
'''
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image' , 'caption']

class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields=['post']


'''
Class for storing comments for that particular post of each user and  storing it database
'''
class CommentForm(forms.ModelForm):
  class Meta:
    model = CommentModel
    fields = ['comment_text', 'post']