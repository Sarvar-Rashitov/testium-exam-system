from django.core.management.base import BaseCommand
from organizations.models import Organization, OrganizationSettings


class Command(BaseCommand):
    help = 'Create OrganizationSettings for organizations that don\'t have one'

    def handle(self, *args, **options):
        organizations = Organization.objects.all()
        created_count = 0
        
        for org in organizations:
            if not hasattr(org, 'settings'):
                OrganizationSettings.objects.create(organization=org)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created settings for: {org.organization_name}')
                )
        
        if created_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All organizations already have settings!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} settings!')
            )
