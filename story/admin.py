from django.contrib import admin
from story.models import Story, GeneratedStory, StoryImages, SystemSettings
from django import forms

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = '__all__'
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 80}),
            'summary': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'context': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'historical_significance': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'main_happenings': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'result': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'content': forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        }

class StoryAdmin(admin.ModelAdmin):
    form = StoryForm

class StoryImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'url', 'is_publish')
    ordering = ('id',)

class GeneratedStoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'is_publish')
    ordering = ('-id',)

admin.site.register(Story, StoryAdmin)
admin.site.register(GeneratedStory, GeneratedStoryAdmin)
admin.site.register(StoryImages, StoryImagesAdmin)
admin.site.register(SystemSettings)
