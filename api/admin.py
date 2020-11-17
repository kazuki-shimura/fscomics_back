# adminダッシュボードを使用するための設定ファイル

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models    # ←←← この記載があることで作成したmodels.pyの内容を利用できる


# カスタマイズしたUserのモデルは特殊でadminダッシュボード自体のレイアウトも変更しなければいけない
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )



# adminダッシューボードからUser,Profile,Review,Commentの作成が可能になる
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Review)
admin.site.register(models.Comment)


