from django.db import models

from users.models import User


class AbstractSlugModel(models.Model):

    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Ingredient(AbstractSlugModel):

    name = models.CharField(
        max_length=256,
        verbose_name='Название ингредиентов',
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.TextField(verbose_name='Единицы измерения')


class Tag(AbstractSlugModel):

    name = models.CharField(
        max_length=256,
        verbose_name='Тег',
        help_text='Введите название тега',
    )
    color = models.CharField(max_length=16)


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
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipyIngredient')
    tags = models.ManyToManyField(Tag, through='RecipyTag')
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.text[:20]


class RecipyIngredient(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.recipy} {self.ingredients}'


class RecipyTag(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipy} {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liker',
        verbose_name='Избраник',
    )
    recipy = models.ForeignKey(
        Recipy,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = [['recipy', 'user']]

    def __str__(self) -> str:
        return f'{self.recipy}'
    

class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoper',
        verbose_name='Покупатель',
    )
    recipy = models.ForeignKey(
        Recipy,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Покупки',
    )

    class Meta:
        verbose_name = 'Покупки'
        verbose_name_plural = 'покупки'
        unique_together = [['recipy', 'user']]

    def __str__(self) -> str:
        return f'{self.recipy}'


