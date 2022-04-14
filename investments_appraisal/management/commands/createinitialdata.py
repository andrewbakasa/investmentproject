from datetime import date
from random import randrange

from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from silverstrike.models import Account, Category, RecurringTransaction, Split, Transaction
#from invoices.models import Company

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
import logging

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--prune', action='store_true',
                            help='Clears all data before inserting new objects')

    def handle(self, *args, **options):
        if options['prune']:
            self._prune()
        self._initialize()
        today = date.today()
        try:
            start_date = Transaction.objects.filter(
                date__lte=today).latest('date').date.replace(day=1)
        except ObjectDoesNotExist:
            start_date = date(2016, 1, 1)

        while start_date < today:
            self._create_monthly(start_date.year, start_date.month)
            start_date += relativedelta(months=+1)
        Transaction.objects.bulk_create(self.transactions)
        Split.objects.bulk_create(self.splits)

    def _prune(self):
        Account.objects.exclude(account_type=Account.SYSTEM).delete()

        RecurringTransaction.objects.all().delete()
        Transaction.objects.all().delete()
        Split.objects.all().delete()

    def _initialize(self): 
        self.create_groups()       
        # self.work, _ = Company.objects.get_or_create(name='NRZ Global', country='Zimbabwe')
        # self.work, _ = Company.objects.get_or_create(name='NRZ SA', country='SA')
        # self.work, _ = Company.objects.get_or_create(name='NRZ Zambia', country='Zambia')
        # self.work, _ = Company.objects.get_or_create(name='NRZ Kenya', country='Kenya')
        # self.work, _ = Company.objects.get_or_create(name='NRZ Australia', country='Australia')
        # self.work, _ = Company.objects.get_or_create(name='NRZ USA', country='USA')

    def create_groups():
        GROUPS = [ 'admin', 'ceo', 'manager','datacapture', 'editor', 'employee', 'customer','visitor']
        MODELS = [] # ['video', 'article', 'license', 'list', 'page', 'client']
        PERMISSIONS = ['view', ]  # For now only view permission by default for all, others include add, delete, change

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")

