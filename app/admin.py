from app.models import Draw, UniqueCode, Prize
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'code', 'prize', 'winner', 'try_again', 'retry_used']
    list_filter = ['prize__winner', 'prize__try_again', 'retry_used', 'date']
    search_fields = ['code', 'email', 'prize__label']
    list_display_links = ['id', 'date', 'code']

    def winner(self, obj):
        return obj.prize.winner

    def try_again(self, obj):
        return obj.prize.try_again


@admin.register(UniqueCode)
class UniqueCodeAdmin(admin.ModelAdmin):
    readonly_fields = ["code"]
    list_display = ['id', 'date', 'code', 'used', 'prize']
    list_filter = ['used', 'date']
    list_display_links = ['id', 'date', 'code']


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'label', 'winner', 'try_again']
    list_filter = ['winner', 'try_again']
    list_display_links = ['id', 'label']

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('balance',)

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    list_display = ('username', 'email', 'get_balance', 'is_staff', 'is_active')
    list_select_related = ('userprofile',)

    def get_balance(self, instance):
        return instance.userprofile.balance
    get_balance.short_description = 'Balance'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)