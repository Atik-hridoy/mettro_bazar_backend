from rest_framework import serializers
from .models import Banner, Category, Product, WeightVariant, CookingStep


class BannerSerializer(serializers.ModelSerializer):
    badgeText = serializers.CharField(source='badge_text', read_only=True)
    buttonText = serializers.CharField(source='button_text', read_only=True)
    buttonLink = serializers.CharField(source='button_link', read_only=True)
    bannerType = serializers.CharField(source='banner_type', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = [
            'id',
            'title',
            'subtitle',
            'badgeText',
            'badge_text',
            'image',
            'buttonText',
            'button_text',
            'buttonLink',
            'button_link',
            'bannerType',
            'banner_type',
            'is_active',
            'order'
        ]

    def get_image(self, obj) -> str:
        request = self.context.get('request')
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url or '/images/hero.jpg'


class CategorySerializer(serializers.ModelSerializer):
    iconName = serializers.CharField(source='icon_name', required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'iconName', 'icon_name', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'slug': {'required': False},
        }

    def create(self, validated_data):
        # Auto-generate slug from name if not provided
        if 'slug' not in validated_data or not validated_data['slug']:
            from django.utils.text import slugify
            validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class WeightVariantSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = WeightVariant
        fields = ['id', 'weight', 'price', 'stock']


class CookingStepSerializer(serializers.ModelSerializer):
    stepNumber = serializers.IntegerField(source='step_number')

    class Meta:
        model = CookingStep
        fields = ['id', 'stepNumber', 'step_number', 'title', 'instruction']


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.slug', read_only=True)
    price = serializers.FloatField()
    badgeText = serializers.CharField(source='badge_text', read_only=True)
    isPopular = serializers.BooleanField(source='is_popular', read_only=True)
    isReadyToCook = serializers.BooleanField(source='is_ready_to_cook', read_only=True)
    preparationTimeMinutes = serializers.IntegerField(source='preparation_time_minutes', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'category', 
            'price', 
            'image', 
            'description', 
            'badgeText',
            'badge_text', 
            'isPopular',
            'is_popular', 
            'isReadyToCook',
            'is_ready_to_cook', 
            'preparationTimeMinutes',
            'preparation_time_minutes', 
            'is_active',
            'created_at'
        ]

    def get_image(self, obj) -> str:
        request = self.context.get('request')
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url or ''


class ProductDetailSerializer(ProductListSerializer):
    weightVariants = WeightVariantSerializer(source='weight_variants', many=True, read_only=True)
    weight_variants = WeightVariantSerializer(many=True, read_only=True)
    cookingSteps = CookingStepSerializer(source='cooking_steps', many=True, read_only=True)
    cooking_steps = CookingStepSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            'weightVariants',
            'weight_variants',
            'cookingSteps',
            'cooking_steps'
        ]


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
