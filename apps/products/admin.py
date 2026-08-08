from django.contrib import admin
from .models import Banner, Category, Product, WeightVariant, CookingStep


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'banner_type', 'badge_text', 'button_text', 'order', 'is_active', 'created_at')
    list_filter = ('banner_type', 'is_active')
    search_fields = ('title', 'subtitle', 'badge_text')


class WeightVariantInline(admin.TabularInline):
    model = WeightVariant
    extra = 1


class CookingStepInline(admin.TabularInline):
    model = CookingStep
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_popular', 'is_ready_to_cook', 'is_active', 'created_at')
    list_filter = ('category', 'is_popular', 'is_ready_to_cook', 'is_active')
    search_fields = ('name', 'description')
    inlines = [WeightVariantInline, CookingStepInline]


@admin.register(WeightVariant)
class WeightVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight', 'price', 'stock', 'created_at')
    list_filter = ('product__category',)
    search_fields = ('product__name', 'weight')


@admin.register(CookingStep)
class CookingStepAdmin(admin.ModelAdmin):
    list_display = ('product', 'step_number', 'title', 'created_at')
    search_fields = ('product__name', 'title')
