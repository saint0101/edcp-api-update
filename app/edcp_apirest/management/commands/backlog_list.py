from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ commande test """

    args = '<team_id>'
    help = 'Affiche la liste des backlogs'
    
    def handle(self, *args, **options):
        self.stdout.write('COUCOU TEST')