from django.core.management.base import BaseCommand
from PIL import features

class Command(BaseCommand):
    help = 'Checks the health of the Pillow library and its support for common image formats.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Pillow Health Check ---'))
        
        # Check for available features
        available_features = {
            'JPEG': features.check_feature('jpeg'),
            'PNG': features.check_feature('png'),
            'ZLIB (PNG compression)': features.check_feature('zlib'),
        }

        for feature, is_available in available_features.items():
            if is_available:
                self.stdout.write(self.style.SUCCESS(f'✅ {feature} support is available.'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ {feature} support is NOT available.'))

        self.stdout.write(self.style.SUCCESS('-------------------------'))

        if all(available_features.values()):
            self.stdout.write(self.style.SUCCESS('Pillow appears to be correctly installed and supports major image formats.'))
        else:
            self.stdout.write(self.style.WARNING('Pillow might be missing required system libraries for some image formats.'))
            self.stdout.write(self.style.WARNING('Please try reinstalling Pillow with the necessary development libraries for your OS.'))
            self.stdout.write(self.style.WARNING('For macOS with Homebrew: brew install libjpeg zlib'))
