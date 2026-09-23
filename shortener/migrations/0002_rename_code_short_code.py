from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shorturl',
            old_name='code',
            new_name='short_code',
        ),
    ]
