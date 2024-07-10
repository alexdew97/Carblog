from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView
from .forms import EmailPostForm

def post_list(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Якщо номер сторінки не ціле число відкрити першу
        posts = paginator.page(1)
    except EmptyPage:
        # Якщо номер сторінки більший за існуючий відкрити останню
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
'blog/post/list.html',
    {'posts': posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(
        request,
'blog/post/detail.html',
    {'post': post}
    )

class PostListView(ListView):
    """
    Альтернативне представлення
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Дістати пост по ІД
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    if request.method == 'POST':
        # Форма передана на обробку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля форми валідовано
            cd = form.cleaned_data
            # Надіслати листа

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form
        }
    )