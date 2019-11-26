import xadmin

from .models import Tutorial, Section, Article, Tag, Category


class TagAdmin(object):
    list_display = ['name', 'created_time', 'last_modified_time']
    search_fields = ['name', ]
    list_filter = ['name', 'created_time', 'last_modified_time']


class CategoryAdmin(object):
    list_display = ['name', 'desc', 'category_type', 'parent_category', 'is_tab', 'index', 'created_time',
                    'last_modified_time', ]
    search_fields = ['name', 'desc', 'category_type', 'parent_category', 'is_tab', 'index', ]
    list_filter = ['name', 'desc', 'category_type', 'parent_category', 'is_tab', 'index', 'created_time',
                   'last_modified_time', ]


class TutorialAdmin(object):
    list_display = ['title', 'desc', 'detail', 'fav_nums', 'image', 'click_nums', 'category', 'tag', 'created_time',
                    'last_modified_time']
    search_fields = ['title', 'desc', 'detail', 'fav_nums', 'image', 'click_nums', 'category', 'tag', ]
    list_filter = ['title', 'desc', 'detail', 'fav_nums', 'image', 'click_nums', 'category', 'tag', 'created_time',
                   'last_modified_time']
    style_fields = {'detail': 'ueditor'}


class SectionAdmin(object):
    list_display = ['name', 'tutorial', 'index', 'created_time', 'last_modified_time']
    search_fields = ['name', 'index', 'tutorial']
    list_filter = ['name', 'tutorial', 'index', 'created_time', 'last_modified_time']


class ArticleAdmin(object):
    list_display = ['title', 'excerpt', 'content', 'click_nums', 'is_recommend', 'teacher', 'video', 'created_time',
                    'last_modified_time']
    search_fields = ['title', 'excerpt', 'content', 'click_nums', 'is_recommend', 'teacher', 'video', ]
    list_filter = ['title', 'excerpt', 'content', 'click_nums', 'is_recommend', 'teacher', 'video', 'created_time',
                   'last_modified_time']
    style_fields = {'content': 'ueditor'}


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tutorial, TutorialAdmin)
xadmin.site.register(Section, SectionAdmin)
xadmin.site.register(Article, ArticleAdmin)
