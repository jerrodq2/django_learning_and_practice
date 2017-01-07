from django.shortcuts import render
from .models import Blog, Entry, Author,

# SEQUAL QUERIES

# CREATING
# b = Blog(name='Beatles Blog', tagline='All the latest...')
# b.save()

# SAVING CHANGES
# b5.name = 'New name'
# br.save()

# SAVING ForeignKey AND ManyToManyFields
# entry = Entry.objects.get(pk=1)
# cheese_blog = Blog.objects.get(name="Cheddar Talk")
# entry.blog = cheese_blog
# entry.save()

# UPDATING A ManyToManyField - use the add() method on the field to add a record to the relation. This example adds the Author instance joe to the entry object
# joe = Author.objects.create(name="Joe")
# entry.authors.add(joe)

# ADDING MUTLIPLE RECORDS TO A ManyToManyField AT ONE TIME
# john = Author.objects.create(name="John")
# paul = Author.objects.create(name="Paul")
# george = Author.objects.create(name="George")
# ringo = Author.objects.create(name="Ringo")
# entry.authors.add(john, paul, george, ringo)

# RETRIEVING OBJECTS
# b = Blog.objects(name='Foo', tagline='Bar')
# b.objects
# OR
# all_entries = Entry.objects.all()

# METHODS FOR FILTERING RESULTS:
# filter(**kwargs) - Returns a new QuerySet containing objects that match the given lookup parameters.
# exclude(**kwargs) - Returns a new QuerySet containing objects that do not match the given lookup parameters.
# EX:
# Entry.objects.filter(pub_date__year=2006)
# Entry.objects.all().filter(pub_date__year=2006)
# Entry.objects.exclude(pub_date__year==2006)

# CHAINING FILTERS
# >>> Entry.objects.filter(headline__startswith='What').exclude(pub_date__gte=datetime.date.today()).filter(pub_date__gte=datetime(2005, 1, 30))
# startswith, gte, and year (in pub_date__year) all appear to be methods, not part of the actual column

# END QUERIES
def index(request):

    return render(request, 'query_app/index.html')
