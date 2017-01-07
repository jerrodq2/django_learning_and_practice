from __future__ import unicode_literals

from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=35)
    country_code = models.CharField(max_length=3)
    district = models.CharField(max_length=20)
    population = models.IntegerField()
    country = models.ForeignKey('Countries', related_name="citytocountry")

    class Meta:
        managed = False
        db_table = 'cities'


class Countries(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=52)
    continent = models.CharField(max_length=13)
    region = models.CharField(max_length=26)
    surface_area = models.FloatField()
    indep_year = models.SmallIntegerField(blank=True, null=True)
    population = models.IntegerField()
    life_expectancy = models.FloatField(blank=True, null=True)
    gnp = models.FloatField(blank=True, null=True)
    gnp_old = models.FloatField(blank=True, null=True)
    local_name = models.CharField(max_length=45)
    government_form = models.CharField(max_length=45)
    head_of_state = models.CharField(max_length=60, blank=True, null=True)
    capital = models.IntegerField(blank=True, null=True)
    code2 = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'countries'


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


class Languages(models.Model):
    country_code = models.CharField(max_length=3)
    language = models.CharField(max_length=30)
    is_official = models.CharField(max_length=1)
    percentage = models.FloatField()
    country = models.ForeignKey(Countries, related_name="languagetocountry")

    class Meta:
        managed = False
        db_table = 'languages'
