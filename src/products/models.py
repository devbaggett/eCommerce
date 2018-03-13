from django.db import models
import random
import os # parse filename for extension (e.g. png, gif, etc..)

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath) # if you passed in a whole path
	name, ext = os.path.splitext(base_name) 
	return name, ext

# can change filename and use a random integer for that filename
def upload_image_path(instance, filename):
	print(instance)
	print(filename)
	new_filename = random.randint(1,3434934934)
	name, ext = get_filename_ext(filename) # gets us new filename and new filename extension
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "products/{new_filename}/{final_filename}".format(
		new_filename=new_filename, 
		final_filename=final_filename) # gives us a more robust way of naming these files


class ProductManager(models.Manager):
	def featured(self):
		return self.get_queryset().filter(featured=True)

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
		if qs.count() == 1:
			return qs.first() # getting the individual instance/object
		return None


class Product(models.Model):
	title = models.CharField(max_length=120)
	slug = models.SlugField(blank=True)
	description = models.TextField()
	price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	# null means in the db this could be empty value, blank means not required in django
	# allows us to add image upload option to admin section
	image = models.ImageField(upload_to=upload_image_path, null=True, blank=True) 
	# switched products/ with upload_image_path
	# changed FileField to ImageField so only images could be uploaded
	featured = models.BooleanField(default=False)

	objects = ProductManager() # extending the defaults
	
	def get_absolute_url(self):
		return "/products/{slug}/".format(slug=self.slug)

	def __str__(self):
		return self.title