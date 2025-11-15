from django.contrib import admin
from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_text_preview', 'book', 'user', 'page_number', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['quote_text', 'my_comment', 'book__title']
    filter_horizontal = ['tags']

    def quote_text_preview(self, obj):
        return obj.quote_text[:75] + '...' if len(obj.quote_text) > 75 else obj.quote_text
    quote_text_preview.short_description = 'Quote'
