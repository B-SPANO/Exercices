from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from forum.models import Forum, Topic, Post, Profile#, PostTracking


class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic_count']
    readonly_fields = ['post_count', 'topic_count', 'last_post']

class TopicAdmin(admin.ModelAdmin):

    def forum_label(self, obj):
        return str(obj.forum)

    list_display = ['name', 'forum_label', 'created', 'post_count', 'closed']
    search_fields = ['name']
    readonly_fields = ['post_count', 'last_post']

class PostAdmin(admin.ModelAdmin):

    def user_name(self, obj):
        return str(obj.user)

    def topic_label(self, obj):
        return str(obj.topic)

    
    list_display = [ 'topic_label', '__str__', 'user_name', 'created', 'updated',]
    search_fields = ['body']
   
    

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'location' ]
    # readonly_fields = ['post_count', 'topic_count', 'last_post']

# class PostTrackingAdmin(admin.ModelAdmin):
#     list_display = ['user', 'last_read', 'topics']
    


admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(PostTracking, PostTrackingAdmin)