# 🚀 DAY — Django Framework (In-Depth Session Notes + Examples)

A complete guide to understanding Django architecture, components, patterns, and real-world usage.

---

## 📌 1. What is Django?

- ✔ Django = High-level Python web framework
- ✔ Follows MVT Architecture (Model–View–Template)
- ✔ Batteries-included → lots of features built-in
- ✔ Secure, scalable, production-ready

**Django is used by:**
- Instagram
- Pinterest
- Dropbox backend
- Mozilla
- Spotify internal tools

---

## 📌 2. Django MVT Architecture (Core Concept)

Django uses MVT, NOT MVC.

| MVC | Django |
|-----|--------|
| Model | Model |
| View | Template |
| Controller | View |

- ✔ **M (Model)** → DB Access layer
- ✔ **V (View)** → Business logic
- ✔ **T (Template)** → HTML generation

**Diagram:**
```
Client → URL → View → Model → DB → View → Template → Client
```

---

## 📌 3. Installing Django

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py runserver
```

---

## 📌 4. Django Project Structure (Important)

```
mysite/
    manage.py
    mysite/
        settings.py
        urls.py
        wsgi.py
```

- `manage.py` → command-line tool
- `settings.py` → configuration
- `urls.py` → routing
- `wsgi.py`/`asgi.py` → deployment interface

---

## 📌 5. Creating an App

```bash
python manage.py startapp blog
```

Each app has:

```
blog/
    models.py
    views.py
    urls.py (create manually)
    admin.py
```

---

## 📌 6. Django URL Routing

**Project-level urls.py:**

```python
from django.urls import path, include

urlpatterns = [
    path("blog/", include("blog.urls"))
]
```

**App-level urls.py:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("post/<int:id>", views.post_detail)
]
```

---

## 📌 7. Django Views

**Function-based view:**

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello Django")
```

**Returning HTML with template:**

```python
from django.shortcuts import render

def about(request):
    return render(request, "about.html", {"name": "John"})
```

---

## 📌 8. Django Templates

**Folder structure:**

```
blog/
    templates/
        home.html
```

**Example:**

```html
<h1>Hello {{ name }}</h1>
```

**Template Logic:**

```django
{% if user.is_authenticated %}
    Welcome back {{ user.username }}
{% endif %}
```

**Loop:**

```django
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}
```

---

## 📌 9. Django ORM (Powerful)

**Model example:**

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
```

---

## 📌 10. Database Migrations

**Generate migration:**

```bash
python manage.py makemigrations
```

**Apply migrations:**

```bash
python manage.py migrate
```

---

## 📌 11. ORM Queries (Must Know)

**Create:**

```python
Post.objects.create(title="Django", content="Intro")
```

**Read:**

```python
Post.objects.all()
Post.objects.filter(title__icontains="dj")
Post.objects.get(id=1)
```

**Update:**

```python
p = Post.objects.get(id=1)
p.title = "New Title"
p.save()
```

**Delete:**

```python
Post.objects.filter(id=1).delete()
```

---

## 📌 12. Django Admin (Massive Advantage)

**Enable admin:**

In `blog/admin.py`:

```python
from .models import Post
admin.site.register(Post)
```

**Login at:**
```
/admin
```

**Create superuser:**

```bash
python manage.py createsuperuser
```

---

## 📌 13. Django Forms (HTML + validation)

**Form Class:**

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
```

**Use in view:**

```python
def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
```

---

## 📌 14. Django Model Forms

Automatically generates form from model.

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
```

---

## 📌 15. Django Authentication (Built-in)

**Login:**

```python
from django.contrib.auth import authenticate, login

user = authenticate(username='john', password='pass')
if user:
    login(request, user)
```

**Logout:**

```python
from django.contrib.auth import logout
logout(request)
```

**Protect routes:**

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return ...
```

---

## 📌 16. Django Sessions

**Store data:**

```python
request.session["cart"] = ["item1", "item2"]
```

**Get data:**

```python
cart = request.session.get("cart", [])
```

---

## 📌 17. Django Static & Media Files

**Static files (CSS, JS)**

```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

**Media files (User uploads)**

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

## 📌 18. Django REST Framework (DRF) — API Development

**Install:**

```bash
pip install djangorestframework
```

**Enable in settings:**

```python
INSTALLED_APPS = ["rest_framework"]
```

### ⭐ Create a Serializer:

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
```

### ⭐ API View:

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
```

---

## 📌 19. Class-Based Views (CBV)

**List View:**

```python
from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    model = Post
```

**Detail View:**

```python
class PostDetail(DetailView):
    model = Post
```

**Create View:**

```python
class PostCreate(CreateView):
    model = Post
    fields = ["title", "content"]
```

---

## 📌 20. Django Middleware

Middleware = code that runs before or after every request.

**Example:**

```python
class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("REQUEST:", request.path)
        response = self.get_response(request)
        print("RESPONSE:", response.status_code)
        return response
```

**Enable in settings:**

```python
MIDDLEWARE.append("mysite.middleware.LogMiddleware")
```

---

## 📌 21. Django Signals

Signals allow one part of Django to notify another.

**Example:** Create a profile when a new user registers.

```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

---

## 📌 22. Caching (Performance Optimization)

Django supports:
- ✔ In-memory caching
- ✔ File-based caching
- ✔ Redis caching

**Example:**

```python
from django.views.decorators.cache import cache_page

@cache_page(60)
def home(request):
    return ...
```

---

## 📌 23. Django Deployment

**Production stack:**
- Django + Gunicorn
- Nginx
- PostgreSQL
- Redis (cache / session / MQ)
- Celery (background tasks)
- Docker + Kubernetes (optional)

**Run via gunicorn:**

```bash
gunicorn mysite.wsgi
```

---

## 📌 24. Environment Management

Use `.env` file + `python-decouple`:

```bash
pip install python-decouple
```

**Usage:**

```python
from decouple import config
SECRET_KEY = config("SECRET_KEY")
```

---

## 📌 25. Summary — What You Should Know

By now you should clearly understand:

- ✔ Django Architecture
- ✔ MVT pattern
- ✔ Models, Views, Templates
- ✔ ORM Queries
- ✔ Admin
- ✔ Forms + ModelForms
- ✔ Authentication & Authorization
- ✔ Static and Media
- ✔ Middleware
- ✔ Signals
- ✔ DRF APIs
- ✔ Deployment basics