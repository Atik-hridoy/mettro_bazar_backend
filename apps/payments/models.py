import uuid
from django.db import models
from apps.orders.models import Order


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VALID', 'Valid / Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('UNATTEMPTED', 'Unattempted'),
    ]

    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    tran_id = models.CharField(max_length=100, unique=True, db_index=True)
    val_id = models.CharField(max_length=100, blank=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='BDT')
    card_type = models.CharField(max_length=50, blank=True, default='')
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='PENDING')
    raw_response = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.tran_id} - {self.status} (৳{self.amount})"
