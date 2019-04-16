## Django M:N Relationship

> [Many-to-many relationships](https://docs.djangoproject.com/ko/2.1/topics/db/examples/many_to_many/#many-to-many-relationships)
>
> [모델관계 다대다](https://nachwon.github.io/django-relationship/#%EB%8B%A4%EB%8C%80%EB%8B%A4-%EA%B4%80%EA%B3%84-many-to-many-relationship)
>
> [related_name](https://docs.djangoproject.com/ko/2.1/ref/models/fields/#django.db.models.ForeignKey.related_name)

현재 USER : POST = 1 : N 에서는

`post.user`

`user.post_set`

로 서로를 참조/역참조 할 수 있다.

---

만약 User:Post = M:N 으로 설정 후 다시 생각하면,

> user 는 여러 post 에 like 할 수 있고,
>
> post 는 여러 user 로부터 like 받을 수 있다.

```python
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True)
    content = models.TextField()
```

like_users 라는 필드이름으로 설정하면

`post.like_users` 로 게시글에 좋아요한 유저들을 불러 올 수 있지만..

반대로 기존처럼 `user.post_set` 을 했을 때 문제가 생긴다. (**역참조시에 문제 발생**)

> M:N 설정시 related_name 이 없다면 자동으로 `.post_set` 매니저를 사용할 수 있도록 하는데 이 매니저는 이미 1:N 관계에서 사용중인 매니저이다.

- 그래서 내가 작성한 글들(user.post_set) vs 내가 좋아요한 글들(user.post_set) 인지를 django 는 구분 할 수 없다.
- 그래서 user 쪽에서 좋아요한 post 들을 불러올 `related_name` 설정이 필요하다.

---

M:N 설정을 끝내고 db.sqlite 를 살펴보면,

```bash
$ sqlite3 db.sqlite3
sqlite> .tables
```

기존 posts_post 테이블에 새로운 컬럼이 생기는 것이 아니라,

`posts_post_like_users` 라는 새로운 테이블이 만들어진다.

> |  id  | post_id | user_id |
> | :--: | :-----: | :-----: |
> |  .   |    .    |    .    |

---

그렇다면 이제 사용가능한 ORM 명령어들은 무엇이 있을까.

`post.user` : 게시글 작성한 유저

`post.like_users` : 게시글 좋아요한 유저 (post에 추가한 MTM 필드명)

`user.post_set` : 유저가 작성한 게시글들

`user.like_posts`  : 유저가 좋아요한 게시글 (related_name 설정)

---

