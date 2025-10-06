from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.TextInput(attrs={'class':'form-control'}),
        }


class ContactForm(forms.Form):
    subject = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Your Name'}),label="")
    from_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'Email'}),label="")
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder':'Message'}),label="")
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email','body')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug','snippet', 'content','status','header_image')

class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug','snippet', 'content','status','header_image')

    def save(self,commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.slug = self.cleaned_data['slug']
        blog_post.snippet = self.cleaned_data['snippet']
        blog_post.content = self.cleaned_data['content']
        blog_post.status = self.cleaned_data['status']
        blog_post.header_image = self.cleaned_data['header_image']
        if commit:
            blog_post.save()
        return blog_post
