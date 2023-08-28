from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

from django.shortcuts import redirect,get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View


from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from .models import Course
from .forms import ModuleFormSet

# Create your views here.

class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin:
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['subject','title','slug','overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin,ListView):
    # model = Course
    template_name = "courses/manage/course/list.html"
    permission_required = 'courses.view_course'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(owner=self.request.user)
    
class CourseCreateView(OwnerCourseEditMixin,CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin,UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin,DeleteView):

    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin,View):
    template_name = "courses/manage/module/formset.html"
    Course = None

    def get_formset(self,data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)
    
    
    def dispatch(self,request,pk):
        self.course = get_object_or_404(Course,id=pk,owner=request.user)
        return super().dispatch(request,pk)