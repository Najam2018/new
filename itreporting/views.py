from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse 
from itreporting.models import Issue
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView



def home(request): 

    return render(request, 'itreporting/home.html', {'title': 'Welcome'})


def about(request): 

    return HttpResponse('<h1>Student IT Services - About</h1>') 

def contact(request): 

    return HttpResponse('<h1>Student IT Services - Contact us </h1>') 


# def report(request): 

#     return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 3  # Optional pagination

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Issue
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form): 

        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 

    model = Issue

    fields = ['type', 'room', 'details']
    
    def test_func(self):

        issue = self.get_object()

        return self.request.user == issue.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Issue

    success_url = '/report'
    
    def test_func(self):

        issue = self.get_object()

        return self.request.user == issue.author


