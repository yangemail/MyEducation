from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class BlogIndexView(View):
    def get(self, request):
        return render(request, 'blog/blog_index.html', {})


class BlogListView(View):
    def get(self, request):
        return render(request, 'blog/blog_list.html', {})
