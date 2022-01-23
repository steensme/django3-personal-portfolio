from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment
from taggit.models import Tag

def all_blogs(request, tag_slug=None):
    blogs = Blog.objects.order_by('updated')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    return render(request, 'blog/all_blogs.html', {'blogs':blogs,
                                                   'tag': tag})

def detail(request, blog_id):
   post = get_object_or_404(Blog, pk=blog_id)
   # List of active comments for this post
   comments = post.comments.filter(active=True)
   new_comment = None
   if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
   else:
        comment_form = CommentForm()
   return render(request,
                    'blog/detail.html',
                    {'blog':post,
                    'comments': comments,
                    'new_comment': new_comment,
                    'comment_form': comment_form})

from .forms import EmailPostForm, CommentForm
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
