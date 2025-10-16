from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_email(course_id, emails):
    from lms.models import Course
    course = Course.objects.get(id=course_id)

    subject = f"Обновление курса: {course.title}"
    message = f"Курс '{course.title}' был обновлён. Проверьте новые материалы!"

    send_mail(
        subject,
        message,
        'noreply@example.com',
        emails,
        fail_silently=False,
    )
