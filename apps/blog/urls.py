from django.urls import path

from blog.views import ArticleIndexView, ArticleListView, ArticleDetailView
from blog.views import TutorialListView, TutorialDetailView, TutorialArticleListView, TutorialCommentsView

urlpatterns = [
    # 文章列表页
    path('article/index/', ArticleIndexView.as_view(), name='blog_article_index'),
    path('article/list/', ArticleListView.as_view(), name='blog_article_list'),
    path('article/detail/<int:article_id>', ArticleDetailView.as_view(), name='blog_article_detail'),

    # 教程列表页
    path('tutorial/list/', TutorialListView.as_view(), name='blog_tutorial_list'),
    path('tutorial/detail/<int:tutorial_id>/', TutorialDetailView.as_view(), name='blog_tutorial_detail'),
    path('tutorial/info/<int:tutorial_id>/', TutorialArticleListView.as_view(), name='blog_tutorial_article_list'),
    path('tutorial/comments/<int:tutorial_id>/', TutorialCommentsView.as_view(), name='blog_tutorial_comments'),

    # path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    # path('info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
    # path('comments/<int:course_id>/', CourseCommentsView.as_view(), name='course_comments'),

    # 添加博客评论
    # path('add_comment/', CourseAddCommentView.as_view(), name='add_comment'),

    # 播放视频
    # path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),

]
