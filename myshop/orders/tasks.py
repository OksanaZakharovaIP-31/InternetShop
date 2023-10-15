from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа.
    """
    print('here')
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\nYou have successfully placed an order. ' \
              f'Your order ID is {order.id}.'
    send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
              [order.email])
    # mail_sent = send_mail(subject,
    #                       message,
    #                       settings.EMAIL_HOST_USER,
    #                       [order.email])
    return None # mail_sent
