from django.core.management.base import BaseCommand
from kiosk.models import Category


class Command(BaseCommand):
    help = 'Add relevant emojis to existing categories'
    
    def handle(self, *args, **options):
        # Define emoji mappings for common cannabis categories
        emoji_mappings = {
            'All Products': '🌿',
            'Flower': '🌸',
            'Edibles': '🍫',
            'Concentrates': '💎',
            'Vapes': '💨',
            'Topicals': '🧴',
            'Rools': '🚬',  # Pre-rolls/Joints
            'Test Flower': '🧪',
            'Test Category': '🔬',
            'Pre-Rolls': '🚬',
            'Accessories': '🛍️',
            'Beverages': '🥤',
            'Tinctures': '💧',
            'Capsules': '💊',
        }
        
        updated_count = 0
        created_count = 0
        
        for category_name, emoji in emoji_mappings.items():
            try:
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'emoji': emoji}
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created new category: {category_name} {emoji}'
                        )
                    )
                elif not category.emoji:
                    category.emoji = emoji
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated category: {category_name} {emoji}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Category {category_name} already has emoji: {category.emoji}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error processing {category_name}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_count} new categories, '
                f'updated {updated_count} existing categories with emojis.'
            )
        )
