# EduPlatform (Django)

Multi-tenant **School Management System** for Nursery, Primary & Secondary schools.

| Layer | Technology |
|-------|------------|
| Frontend | HTML / CSS / vanilla JavaScript (Django templates) |
| Backend | Django 5 |
| Database | **SQLite** (local) · **PostgreSQL** (production via `DATABASE_URL`) |
| Deploy | PythonAnywhere · Railway · Google Cloud Run |
| Client | **PWA** — installable, offline shell, service worker |

---

## Features

- Multi-tenant schools (permanent **School ID** + **Tenant ID**)
- Roles: Super Admin, School Admin, Teacher, Student, Parent
- Classes, subjects, student enrolment
- Attendance marking (+ offline queue helper in JS)
- Results: draft → submit → approve → publish
- Printable report cards
- Fees: items, invoices, payment recording
- Notices & internal messages
- Tenant middleware (school always from authenticated user)

---

## Progressive Web App (PWA)

- Web app manifest: `/static/manifest.webmanifest`
- Service worker: `/sw.js` (root scope)
- Offline page: `/offline/`
- **Install app** button appears when the browser supports install
- Caches app shell (CSS/JS/login) for offline use
- Network-first for pages; cache-first for static assets

**Requirements for install:** HTTPS (or localhost), valid manifest + SW.

## Quick start (local / SQLite)

```bash
cd eduplatform-django
python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# set DJANGO_SECRET_KEY

python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/login/

| User | Password | Role |
|------|----------|------|
| `superadmin` | `SuperAdmin@123` | Super Admin |
| `schooladmin` | `SchoolAdmin@123` | School Admin |

---

## PostgreSQL

```env
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com
```

Then:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## Deploy

### Railway

1. New project from GitHub repo  
2. Add **PostgreSQL** plugin  
3. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=.up.railway.app`  
4. `DATABASE_URL` is injected automatically  
5. Deploy (uses root `Procfile` / `Dockerfile`)

### Google Cloud Run

```bash
gcloud builds submit --config deploy/cloudrun/cloudbuild.yaml
# Or: docker build -t eduplatform -f Dockerfile .
# Set env: DATABASE_URL, DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS=*.run.app
```

### PythonAnywhere

See `deploy/pythonanywhere/README.md`.

---

## GitHub

```bash
cd eduplatform-django
git init
git add .
git commit -m "EduPlatform Django SMS"
git branch -M main
git remote add origin https://github.com/YOU/eduplatform-django.git
git push -u origin main
```

A ready zip is also provided: `eduplatform-django.zip`.

---

## Project layout

```
config/           # settings, urls, wsgi
apps/
  accounts/       # users, login, dashboards
  schools/        # multi-tenant school + audit
  academics/      # classes, subjects, students, parents
  attendance/
  results/
  fees/
  notices/
  messaging/
templates/        # HTML
static/css|js     # CSS & JS
deploy/           # platform-specific notes
```

---

## Security notes

- Tenant/school is taken from the **logged-in user**, not from form-supplied tenant IDs alone  
- Change default passwords before production  
- Set a strong `DJANGO_SECRET_KEY`  
- Use PostgreSQL + `DEBUG=False` in production  

## Railway — GitHub deployment (recommended)

1. Push the project to a GitHub repository. Keep `.env` out of GitHub.
2. In Railway, create a new project and choose **Deploy from GitHub Repo**.
3. Add a **PostgreSQL** service to the Railway project.
4. In the web service Variables, set:
   - `DJANGO_SECRET_KEY` = a long random secret
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` = `.up.railway.app`
   - `CSRF_TRUSTED_ORIGINS` = `https://YOUR-APP.up.railway.app`
5. Railway supplies `DATABASE_URL` from the PostgreSQL service.
6. Deploy. The included `start.sh` automatically creates/apply migrations, collects static files, and starts Gunicorn.
7. After the first successful deployment, open the Railway-generated domain and test `/login/` and `/admin/`.

### Railway uploaded files

Student/staff photos, signatures, and other uploads are stored under `media/`. Railway's filesystem is ephemeral unless a **Volume** is attached. For a production school system, attach a Railway Volume mounted at `/app/media`, or later move media storage to an object-storage service.

### Important

Do not commit real passwords, API keys, `DATABASE_URL`, or `.env` to GitHub. Set them in Railway Variables instead.
