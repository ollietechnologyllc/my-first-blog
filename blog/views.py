from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment#, Profile
from django.utils import timezone
from .forms import PostForm, CommentForm, CustomUserCreationForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def post_list(request):
    if not request.user.is_authenticated:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date').filter(make_public=True)
        otherposts = None
    else:
        otherposts = Post.objects.filter(published_date__lte=timezone.now()).filter(make_public=True).exclude(author=request.user).order_by('-published_date')
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date').filter(author=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts,'otherposts': otherposts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # This is a cleaner way than: Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post  = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    print(post.published_date)
    return redirect('post_detail', pk=post.pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
#def make_public(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    post.make_public()
#    return redirect('post_detail', pk=post.pk)
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
def approved_comments(request):
    return self.comments.filter(approved_comment=True)

def register(request):
   
    if request.method == 'POST':
        #f = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #form.refresh_from_db()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form':form})

#def update_user_data(user):
#    Profile.objects.update_or_create(user=user, defaults={'mob': user.profile.mob},)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            #custom user value
 #           user.profile.mob = form.cleaned_data.get('mob')
 #           update_user_data(user)
            #load the profle instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            #login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # Redirect user to home page
            return redirect('post_list')
                
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})
