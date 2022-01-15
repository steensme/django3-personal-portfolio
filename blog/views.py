from django.shortcuts import render, get_object_or_404
from .models import Blog

def all_blogs(request):
    blogs = Blog.objects.order_by('updated')
    return render(request, 'blog/all_blogs.html', {'blogs':blogs})

def detail(request, blog_id):
   blog = get_object_or_404(Blog, pk=blog_id)
   return render(request, 'blog/detail.html',{'blog':blog})

from .forms import EmailPostForm
from django.core.mail import send_mail
def post_share(request, year, month, day, blog_id):
    # Retrieve post by id
    post = get_object_or_404(Post, slug=blog_id,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'evan.d.steensma@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

# def post_share(request, blog_id):
#     # Retrieve post by id
#     post = get_object_or_404(Blog, id=blog_id)
#     if request.method == 'POST':
#         # Form was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             # Form fields passed validation
#             cd = form.cleaned_data
#             # ... send email
#     else:
#         form = EmailPostForm()
#     return render(request, 'blog/post/share.html', {'post': post,
#                                                     'form': form})
