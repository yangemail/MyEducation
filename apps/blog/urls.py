from django.urls import path

from blog.views import BlogListView, BlogIndexView

urlpatterns = [
    # 博客列表页
    path('index/', BlogIndexView.as_view(), name='blog_index'),
    path('list/', BlogListView.as_view(), name='blog_list'),

    # path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    # path('info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
    # path('comments/<int:course_id>/', CourseCommentsView.as_view(), name='course_comments'),

    # 添加博客评论
    # path('add_comment/', CourseAddCommentView.as_view(), name='add_comment'),

    # 播放视频
    # path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),

]
