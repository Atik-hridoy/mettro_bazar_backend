from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('tran_id', 'order', 'amount', 'currency', 'card_type', 'status', 'created_at')
    list_filter = ('status', 'currency', 'card_type', 'created_at')
    search_fields = ('tran_id', 'val_id', 'order__order_number', 'order__customer_name')
    readonly_fields = ('tran_id', 'order', 'amount', 'currency', 'card_type', 'status', 'raw_response', 'created_at', 'updated_at')
    ordering = ('-created_at',)
