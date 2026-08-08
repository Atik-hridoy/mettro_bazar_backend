import os
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from apps.products.models import Banner, Category, Product, WeightVariant, CookingStep
from apps.delivery.models import DeliveryZone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds initial categories, products, banners, delivery zones from mock_data folder.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding data from mock_data folder..."))
        mock_dir = settings.BASE_DIR / 'mock_data'

        # 1. Superusers
        u1, _ = User.objects.get_or_create(phone='01700000000')
        u1.set_password('admin1234')
        u1.is_staff = True
        u1.is_superuser = True
        u1.is_active = True
        u1.name = 'Metro Bazar Admin'
        u1.save()

        u2, _ = User.objects.get_or_create(phone='admin')
        u2.set_password('admin1234')
        u2.is_staff = True
        u2.is_superuser = True
        u2.is_active = True
        u2.name = 'Admin User'
        u2.save()

        self.stdout.write(self.style.SUCCESS("Superusers created (01700000000 / admin with pass: admin1234)"))

        # 2. Categories from mock_data/categories.json
        categories_file = mock_dir / 'categories.json'
        if categories_file.exists():
            with open(categories_file, 'r', encoding='utf-8') as f:
                categories_data = json.load(f)
            
            cat_map = {}
            for cat in categories_data:
                c, _ = Category.objects.update_or_create(
                    id=cat['id'],
                    defaults={
                        'name': cat['name'],
                        'slug': cat['slug'],
                        'icon_name': cat.get('icon_name') or cat.get('iconName', 'Utensils'),
                        'is_active': True
                    }
                )
                cat_map[cat['slug']] = c

            self.stdout.write(self.style.SUCCESS(f"Seeded {len(categories_data)} categories."))

        # 3. Banners from mock_data/banners.json
        banners_file = mock_dir / 'banners.json'
        if banners_file.exists():
            with open(banners_file, 'r', encoding='utf-8') as f:
                banners_data = json.load(f)

            for b in banners_data:
                Banner.objects.update_or_create(
                    id=b['id'],
                    defaults={
                        'title': b['title'],
                        'subtitle': b.get('subtitle', ''),
                        'badge_text': b.get('badge_text') or b.get('badgeText', ''),
                        'image_url': b.get('image_url') or b.get('image', ''),
                        'button_text': b.get('button_text') or b.get('buttonText', 'Shop Now'),
                        'button_link': b.get('button_link') or b.get('buttonLink', '#products'),
                        'banner_type': b.get('banner_type') or b.get('bannerType', 'hero'),
                        'is_active': b.get('is_active', True),
                        'order': b.get('order', 1)
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(banners_data)} homepage banners."))

        # 4. Delivery Zones
        delivery_zones = [
            {"area_name": "Dhaka City (Inside Ring Road)", "city": "Dhaka", "delivery_charge": 60.00, "estimated_delivery_time": "30-45 mins"},
            {"area_name": "Uttara / Gazipur", "city": "Dhaka North", "delivery_charge": 80.00, "estimated_delivery_time": "45-60 mins"},
            {"area_name": "Old Dhaka / Lalbagh", "city": "Dhaka South", "delivery_charge": 70.00, "estimated_delivery_time": "40-50 mins"},
            {"area_name": "Suburbs (Savar / Narayanganj)", "city": "Greater Dhaka", "delivery_charge": 120.00, "estimated_delivery_time": "60-90 mins"},
        ]

        for dz in delivery_zones:
            DeliveryZone.objects.update_or_create(
                area_name=dz['area_name'],
                defaults=dz
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(delivery_zones)} delivery zones."))

        # 5. Products from mock_data/products.json
        products_file = mock_dir / 'products.json'
        if products_file.exists():
            with open(products_file, 'r', encoding='utf-8') as f:
                products_data = json.load(f)

            for item in products_data:
                cat_slug = item.get('category')
                cat = Category.objects.filter(slug=cat_slug).first() or Category.objects.first()

                product, _ = Product.objects.update_or_create(
                    id=item['id'],
                    defaults={
                        'name': item['name'],
                        'category': cat,
                        'price': item['price'],
                        'image_url': item.get('image', ''),
                        'description': item['description'],
                        'is_popular': item.get('isPopular', item.get('is_popular', False)),
                        'badge_text': item.get('badgeText', item.get('badge_text', '')),
                        'is_ready_to_cook': item.get('isReadyToCook', item.get('is_ready_to_cook', True)),
                        'preparation_time_minutes': item.get('preparationTimeMinutes', item.get('preparation_time_minutes', 15)),
                        'is_active': True
                    }
                )

                # Weight Variants
                for wv in item.get('weightVariants', item.get('weight_variants', [])):
                    WeightVariant.objects.update_or_create(
                        id=wv['id'],
                        defaults={
                            'product': product,
                            'weight': wv['weight'],
                            'price': wv['price'],
                            'stock': wv['stock']
                        }
                    )

                # Cooking Steps
                for cs in item.get('cookingSteps', item.get('cooking_steps', [])):
                    step_num = cs.get('stepNumber', cs.get('step_number', 1))
                    CookingStep.objects.update_or_create(
                        id=f"{product.id}-cs-{step_num}",
                        defaults={
                            'product': product,
                            'step_number': step_num,
                            'title': cs['title'],
                            'instruction': cs['instruction']
                        }
                    )

            self.stdout.write(self.style.SUCCESS(f"Seeded {len(products_data)} products from mock_data."))
