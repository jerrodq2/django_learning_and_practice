from django.shortcuts import render
from . import models
from django.db.models import Count, Sum
# Create your views here.
def index(req):
    cities = models.Countries.objects.aggregate(Sum('region'))
    # What query would you run to summarize the number of countries in each region? The query should display the name of the region and the number of countries. Also, the query should arrange the result by the number of countries in descending order






    # QUERIES BELOW numbered 1 - 8
    # 1. What query would you run to get all the countries that speak Slovene? Your query should return the name of the country, language and language percentage. Your query should arrange the result by language percentage in descending order.
    # cities = models.Countries.objects.values_list('name', 'languagetocountry__language', 'languagetocountry__percentage').filter(languagetocountry__language='slovene').order_by('-languagetocountry__percentage')
            # *********NOTE******** values_list returns something like a tuple (u'Croatia', u'Serbo-Croatian', 95.9), could not access the values in the html through city.name, inside the loop, had to put {{city.0}} to access the name of the first dictionary/tuple


    # 2.What query would you run to display the total number of cities for each country? Your query should return the name of the country and the total number of cities. You query should arrange the result by the number of cities in descending order
    # cities = models.Countries.objects.values('citytocountry', 'name').annotate(count=Count('citytocountry')).order_by('-citytocountry')


    # 3.What query would you run to get all the cities in Mexico with a population of greater than 500,000? Your query should arrange the result by population in descending order
    # cities = models.Cities.objects.filter(population__gt=500000).filter(country__name='Mexico').order_by('-population')

    # 4.What query would you run to get all languages in each country with a percentage greater than 89%? Your query should arrange the result by percentage in descending order
    # cities = models.Countries.objects.values('name', 'languagetocountry__language').filter(languagetocountry__percentage__gt=89).order_by('-languagetocountry__percentage')


    # 5. What query would you run to get all the countries with Surface Area below 501 and Population greater than 100,000?
    # cities = models.Countries.objects.filter(surface_area__lt=501).filter(population__gt=100000)


    # 6. What query would you run to get countries with only Constitutional Monarchy with a capital greater than 200 and a life expectancy greater than 75 years?
    # cities = models.Countries.objects.filter(capital__gt=200).filter(life_expectancy__gt=75).filter(government_form='Constitutional Monarchy')


    # 7. What query would you run to get all the cities of Argentina inside the Buenos Aires district and have the population greater than 500, 000? The query should return the Country Name, City Name, District and Population.
    # cities = models.Cities.objects.values('country__name', 'name', 'district', 'population' ).filter(country__name='Argentina').filter(population__gt=500000).filter(district='Buenos Aires')


    # 8. What query would you run to summarize the number of countries in each region? The query should display the name of the region and the number of countries. Also, the query should arrange the result by the number of countries in descending order

        # COULDN'T FIGURE 8 OUT





    # prints the queries
    print (50*"*")
    # print cities.query
    print (50*"*")
    return render(req, 'worldApp/index.html', context={'cities':cities})
