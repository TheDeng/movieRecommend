from django.contrib import admin

# Register your models here.
from import_export import resources
from movie.models import User,Movie,rating
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):

    class Meta:
        model = User

class MovieResource(resources.ModelResource):

    class Meta:
        model = Movie

class RatingResource(resources.ModelResource):

    class Meta:
        model = rating

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    # list_display = ('name', 'author', 'author_email', 'imported', 'published', 'price', 'categories')
    # search_fields = ('name', 'author','published')
    # date_hierarchy = 'date'

    resource_class = UserResource
    resource_class = RatingResource

class ratingAdmin(admin.ModelAdmin):
    list_display = ('rating_id','user_md5', 'movie_id', 'rating','time')
admin.site.register(rating,ratingAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id','name', 'alias', 'actors','cover','directors','score','votes','genres','languages',
                    'mins','official_site','regions','release_date','slug','storyline','tags','year','actor_ids','director_ids')
admin.site.register(Movie,MovieAdmin)


