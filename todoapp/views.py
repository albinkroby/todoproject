from django.shortcuts import render,redirect
from django.urls import reverse_lazy
# from django.http import HttpResponse

from .models import Task
from .forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'cbvdetails.html'
    context_object_name = 'task'
    
class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'cbvupdate.html'
    context_object_name = 'task'
    fields = ['name','priority','date']
    def get_success_url(self):
        return reverse_lazy('cbvdetails',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

def home(request):
    tasks=Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name','')
        priority = request.POST.get('priority','')
        date=request.POST.get('date','')
        task = Task(name=name, priority=priority, date=date)
        task.save()
    return render(request, 'home.html',{'tasks':tasks})

def details(request,id):
    tasks=Task.objects.get(id=id)
    return render(request,'details.html',{'tasks':tasks})

def delete(request,id):
    if request.method == 'POST':
        task=Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task=Task.objects.get(id=id)
    f=TodoForm(request.POST or None,instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':task})