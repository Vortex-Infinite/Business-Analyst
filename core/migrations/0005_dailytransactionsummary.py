from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_core_onetime_user_0a9c8d_idx_core_onetim_user_id_90d06c_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTransactionSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('total_transactions', models.IntegerField(default=0)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('anomaly_count', models.IntegerField(default=0)),
                ('high_risk_anomalies', models.IntegerField(default=0)),
                ('avg_transaction_value', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['date'], name='core_daily_date_2a1b9c_idx')],
            },
        ),
    ]
