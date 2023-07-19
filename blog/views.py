import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm, PostForm, CommentForm, GroupForm
from .models import Contact, Post, Group, Comments
from .tasks import send_contact_email
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})


def staff(request):
    contacts = Contact.objects.filter(is_report_sent=False)
    contact_count = contacts.count()
    context = {
        'contact_count': contact_count
    }
    if request.method == 'POST':
        send_contact_email.delay()  # Запуск задачи асинхронно
        return render(request, 'staff_request.html')
    return render(request, 'staff_request.html', context)


def about(request):
    return render(request, 'about.html')


@cache_page(60)
def blog_url(request):
    posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-date')[:3]

    context = {
        'posts': posts,
    }
    return render(request, 'blog.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# in fact, I can use the decorator login_required, because I don't have the authorisation,
# but, "user_passes_test" for me this is new expertise, therefore I used that.
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/admin/')
def admin_create_new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_url')
    else:
        form = PostForm()
    return render(request, 'add_new_post.html', {'form': form})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-date")[:12]
    return render(request, "group_posts.html", {"group": group, "posts": posts})


def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all()  # Получение всех комментариев для данного поста

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('add_comment', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'single.html', {'post': post, 'comments': comments, 'form': form})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/admin/')
def admin_create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_post')
    else:
        form = GroupForm()
    return render(request, 'group.html', {'form': form})
