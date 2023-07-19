from django.urls import path

from blog.views import index, about, blog_url, contact, staff, admin_create_new_post, group_posts, post_comment, admin_create_group
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('blog/', blog_url, name='blog_url'),
    path('contact/', contact, name='contact'),
    path('give-contacts/', staff, name='staff'),
    path('create-post/', admin_create_new_post, name='create_post'),
    path('group/<slug:slug>/', group_posts, name='group_posts'),
    path('single/<int:pk>/', post_comment, name='add_comment'),
    path('create-group/', admin_create_group, name='create_group'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
