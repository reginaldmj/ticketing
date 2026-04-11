from importlib import import_module

from django.apps import apps
from django.test import TestCase

from .models import MyTicket, MyUser

fix_invalid_ticket_statuses = import_module(
	'tickets.migrations.0002_fix_ticket_status_default'
).fix_invalid_ticket_statuses


class MyTicketStatusTests(TestCase):
	def setUp(self):
		self.user = MyUser.objects.create_user(
			username='alice',
			password='testpass123',
		)

	def test_ticket_status_defaults_to_new(self):
		ticket = MyTicket.objects.create(
			title='Status default',
			description='Verify default status is new.',
			creator=self.user,
		)

		self.assertEqual(ticket.status, MyTicket.NEW)
		self.assertEqual(ticket.get_status_display(), 'New')

	def test_ticket_status_is_one_of_allowed_values(self):
		valid_statuses = {choice[0] for choice in MyTicket.STATUS_CHOICES}
		ticket = MyTicket.objects.create(
			title='Allowed status',
			description='Verify status choices remain valid.',
			status=MyTicket.IN_PROGRESS,
			creator=self.user,
		)

		self.assertIn(ticket.status, valid_statuses)
		self.assertEqual(ticket.status, MyTicket.IN_PROGRESS)

	def test_migration_cleanup_normalizes_invalid_status(self):
		ticket = MyTicket.objects.create(
			title='Needs cleanup',
			description='Migration should normalize invalid status values.',
			status='X',
			creator=self.user,
		)

		fix_invalid_ticket_statuses(apps, None)
		ticket.refresh_from_db()

		self.assertEqual(ticket.status, MyTicket.NEW)
