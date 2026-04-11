from django.db import migrations, models


def fix_invalid_ticket_statuses(apps, schema_editor):
    MyTicket = apps.get_model('tickets', 'MyTicket')
    valid_statuses = {'N', 'P', 'D', 'I'}

    # Previous default stored invalid values in max_length=1 field.
    # Normalize anything outside the allowed choices to New.
    for ticket in MyTicket.objects.all().only('id', 'status'):
        if ticket.status not in valid_statuses:
            ticket.status = 'N'
            ticket.save(update_fields=['status'])


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myticket',
            name='status',
            field=models.CharField(
                choices=[('N', 'New'), ('P', 'In Progress'), ('D', 'Done'), ('I', 'Invalid')],
                default='N',
                max_length=1,
            ),
        ),
        migrations.RunPython(fix_invalid_ticket_statuses, migrations.RunPython.noop),
    ]
