from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.core.management import call_command
from django.utils import timezone
from users.models import CustomUser
from transactions.models import BankAccount


class Command(BaseCommand):
    help = 'Initialize the project by creating a superuser and running migrations.'

    def handle(self, *args, **options):
        
        self.stdout.write('Running migrate...')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations complete.'))

        # Check if there are existing superusers
        if CustomUser.objects.filter(email='admin@gmail.com',is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
            return
    
        # check if there are existing banks
        if BankAccount.objects.filter(name='Northern').exists():
            self.stdout.write(self.style.WARNING('Bank Northern already exists.'))
            return

        # Create a superuser
        try:
            new_bank = BankAccount.objects.create(
                name='Northern',
                balance=100000.00
            )
            self.stdout.write(self.style.SUCCESS('Bank "Northern" created successfully.'))

            admin = CustomUser.objects.create_superuser(
                email='admin@gmail.com',
                password='admin',
                first_name='Admin',
                last_name='User',
                account_number='42230100636',
                balance=0,  
                bank=new_bank,
                date_joined=timezone.now(),
                is_staff=True,
                is_active=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Superuser ["admin@gmil.com"] ["admin"] created successfully.'))

        except IntegrityError:
            self.stdout.write(self.style.ERROR('Failed to create superuser.'))

     
        # Run collectstatic
        call_command('collectstatic', interactive=False)
        self.stdout.write(self.style.SUCCESS('Collectstatic complete.'))

        # add worning message
        


        self.stdout.write(self.style.SUCCESS('Project initialization complete.'))

        self.stdout.write(self.style.WARNING('! ================================================ !'))

        self.stdout.write(self.style.SUCCESS('! ============== E-Banking Solution ============== !'))
        self.stdout.write(self.style.SUCCESS('! ============== Team : "Particle" =============== !'))

        self.stdout.write(self.style.WARNING('! ================================================ !'))

        self.stdout.write(self.style.SUCCESS('You can now login with the superuser credentials.'))
        self.stdout.write(self.style.SUCCESS('Email: admin@gmail.com'))
        self.stdout.write(self.style.SUCCESS('Password: admin'))
        self.stdout.write(self.style.WARNING('Please change the password after logging in.'))

  