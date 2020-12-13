# Generated by Django 3.1.4 on 2020-12-13 15:03

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True)),
                ('contact_number', models.CharField(blank=True, db_index=True, max_length=16, null=True, validators=[user.models.User.validate_contact_number])),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('mobile_otp', models.IntegerField(blank=True, null=True)),
                ('mobile_otp_validity', models.DateTimeField(blank=True, null=True)),
                ('email_otp', models.IntegerField(blank=True, null=True)),
                ('email_otp_validity', models.DateTimeField(blank=True, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('contact_number_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars')),
                ('groups', models.ManyToManyField(blank=True, null=True, to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
