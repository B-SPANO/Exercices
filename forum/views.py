from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from forum.permissions import IsOwnerOrReadOnly
from django.core.mail import send_mail
from forum.task import sendmail_task
from forum.forms import SubscriptionForm
from django.db.models import Q
from forum.models import Forum, Post, Topic, Profile, Subscription
from forum.serializer import ForumSerializer, TopicSerializer, PostSerializer, ProfileSerializer


User = get_user_model()

def mail():
    """ call (send_mail) mailler"""

    sendmail_task.delay()


@login_required
def index(request):
    """ Define index.views """
    forums = Forum.objects.all().prefetch_related('topics',)

    context = {
        'forums': forums,
        'total_post_count': Post.objects.count(),
        'total_topic_count': Topic.objects.count(),
    }
    return render(request, 'forum/index.html', context)


@login_required
def show_forum(request, forum_id):
    """ Detailled view on forum=forum_id """
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = forum.topics.all
    moderators = forum.moderators.all

    to_return = {
        'forum': forum,
        'topics': topics,
        'posts': forum.post_count,
        # 'topics_page': get_page(topics, request, forum_settings.FORUM_PAGE_SIZE),
        'moderators': moderators,
    }

    return render(request, 'forum/forum.html', to_return)


@login_required
def show_topic(request, topic_id):
    """ Detailled view on topic=shawn_id """

    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    profile = user.forum_profile
    subscription = Subscription.objects.filter(topic=topic, profile=profile).first()

    if subscription is None:
        subscription_value = False
    else:
        subscription_value = subscription.value

    last_post = topic.last_post
    posts = topic.posts.all
    post_count = topic.post_count

    form = SubscriptionForm(initial={
        'profile':profile.id,
        'topic':topic.id,
        'value':subscription_value
        })


    view_data = {
        'topic': topic,
        # 'posts_page': get_page(posts, request, forum_settings.TOPIC_PAGE_SIZE),
        'last_post': last_post,
        'posts': posts,
        'post_count': post_count,
        'form': form,
    }

    return render(request, 'forum/topic.html', view_data)


def subscription(request):
    """ Define subsciption view, between topics and subscribers """


    form = SubscriptionForm(request.POST)

    if form.is_valid():
        # import pdb; pdb.set_trace()
        subscription, _ = Subscription.objects.update_or_create(
            topic_id=form.cleaned_data['topic'],
            profile=form.cleaned_data['profile'],
            defaults={'value':form.cleaned_data['value']},
            )
        subscription.save()

    return HttpResponseRedirect(reverse('topic', args=(subscription.topic_id,)))


class AddTopic(LoginRequiredMixin, CreateView):
    """ Create topic """

    login_url = 'accounts/login/'
    model = Topic
    fields = ['forum', 'name', ]

    def form_valid(self, form):
        # import pdb; pdb.set_trace()
        form.instance.profile = self.request.user.forum_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add_post',
                       kwargs={'topic_id':self.object.id,
                               'forum_id':self.object.forum_id}
                      )


class AddPost(LoginRequiredMixin, CreateView):

    login_url = 'accounts/login/'
    model = Post
    fields = ['body',]


    def form_valid(self, form):
        # import pdb; pdb.set_trace()
        form.instance.topic_id = self.request.resolver_match.kwargs.get('topic_id')
        form.instance.profile = self.request.user.forum_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk':self.object.id})


class ShowPost(LoginRequiredMixin, DetailView):

    login_url = 'accounts/login/'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditPost(LoginRequiredMixin, UpdateView):

    login_url = 'accounts/login/'
    model = Post
    fields = ['body']

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super().get_object(queryset=queryset)
        return self._object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user and self.request.user not in Post.topic.Forum_moderators:
            raise PermissionDenied("Vous n'avez pas la permission de modifier ceci.")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post', kwargs={'pk':self.object.id})


class Subscribe(LoginRequiredMixin, UpdateView):
    login_url = 'accounts/login/'
    model = Topic
    fields = ['']


class DeleteTopic(LoginRequiredMixin, DeleteView):

    login_url = 'accounts/login/'
    model = Topic

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super().get_object(queryset=queryset)
        return self._object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user and self.request.user not in Topic.Forum_moderators:
            raise PermissionDenied("Vous n'avez pas la permission de modifier ceci.")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('index')


class DeletePost(LoginRequiredMixin, DeleteView):

    login_url = 'accounts/login/'
    model = Post

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super().get_object(queryset=queryset)
        return self._object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user and self.request.user not in Post.topic.Forum_moderators:
            raise PermissionDenied("Vous n'avez pas la permission de modifier ceci.")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('index')


#
# API Rest Class
#

class ForumViewset(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    pagination_class = LimitOffsetPagination


class TopicViewset(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = LimitOffsetPagination


class PostViewset(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,  )
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination


class UserViewset(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = LimitOffsetPagination

class UserCreate(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    