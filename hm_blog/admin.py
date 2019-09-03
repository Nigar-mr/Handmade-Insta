from django.contrib import admin
from hm_blog.models import *

# Register your models here.
from django.contrib import admin
from hm_blog.forms import MyUserChangeForm, MyUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email',
            'profile_image', 'headline', 'location', 'description')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("first_name", "last_name", 'username', 'password1', 'password2'),
        }),
    )
    # The forms to add and change user instances
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'profile_image')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(ContactFormModel)
class ContactFormModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']

class ImageInline(admin.StackedInline):
    model = AddImages
    extra = 5

class  ShotDetailsAdmin(admin.ModelAdmin):
    inlines = [ImageInline]




admin.site.register(SocialSettings)
admin.site.register(ShotDetails, ShotDetailsAdmin)
admin.site.register(Menu)
admin.site.register(Footer)
admin.site.register(RowMenu)
admin.site.register(FooterIcons)
admin.site.register(Unique)
admin.site.register(Verification)
admin.site.register(About)
admin.site.register(AboutTeam)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(ContactUs)
admin.site.register(Comment)
admin.site.register(AddImages)





# admin.sitete.register(SiteHeader)
# admin.site.register(Menu)
# admin.site.register(Menu)
