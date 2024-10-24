from app.models import Draw, UniqueCode, Prize
from django.contrib import admin


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
