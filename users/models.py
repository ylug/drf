from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="город", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="аватар", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payments(models.Model):

    CASH = "Наличные"
    TRANSFER = "Перевод"

    PAYMENT_METHOD_CHOISE = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод")
    ]

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, verbose_name='Студент')
    date_payment = models.DateField(verbose_name='Дата платежа', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='отдельно оплаченный урок', **NULLABLE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=20, verbose_name='способ оплаты', choices=PAYMENT_METHOD_CHOISE)
    payment_link = models.URLField(max_length=400, verbose_name='ссылка для оплаты', null=True, blank=True)
    payment_id = models.CharField(max_length=255, verbose_name='идентификатор платежа', null=True, blank=True)

    def __str__(self):
        return f"{self.user}: ({self.paid_course if self.paid_course else self.paid_lesson})"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежы"
