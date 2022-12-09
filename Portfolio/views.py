from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, CommentForm, UserForm,BlogPostForm,UpdateBlogPostForm
from django.views import generic
from .models import Post
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.models import User

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


def post_detail(request, slug):
    template_name = 'Portfolio/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '  Email: ' + from_email
            try:
                send_mail(subject, message, from_email, ['loevliedenny@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('Portfolio:success')
    return render(request, 'Portfolio/index.html', {'form': form})
    # return render(request,'Portfolio/index.html')

def timeline(request):
    return render(request, 'Portfolio/timeline.html')


def portfolio(request):
    return render(request, 'Portfolio/portfolio.html')
    
def publications(request):
    return render(request, 'Portfolio/publications.html')

# class UpdatePostView(generic.UpdateView):
#     model = Post
#     template_name = 'Portfolio/update_post.html'
#     fields = ['title', 'slug','snippet', 'content','status']

def UpdatePostView(request,slug):
    blog_post = get_object_or_404(Post,slug=slug)
    if request.method == 'POST':
        user_profile = User.objects.get(username=request.user.username)
        post_form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = user_profile
            form = form.save()
            return render(request,'Portfolio/posted.html',{'action':'updating'})
        else:
            print(post_form.errors)
    else:
        if str(request.user.username) == str(blog_post.author):
            form = UpdateBlogPostForm(instance=request.user,initial = {"title":blog_post.title,"slug":blog_post.slug,"snippet":blog_post.snippet,"content":blog_post.content,"status":blog_post.status})
            return render(request,'Portfolio/update_post.html',{'form':form})
        else:
            return HttpResponse("<h1>Only the user who created the post may edit it</h1>")



class blog(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'Portfolio/blog.html'
    paginate_by = 3
    #return render(request, 'Portfolio/blog.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password) # Authenticating the user for us
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('Blog'))
            else:
                HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            return HttpResponse("Invalide Login")
    else:
        return render(request,'Portfolio/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Blog'))





def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save() # Saving directly to the DATABASE
            user.set_password(user.password) # Hashing the password
            user.save()

            # Set One to One relationship between

            # UserForm and UserProfileInfoForm
            # Can't commit yet because we still need to manipulate

            registered = True
            login(request,user)
    else:
        user_form = UserForm()
        privacy_policy=True
    return render(request,'Portfolio/registration.html',
                          {'user_form':user_form,
                           'registered':registered,})


def AddPostView(request):
    if request.method == 'POST':
        user_profile = User.objects.get(username=request.user.username)
        #model = Post.objects.get(author=user.request.user)
        post_form = BlogPostForm(data=request.POST)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = user_profile
            form = form.save()
            return render(request,'Portfolio/posted.html',{'action':'making'})
        else:
            return HttpResponse('Something did not work the slug may already exist!')
    else:
        form = BlogPostForm(instance=request.user)
    return render(request,'Portfolio/add_post.html',{'form':form})


def about_me(request):
    return render(request, 'Portfolio/about_me.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '  Email: ' + from_email
            try:
                send_mail(subject, message, from_email, ['loevliedenny@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'Portfolio/message_sent.html')
    return render(request, 'Portfolio/contact.html', {'form': form})