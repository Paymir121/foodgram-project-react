from django.db import models

from users.models import User


class AbstractSlugModel(models.Model):

    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Ingredients(AbstractSlugModel):

    name = models.CharField(
        max_length=256,
        verbose_name='Ингредиенты',
        help_text='Введите название ингридиента',
    )
    count = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )

    units = models.TextField(verbose_name='Единицы измерения')


class Tag(AbstractSlugModel):

    name = models.CharField(
        max_length=256,
        verbose_name='Тег',
        help_text='Введите название тега',
    )
    HEX_code = models.CharField(max_length=16)


class Recipy(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Рецепт',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingredients = models.ManyToManyField(Ingredients,
                                         through='RecipyIngredients')
    tag = models.ManyToManyField(Tag, through='RecipyTag')
    time_cooking = models.IntegerField()


    def __str__(self):
        return self.text[:20]


class RecipyIngredients(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipy} {self.ingredients}'


class RecipyTag(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipy} {self.tag}'

