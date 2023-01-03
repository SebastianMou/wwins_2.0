from django.shortcuts import render, redirect
from .models import PostModel
from .forms import UserRegisterForm, PostForm, UserUpdateForm, ProfileUpdateForm, PostUpdateForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home_info(request):
    return render(request, 'blog/home_info.html')

def home(request):
    posts = PostModel.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'there was a error')
            return redirect('login_user')
    return render(request, 'blog/users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'you where loged out')
    return redirect('home')

@login_required
def create_post(request):
    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'blog/create_post.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/users/register.html', context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profilemodel)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'blog/profile.html', context)

def like_post(request, pk):
    post = get_object_or_404(PostModel, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

@login_required
def post_detail(request, pk):
    likes_connected = get_object_or_404(PostModel, id=pk)
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True

    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('post_detail', pk=post.id)
    else:
        c_form = CommentForm()

    context = {
        'post': post,
        'c_form': c_form,
        'total_likes': likes_connected.total_likes(),
        'post_is_liked': liked,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)

@login_required
def delete(request, post_id=None):
    post = PostModel.objects.get(id=post_id)
    post.delete()
    return redirect('/')




