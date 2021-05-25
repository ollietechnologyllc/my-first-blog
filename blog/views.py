from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required


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
