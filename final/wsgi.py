import os
import django
from django.core.wsgi import get_wsgi_application

# 1. Environment sozlanadi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings')

# 2. Djangoni majburan to'liq yuklaymiz (Xatolikni yo'qotadigan qism)
django.setup()

# 3. WSGI dasturini ishga tushiramiz
application = get_wsgi_application()

# 4. Vercel uchun o'zgaruvchi
app = application


