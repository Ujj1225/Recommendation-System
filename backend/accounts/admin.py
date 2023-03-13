from django.contrib import admin
from accounts.models import RatedMovies, User,MovieList,MoviesToRecommend
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name','is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name',)}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

class MovieListModelAdmin(admin.ModelAdmin):
  list_display=['id','Title','Year','Genre1','Genre2','Genre3','Director','Cast1','Cast2','Cast3','Cast4']

admin.site.register(MovieList,MovieListModelAdmin)

class RatedMovieModelAdmin(admin.ModelAdmin):
  list_display= ['id','user','movie','rating']

admin.site.register(RatedMovies,RatedMovieModelAdmin)

class MoviesToRecommendModelAdmin(admin.ModelAdmin):
  list_display= ['id','user','movie','priority']

admin.site.register(MoviesToRecommend,MoviesToRecommendModelAdmin)