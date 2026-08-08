import uuid
from django.db import models


class Banner(models.Model):
    BANNER_TYPE_CHOICES = [
        ('hero', 'Hero Banner'),
        ('promo', 'Promotional Banner'),
        ('side', 'Side Banner'),
    ]

    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True, default='')
    badge_text = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, default='', help_text="Fallback static image path if file not uploaded")
    button_text = models.CharField(max_length=50, default='Shop Now')
    button_link = models.CharField(max_length=255, default='#products')
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPE_CHOICES, default='hero')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'banners'
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_banner_type_display()})"


class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    icon_name = models.CharField(max_length=50, default='Utensils', help_text="Lucide icon identifier")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='products',
        db_index=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, default='', help_text="Fallback static image URL/path")
    description = models.TextField(blank=True)
    badge_text = models.CharField(max_length=100, blank=True, default='')
    is_popular = models.BooleanField(default=False)
    is_ready_to_cook = models.BooleanField(default=True)
    preparation_time_minutes = models.PositiveIntegerField(default=15)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class WeightVariant(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='weight_variants'
    )
    weight = models.CharField(max_length=50, help_text="e.g. 500g, 1kg")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'weight_variants'
        verbose_name = 'Weight Variant'
        verbose_name_plural = 'Weight Variants'
        ordering = ['price']

    def __str__(self):
        return f"{self.product.name} - {self.weight} (৳{self.price})"


class CookingStep(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='cooking_steps'
    )
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    instruction = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cooking_steps'
        verbose_name = 'Cooking Step'
        verbose_name_plural = 'Cooking Steps'
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"
