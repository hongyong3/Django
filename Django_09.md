[TOC]

## Django_09

**Content**

0. Authentication
1. Sign up
2. Login
3. Logout
4. 매끄럽게
5. 회원 탈퇴
6. 회원 수정
7. 비밀번호 변경
8. Authorization
9. auth_form 합치기
10. User - Board

> 190408~09 Mon~Tue

---

### 0. Authentication(인증)

> [Using the Django authentication system](https://docs.djangoproject.com/en/2.1/topics/auth/default/#using-the-django-authentication-system)

- 이전 ModelForm 수업에 이어서 진행
- django 에는 기본적으로 로그인 기능이 구현되어 있다.
  - createsuperuser 로 계정을 만들고, admin 페이지에서 로그인을 할 수 있었던 이유.
- 기능 자체는 구현이 되어 있으므로 우리는 로그인 페이지만 만들면 된다.
  - 하지만, `게시글 작성` 과는 다른 `로그인` 이라는 새로운 기능을 만드므로 새 app인 `accounts` 을 만든다.

```bash
$ python manage.py startapp accounts
```

```python
# settings.py
INSTALLED_APPS = [
    'boards.apps.BoardsConfig',
    'accounts.apps.AccountsConfig',
```

```python
# myform/urls.py
path('accounts/', include('accounts.urls')),
```

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
]
```

> app 이름이 반드시 accounts 일 필요는 없으나, 후에 auth 관련된 기본 값들이 accounts 로 되어 있는 모습을 발견하게 될 것이다. 되도록 accounts 라는 이름을 사용한다.

---

### 1. Sign up

> [Using the Django authentication system - Built-in forms](https://docs.djangoproject.com/ko/2.2/topics/auth/default/#module-django.contrib.auth.forms)

- 회원가입은 CRUD 로직에서 User 를 Create 하는 것과 같다.
- `class User` Model 은 django 가 미리 만들어 놨다.
- 그리고 이 User 모델과 연동된 ModelForm 인 `UserCreationForm` 도 만들어져 있다.

```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
```

```python
# accounts/urls.py
path('signup/', views.signup, name='signup')
```

```django
<!-- accounts/signup.html -->
{% extends 'boards/base.html' %}
{% block body %}
{% load crispy_forms_tags %}

<h1>회원 가입</h1>
<form action="" method="POST">
    {% csrf_token %}
    {{ form|crispy }}
    <input type="submit" value="Submit"/>
</form>
{% endblock %}
```

> admin 페이지에서 새로운 user 가 생겼는지 확인, User Model 은 admin 페이지에 이미 등록도 되어 있다.

---

### 2. Login

- 새로운 user 를 만들었으니, 만든 user 정보로 로그인을 해보자.
- 로그인도 Create 로직과 같지만 Session 을 Create 하는 것이다.
  - Session 이란 브라우저의 정보를 가져와 임시로 들고 있도록해서, 지금 이 페이지를 보는게 누구인지 구분하도록 서버 쪽에서 정보를 들고 있는 것을 의미한다. (간단 설명)
  - 그래서 이 session 은 사용자가 로그인 하면, 로그인한 사용자의 정보를 페이지가 전환되더라도 계속 들고 있는다. (로그아웃 버튼을 누르거나, sesstion 만료시간이 지날 때 까지 들고 있는다.
- Session 은 잠시 뒤로 넘기고 우리는 django 가 세션 관리를 알아서 모두 해준다는 것을 알고 가자.
- User 를 만드는 ModelForm 은 `AuthenticationForm` 을 사용한다.
  - `auto_login` 은 session 에 user 정보를 기록해서 계속 들고 있도록 한다. 즉, 로그인을 한다.
  - 이름을 변경해서 사용하는 이유는 view 함수인 login 과의 혼동을 방지하기 위해 변경한다.

```python
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('boards:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)
```

```python
# accounts/urls.py
path('login/', views.login, name='login'),
```

```django
<!-- accounts/login.html -->
{% extends 'boards/base.html' %}
{% block body %}
{% load crispy_forms_tags %}

<h1>로그인</h1>
<form action="" method="POST">
    {% csrf_token %}
    {{ form|crispy }}
    <input type="submit" value="Submit"/>
</form>
{% endblock %}
```

- 로그인 되었는지 확일할 방법이 없으니 다음과 같이 설정해본다.

  ```django
  <!-- base.html -->
  <body>
      <div class="container">
      <h1>현재 유저는 {{ user.username }} !</h1>
      <hr>
          {% block body %}
          {% endblock %}
      </div>
  ```

---

### 3. Logout

> [django User model](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#user-model)

- 로그아웃은 CRUD 에서 Session 을 Delete 하는 로직이다.

```python
# accounts/views.py
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('boards:index')
```

```python
# accounts/urls.py
path('logout/', views.logout, name='logout'),
```

---

### 4. 매끄럽게

#### 4.1 링크 분기

- `user.is_authenticated` 를 통해 로그인 되었는지를 판단할 수 있다.
- 이를 통해 템플릿을 매끄럽게 작업해보자.
  - 로그인과 비로그인 상태에서 보이는 링크를 다르게 변경.

```django
<!-- base.html -->
<body>
    <div class="container">
    {% if user.is_authenticated %}
        <h1>
            안녕, {{ user.username }}
            <a href="{% url 'accounts:logout' %}">로그아웃</a>
        </h1>
    {% else %}
        <h1>
            <a href="{% url 'accounts:login' %}">로그인</a>
            <a href="{% url 'accounts:signup' %}">회원가입</a>
        </h1>
    {% endif %}
    <hr>
        {% block body %}
        {% endblock %}
    </div>
```

```django
<!-- boards/index.html -->
{% extends 'boards/base.html' %}
{% block body %}
<h1>게시글 목록</h1>
{% if user.is_authenticated %}
    <a href="{% url 'boards:create' %}">새 글 작성</a>
{% else %}
    <a href="{% url 'accounts:login' %}">새 글을 쓰려면 로그인 하세요.</a>
{% endif %}
```

#### 4.2 회원가입 후 바로 로그인 상태로 전환

- 현재 회원가입이 완료되면 로그인 되지 않은 상태로 index 페이지로 그냥 넘어간다.
- 그래서 회원가입과 동시에 로그인상태로 만들어 준다.

```python
# accounts/views.py
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()							# 1
            auth_login(request, user)				# 2
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
```

#### 4.3 로그인 되어 있으면 로그인/회원가입 페이지 못보게 설정

- 로그인 되어있는 상태라면 로그인과 회원가입 페이지에 접근 할 수 없도록 설정한다.

```python
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
```

```python
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
```

---

