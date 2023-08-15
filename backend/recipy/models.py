from django.db import models

# from users.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название ингредиентов',
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.TextField(verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    name = models.CharField(
        max_length=256,
        verbose_name='Тег',
        help_text='Введите название тега',
    )
    color = models.CharField(max_length=16)

    class Meta:
        verbose_name = 'Таг'
        verbose_name_plural = 'Таги'

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text[:20]


class RecipyIngredient(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.recipy} {self.ingredients}'


class RecipyTag(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Таг в рецепте'
        verbose_name_plural = 'Таги в рецептах'

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
        related_name='favorites',
        verbose_name='Избранное',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
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
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        unique_together = [['recipy', 'user']]

    def __str__(self) -> str:
        return f'{self.recipy}'
