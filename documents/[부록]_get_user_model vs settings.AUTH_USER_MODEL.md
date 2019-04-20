## get_user_model vs settings.AUTH_USER_MODEL

>  [Django using get_user_model vs settings.AUTH_USER_MODEL](https://stackoverflow.com/questions/24629705/django-using-get-user-model-vs-settings-auth-user-model)

If you try to user `get_user_model()` when creating ForeignKey, ManyToManyField or OneToOneField you may have circular import issues. If you change some settings (e.g. the order of `INSTALLED_APPS`) it might very well break the import and you will have to spend additional time debugging.

Using `settings.AUTH_USER_MODEL` will delay the retrieval of the actual model class until all apps are loaded. get_user_model will attempt to retrieve the model class at the moment your app is imported the first time.

만약 models.py Field 설정에 `get_user_model()` 을 사용하고 커스텀 유저 모델을 만들면 서버 실행시 에러가 발생합니다.

django 문서와 스택오버플로우를 토대로 설명하자면 `get_user_model()` 은 클래스를 호출하는 것인데 가장 먼저 서버가 켜질 때 모델이 `앱이름.커스텀한유저모델(ex. accounts.User)` 을 가르키고 있어 해당 app의 커스텀 된 User 모델을 불러오려합니다.
하지만 아직 해당 app 이 `INSTALLED_APPS`  에 작성된 순서 때문에 호출되지 않은 상태라 `get_user_model()` 이 어떤 app 의 User 모델을 가르키는지 django 가 모르는 상황이 발생하는 것입니다.

그래서 모델에서는 타입이 string 이어서 즉시 가르킬 수 있는 `settings.AUTH_USER_MODEL` 을 사용하라고 공식문서는 권장하고 있습니다.

> 결론 내리자면
>
> 1. 모든 곳에서 User 를 호출할 땐 `get_user_model()`
> 2. 단, models.py 만 예외. `settings.AUTH_USER_MODEL`

