from django.urls import path

from course.views import CourtListView, CourseDetailView, CourseInfoView, CourseCommentsView, CourseAddCommentView, \
    VideoPlayView

urlpatterns = [

    # 课程列表页
    path('list/', CourtListView.as_view(), name='course_list'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
    path('comments/<int:course_id>/', CourseCommentsView.as_view(), name='course_comments'),

    # 添加课程评论
    path('add_comment/', CourseAddCommentView.as_view(), name='add_comment'),

    # 播放视频
    path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),

]
