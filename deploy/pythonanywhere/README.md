# Deploy on PythonAnywhere

1. Create a **Beginner** or paid account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Open **Bash** console and clone or upload this project:
   ```bash
   git clone <your-repo-url> eduplatform
   cd eduplatform
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set environment variables (or edit `.env`):
   ```bash
   export DJANGO_SECRET_KEY='your-long-secret'
   export DJANGO_DEBUG=False
   export DJANGO_ALLOWED_HOSTS='yourusername.pythonanywhere.com'
   # Optional PostgreSQL — otherwise SQLite is used (OK for free tier demos)
   ```
4. Migrate and seed:
   ```bash
   python manage.py migrate
   python manage.py seed_demo
   python manage.py collectstatic --noinput
   ```
5. **Web** tab → Add a new web app → Manual configuration → Python 3.12.
6. Source code: `/home/yourusername/eduplatform`
7. WSGI file — replace contents with:

```python
import os
import sys

path = '/home/yourusername/eduplatform'
if path not in sys.path:
    sys.path.append(path)

from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

8. Static files mapping: URL `/static/` → Directory `/home/yourusername/eduplatform/staticfiles`
9. Reload the web app.
