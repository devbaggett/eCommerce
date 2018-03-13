from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Product

# class based view

class ProductFeaturedListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.featured()

class ProductFeaturedDetailView(DetailView):
	queryset = Product.objects.featured() # makes queryset
	template_name = "products/featured-detail.html"

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()

	

class ProductListView(ListView):
	# queryset = Product.objects.all() # makes queryset
	template_name = "products/list.html"

	# every single classed based view has this method. What this method does is it gets the context
	# for any given query set or whatever view is being done. Happens to default. This removes the 
	# repetitiveness out of context
	# def get_context_data(self, *args, **kwargs): # keyword args, holds whatever arguments you may have
	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context

# function based view
def Product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, "products/list.html", context)

class ProductDetailSlugView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		# instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance=Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Not found..")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404("uhmmm")
		return instance

class ProductDetailView(DetailView):
	queryset = Product.objects.all() # makes queryset
	template_name = "products/detail.html"

	# every single classed based view has this method. What this method does is it gets the context
	# for any given query set or whatever view is being done. Happens to default. This removes the 
	# repetitiveness out of context
	def get_context_data(self, *args, **kwargs): # keyword args, holds whatever arguments you may have
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		print(context)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product doesn't exist")
		return instance

# function based view
def Product_detail_view(request, pk=None, *args, **kwargs):
	# print(args)
	# print(kwargs)
	instance = Product.objects.get(pk=pk, featured=True) # left pk is primary key/id, auto increments id

	# instance = get_object_or_404(Product, pk=pk)
	# try:
	# 	# id = pk is interchangeable
	# 	instance = Product.objects.get(id=pk) # instance equals to the id being passed, or primary key being passed
	# except Product.DoesNotExist:
	# 	print('no product here')
	# 	raise Http404("Product doesn't exist")
	# except:
	# 	print('huh?')


	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product doesn't exist")

	# print(instance)
	# qs = Product.objects.filter(id=pk) # same error handling as try/excep statement above
	

	# if qs.exists() and qs.count() == 1: 
	# 	instance = qs.first()
	# # when we run qs we can see what it is when we print it out. Count counts the
	# else: 
	# # count: counting length of queryset. We would do this over doing: len(queryset). More efficient
	# 	raise Http404("Product does not exists")
	context = {
		'object': instance
	}
	return render(request, "products/detail.html", context)