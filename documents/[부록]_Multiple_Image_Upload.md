## [부록] Multiple Image Upload

### 0. FormSet

> [FormSet](https://docs.djangoproject.com/ko/2.1/topics/forms/formsets/#module-django.forms.formsets)

- formset 을 사용해 여러 이미지를 업로드 하는 방법.

```python
# posts/models.py
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Post(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
            upload_to='posts/images',
            processors=[ResizeToFill(600, 600)],
            format='JPEG',						
            options={'quality': 90},						
        )
```

```python
# posts/forms.py
from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file',]
```

- 이렇게되면 하나의 레코드를 만드는 form 이다. 하지만 우리는 여러 이미지를 하나의 게시글에 올려야 한다.

- 하나의 이미지를 올리는 form 을 엮어서, 여러개의 이미지를 올릴 수 있게 formset 를 만든다.

  ```python
  # posts/forms.py
  from django.forms import inlineformset_factory
  
  ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=3)
  ```

  > - Post : 부모 모델
  > - Image :  레코드를 생성할 모델
  > - form : 레코드를 생성할 form
  > - extra : 엮을 form 개수 
  > - (번외) `can_order=True` : 이미지의 순서를 정할 수 있다.

### 1. transaction.atomic()

- 데이터베이스에 save 되는 순서를 보장하기 위해서 작성한다. Post 레코드가 먼저 작성되고 나서, 그 아래에 달리는 Image 레코드들이 생겨야 하기 때문에 이 코드가 필요하다.

- `.save()`는 실제 데이터베이스에 레코드를 생성하는 쿼리를 보내는데, Django는 쿼리 요청을 보내고나서 실제로 데이터베이스에 레코드가 저장되었는지 확인을 하고 그 다음 코드들을 실행하는 것이 아니라, **요청을 보내놓고 비동기적으로 바로 다음 코드를 실행**한다.

- 그래서 경우에 따라서는 post가 DB에 저장되지 않았는데 image가 만들어지는, 순서가 뒤집히는 경우가 생길 수 있다. 순서가 뒤집히면 존재하지 않는 post 정보를 가지고 image를 만든 것이 되기 때문에 에러가 발생한다. 이를 방지하기 위해서 Django는 INSERT 순서를 보장하는 `transaction.atomic()`의 사용을 권장하고 있다.

  ```python
  # posts/views.py
  from .forms import PostForm, ImageFormSet
  
  def create(request):
      if request.method == 'POST':
          post_form = PostForm(request.POST)
          image_formset = ImageFormSet(request.POST, request.FILES)
          if post_form.is_valid() and image_formset.is_valid():
              with transaction.atomic():
                  post = post_form.save()
                  image_formset.instance = post
                  image_formset.save()
              return redirect('posts:list')
      else:
          post_form = PostForm()
          image_formset = ImageFormSet()
      context = {
          'post_form': post_form,
          'image_formset': image_formset,
          }
      return render(request, 'posts/form.html', context)
  ```

  ```django
  <!-- posts/form.html -->
  
  <form action="" method="POST" enctype="multipart/form-data">
      {% csrf_token %}
      {% bootstrap_form post_form %}
      {{ image_formset.management_form }}
      {% bootstrap_formset image_formset layout='horizontal' show_label=False %}
      {% buttons submit="Submit" reset="Cancel" %}{% endbuttons %}
    	<a href="{% url 'posts:list' %}" class="btn btn-info">Back</a>
  </form>
  ```

  > `management_form` 은 formset과 관련된 정보(총 몇 개의 form인지, 최대 몇 개의 form에서 넘어오는 지 등)가 hidden input으로 렌더링 된다.
  >
  > - [Understanding the `ManagementForm`](https://docs.djangoproject.com/ko/2.1/topics/forms/formsets/#understanding-the-managementform)
  >
  > ```html
  > <input type="hidden" name="image_set-TOTAL_FORMS" value="3" id="id_image_set-TOTAL_FORMS">
  > <input type="hidden" name="image_set-INITIAL_FORMS" value="0" id="id_image_set-INITIAL_FORMS">
  > <input type="hidden" name="image_set-MIN_NUM_FORMS" value="0" id="id_image_set-MIN_NUM_FORMS">
  > <input type="hidden" name="image_set-MAX_NUM_FORMS" value="1000" id="id_image_set-MAX_NUM_FORMS">
  > ```

- 사진이 잘 업로드 되서 나오는지 확인해보자.

### 2. Image Update

- 여기서는 `transaction.atomic()` 이 필요하지 않다. 이미 Image 생성을 위한 Post가 존재하기 때문에, save 순서로 인해서 발생하는 에러가 없기 때문이다.

  ```python
  def update(request, post_pk):
      post = get_object_or_404(Post, pk=post_pk)
      if request.method == 'POST':
          post_form = PostForm(request.POST, instance=post)
          image_formset = ImageFormSet(request.POST, request.FILES, instance=post)
          if post_form.is_valid() and image_formset.is_valid():
              post_form.save()
              image_formset.save()
              return redirect('posts:list')
      else:
          post_form = PostForm(instance=post)
          image_formset = ImageFormSet(instance=post)
      context = {
          'post_form': post_form,
          'image_formset': image_formset,
          }
      return render(request, 'posts/form.html', context)
  ```

- 이미지 수정이 잘 되는지 확인해본다.

