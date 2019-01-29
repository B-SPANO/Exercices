from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from forum.models import Forum, Topic, Post, Profile


class ForumAdmin(admin.ModelAdmin):
    """ Topic admin model setting displaying field on back-office """

    list_display = ['name', 'topic_count']
    readonly_fields = ['post_count', 'topic_count', 'last_post']

class TopicAdmin(admin.ModelAdmin):
    """ Topic admin model setting displaying field on back-office """

    def forum_label(self, obj):
        """ function setting human readable field """
        return str(obj.forum)

    list_display = ['name', 'forum_label', 'created', 'post_count', 'closed']
    search_fields = ['name']
    readonly_fields = ['post_count', 'last_post']

class PostAdmin(admin.ModelAdmin):
    """
    Post Admin model setting displaying field on back-office
    """

    def user_name(self, obj):
        """ function setting human readable field """
        return str(obj.profile)

    def topic_label(self, obj):
        """ function setting human readable field """
        return str(obj.topic)


    list_display = ['topic_label', '__str__', 'user_name', 'created', 'updated',]
    search_fields = ['body']


class ProfileAdmin(admin.ModelAdmin):
    """
    Profile Admin Model setting displaying field on back-office
    """
    list_display = ['__str__', 'location']


admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
