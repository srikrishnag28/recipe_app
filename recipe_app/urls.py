from django.contrib import admin
from django.urls import path
from recipe import views as recipe_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipe/', recipe_views.Home, name='recipe-home'),
    path('login/', recipe_views.Login, name='login'),
    path('logout/', recipe_views.Logout, name='logout'),
    path('register/', recipe_views.Register, name='register'),
    path('delete/<int:id>/', recipe_views.delete_recipe, name='delete-recipe'),
    path('update/<int:id>/', recipe_views.update_recipe, name='update-recipe')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
