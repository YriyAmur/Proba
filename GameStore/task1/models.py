from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Buyer(models.Model):
    objects = models
    name = models.CharField(max_length=100)  # Имя покупателя
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Баланс
    age = models.IntegerField()  # Возраст

    def __str__(self):
        return self.name


class Game(models.Model):
    objects = models
    title = models.CharField(max_length=100)  # Название игры
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Цена игры
    size = models.DecimalField(max_digits=10, decimal_places=2)  # Размер файлов игры
    description = models.TextField()  # Описание игры
    age_limited = models.BooleanField(default=False)  # Ограничение по возрасту
    buyers = models.ManyToManyField(Buyer, related_name='games')  # Покупатели

    def __str__(self):
        return self.title
