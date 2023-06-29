from django.shortcuts import render, get_object_or_404, redirect
from products.forms import ProductCommentModelForm
from products.utils import get_product_last_price_list
from .models import Product, Comment

# Create your views here.


def product_list_view(request):
    page = int(request.GET.get('page', 1))
    query = Product.objects.all()
    q = request.GET.get('q', '')
    if q:
        query = query.filter(name__contains=q)
    page_size = 10
    products = query[(page-1) * page_size:page*page_size]
    context = {"products": products}

    return render(
        template_name='products/product-list.html',
        request=request,
        context=context,
    )


def product_detail_view(request, pk):
    p = get_object_or_404(Product.objects.select_related(
        'category').prefetch_related("comment_set"), pk=pk)

    if request.method == "GET":
        form = ProductCommentModelForm(initial={'product': p})
    elif request.method == 'POST':
        form = ProductCommentModelForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('products:product_detail', pk=pk)
        else:
            print(form.errors)
    context = {
        "product": p,
        "seller_prices": p.sellers_last_price,
        "comments": p.comment_set.all(),
        "comment_counts": p.comment_set.all().count(),
        'comment_form': form
    }
    return render(
        template_name='products/product_detail.html',
        request=request,
        context=context
    )


def create_comment(request, product_id):
    pass
    # if request.method == "POST":
    #     Comment.objects.create(
    #         user_email=request.POST.get("user_email", ''),
    #         title=request.POST.get("title", ''),
    #         text=request.POST.get("text", ''),
    #         rate=int(request.POST.get("rate", 0)),
    #         product_id=request.POST.get("product_id", '')
    #     )
    # return redirect('products:product_detail', pk=product_id)


# def delete_comment(request, pk):
#     if request.method == 'POST':
#         c = Comment.objects.get(pk=pk)
#         c.delete()
#         return HttpResponse('comment delete successfully')
#     else:
#         return HttpResponseNotAllowed('method not allowed')
