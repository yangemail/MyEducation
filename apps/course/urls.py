from django.urls import path

from course.views import CourtListView, CourseDetailView, CourseCommentsView, CourseAddCommentView, \
    VideoPlayView, CourseVideoListView

urlpatterns = [

    # 课程列表页
    path('list/', CourtListView.as_view(), name='course_list'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'), # 课程详情
    path('videolist/<int:course_id>/', CourseVideoListView.as_view(), name='course_video_list'), # “课程章节信息” - 带视频的那个页面，
    path('comments/<int:course_id>/', CourseCommentsView.as_view(), name='course_comments'),

    # 添加课程评论
    path('add_comment/', CourseAddCommentView.as_view(), name='add_comment'),

    # 播放视频
    path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'), # 课程视频播放页面

]
