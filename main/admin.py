from django.contrib import admin

from main.models import *

admin.site.register([Book, Account, Wishlist, Image])
