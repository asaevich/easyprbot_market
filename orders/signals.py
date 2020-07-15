from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, SalesStatistic


@receiver(post_save, sender=OrderItem)
def update_sales_statistic(sender, instance, created, **kwargs):
    if created:
        creator = instance.product.creator
        statistic = SalesStatistic.objects.get(author=creator)

        statistic.cash_amount += instance.price
        statistic.sold += 1
        statistic.save()
