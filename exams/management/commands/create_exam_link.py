from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from exams.models import Exam, ExamLink


class Command(BaseCommand):
    help = 'Create an exam link for testing'

    def add_arguments(self, parser):
        parser.add_argument('exam_id', type=int, help='Exam ID')
        parser.add_argument('--days', type=int, default=30, help='Expiration days (default: 30)')
        parser.add_argument('--max-uses', type=int, default=None, help='Maximum uses (default: unlimited)')
        parser.add_argument('--password', type=str, default='1234', help='Resume password (default: 1234)')

    def handle(self, *args, **options):
        exam_id = options['exam_id']
        days = options['days']
        max_uses = options['max_uses']
        password = options['password']

        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Exam with ID {exam_id} not found'))
            return

        # Create exam link
        link = ExamLink.objects.create(
            exam=exam,
            expires_at=timezone.now() + timedelta(days=days),
            max_uses=max_uses,
            resume_password=password,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(f'Exam Link Created Successfully!'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(f'Exam: {exam.title}'))
        self.stdout.write(self.style.SUCCESS(f'Link Token: {link.unique_token}'))
        self.stdout.write(self.style.SUCCESS(f'Expires: {link.expires_at.strftime("%Y-%m-%d %H:%M")}'))
        self.stdout.write(self.style.SUCCESS(f'Max Uses: {max_uses if max_uses else "Unlimited"}'))
        self.stdout.write(self.style.SUCCESS(f'Resume Password: {password}'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(f'URL: http://localhost:8000/exam/start/{link.unique_token}/'))
        self.stdout.write(self.style.SUCCESS('='*70))
