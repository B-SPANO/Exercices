from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from forum import views

router = DefaultRouter()
router.register(r'rest/forum', views.ForumViewset,)
router.register(r'rest/topic', views.TopicViewset,)
router.register(r'rest/post', views.PostViewset,)
router.register(r'rest/user', views.UserViewset,)

urlpatterns = [

    # # Auth
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='forum/login.html')),

    #User
    path('users/', views.UserCreate.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    # Forum
    path('', views.index, name='index'),
    re_path(r'^(?P<forum_id>\d+)/$', views.show_forum, name='forum'),
    path('mail', views.mail, name='mail'),
    path('sub/', views.subscription, name='subscription'),

    # Topic
    re_path(r'^\d+/topic/(?P<topic_id>\d+)/$', views.show_topic, name='topic'),
    re_path(r'^(?P<forum_id>\d+)/topic/add/$', views.AddTopic.as_view(
        template_name="forum/add_topic.html"), name='add_topic'),
    re_path(r'^topic/(?P<pk>\d+)/$', views.DeleteTopic.as_view(
        template_name="forum/topic_confirmation_delete.html"), name='delete_topic'),

    # Post
    re_path(r'^post/(?P<pk>\d+)/$', views.ShowPost.as_view(
        template_name="forum/post.html"), name='post'),
    re_path(r'^(?P<forum_id>\d+)/topic/(?P<topic_id>\d+)/post/add/$', views.AddPost.as_view(
        template_name="forum/add_post.html"), name='add_post'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.EditPost.as_view(), name='edit_post'),
    re_path(r'^post/(?P<pk>\d+)/delete/$', views.DeletePost.as_view(
        template_name="forum/post_confirmation_delete.html"), name='delete_post'),

] + [
    # API login
    path('api-auth/', include('rest_framework.urls')),

] + router.urls