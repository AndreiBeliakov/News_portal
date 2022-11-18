from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import  User
from .filters import NewFilter
from .forms import NewForm
from .models import New, UsersSubscriptions, Category


class NewsList(ListView):

    model = New

    ordering = "-created"

    template_name = 'news.html'

    context_object_name = 'news'

    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context



class NewDetail(DetailView):

    model = New

    template_name = 'new.html'

    context_object_name = 'new'

class NewSearch(NewsList):
    model = New
    template_name = 'search.html'
    context_object_name = 'news'


class NewCreate(CreateView):
    form_class = NewForm
    model = New
    template_name = 'create.html'

class NewEdit(UpdateView):
    form_class = NewForm
    model = New
    template_name = 'edit.html'


class NewDelete(DeleteView):
    model = New
    template_name = 'delete.html'
    success_url = reverse_lazy('new_list')

@login_required
def usersubscribtions(request, i):
    user = User.objects.get(username=request.user)
    if user:
        cat1 = Category.objects.get(pk=i)
        cat1.usersubscribtions.add(user)
    return redirect('/news/')