from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Author, Category, User
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from .tasks import send_mail_for_sub_once


from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    news_list = News.objects.all().order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news_list': news_list})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news_item': news_item})

class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

# дженерик для добавления объекта
class PostAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    context_object_name = 'add'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    #  метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all
    success_url = '/news/'
    permission_required = ('news.delete_post',)


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'protected_page.html'

@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


# функция отписки от группы
@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')


def send_mail_for_sub(instance):
    print('Представления - начало')
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')

    sub_text = instance.text

    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()


    print('Адреса рассылки:')
    for pos in subscribers:
        print(pos.email)

    print()
    print()
    print()
    for subscriber in subscribers:

        print('**********************', subscriber.email, '**********************')
        print(subscriber)
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})

        sub_username = subscriber.username
        sub_useremail = subscriber.email

        print()
        print(html_content)
        print()

        send_mail_for_sub_once.delay(sub_username, sub_useremail, html_content)


    print('Представления - конец')

    return redirect('/news/')

from django.views.generic import ListView, DetailView
from .models import Product
from .filters import ProductFilter


class ProductsList(ListView):
   model = Product
   ordering = 'name'
   template_name = 'products.html'
   context_object_name = 'products'
   paginate_by = 2

   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = ProductFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context


class ProductDetail(DetailView):
   model = Product
   template_name = 'product.html'
   context_object_name = 'product'

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import NewsArticle
from .forms import NewsArticleForm
from .filters import NewsArticleFilter

def news_list(request):
    news_articles = NewsArticle.objects.all().order_by('-pub_date')
    filter = NewsArticleFilter(request.GET, queryset=news_articles)
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj, 'filter': filter})

def news_search(request):
    filter = NewsArticleFilter(request.GET, queryset=NewsArticle.objects.all())
    return render(request, 'news/news_search.html', {'filter': filter})

def news_create(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsArticleForm()
    return render(request, 'news/news_form.html', {'form': form})

def news_edit(request, pk):
    news_article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, instance=news_article)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsArticleForm(instance=news_article)
    return render(request, 'news/news_form.html', {'form': form})

def news_delete(request, pk):
    news_article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        news_article.delete()
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'object': news_article})