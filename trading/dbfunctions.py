from strategicplan.models import *
from datetime import date, timedelta
from django.db.models import DateTimeField
from django.db.models.functions import Cast, Coalesce
from django.utils import timezone
from django.db.models import Q ,Case, CharField, Value, When, Avg, Count, Min, Sum, Max,Value as V
from dateutil.relativedelta import relativedelta
import datetime
from operations.models import Production
from silverstrike.lib import  short_month_name
from trading.models import Investment

# total 
def total():
    SalesPlan.objects.aggregate(
        approved=Count('pk', filter=Q(status=status.approved)),
        draft=Count('pk', filter=Q(status=status.draft)),
        wip=Count('pk', filter=Q(status=status.wip)),
        )
#{'approved': 2, 'draft': 1, 'wip': 3}

''' 
Conditional update
Let’s say we want to change the account_type for our clients to match their registration dates. We can do this
using a conditional expression and the update() method: 
'''
def export_monthly_production(request):
	start_list, end_list = get_last_n_months_periods(12)# a year (dynamic length)

	response = HttpResponse(content_type='text/csv')

	date_now = datetime.datetime.now() #date.today()
	date_now = str(date_now.year) + '_' + str(date_now.month) \
				+ '_' + str(date_now.day)+ "_" + str(date_now.hour) \
				+ '_' + str(date_now.minute) + "_" +  str(date_now.second)

	filename = "Production" + date_now +  ".csv"
	response['Content-Disposition'] = 'attachment; filename=' + filename
	writer = csv.writer(response, delimiter=',')
	# Writing the first row of the csv
	heading_text = "Production Report For NRZ Company" 
	writer.writerow([heading_text.upper()])	

	#----initialise counter
	c = 0


	#---get user company list
	item_sbu= get_login_user_companies_as_list(request.user)
	for company in Company.objects.filter(pk__in =item_sbu):# Loop SBU {s:0, t, p}
		
		# Writing the first row of the csv
		heading_text = company.name
		
		writer.writerow([heading_text.upper()])	
		#--Headings---
		
		writer.writerow([str(item) for item in end_list.keys()])
        
		#for each company keep time series of products and total
		product_array={}
		
		#-----initialise counter
		t = 0
		for key in start_list:# Loop time series {c, t:0, p}
			products_in_period_month = production_report_period_company(start_list[key], end_list[key],company)
			
			# ----initialize counter
			p = 0					
			for product_item in products_in_period_month:# Loop Products {c, t, p:0}
				#.append qnty in appropriate product_id list
				if product_item.name in product_array.keys():
    				#-insert at appropriate point in timeseries
					#----0, 0, 0, invisible  and visible at time (t)
					while len(product_array[product_item.name]) < t+1:
						product_array[product_item.name].append(0)	
							
					product_array[product_item.name].append(product_item.prod_out)
				else:
					product_array[product_item.name] = []# initilise
					# empty spaces until this time
					product_array[product_item.name].append(product_item.name)				
					while len(product_array[product_item.name]) < t+1:
						product_array[product_item.name].append(0)	
					product_array[product_item.name].append(product_item.prod_out)# add first item	

				
				prod = product_item.name
				price = product_item.price
				out  = product_item.prod_out 
				totat_price= decimal.Decimal(out) * price
				#------ increment counter---------		
				p +=1
			#------ increment counter---------		
			
			
		
			t +=1
      
		#print(product_array)
		

		#Write each one per company
		for key_key in product_array.keys():
    		# each product per line
			writer.writerow([str(item) for item in product_array[key_key]])

		#------ increment counter---------		
		c +=1
	# Return the response
	return response

def update(period):
    a_month_ago = date.today() - timedelta(days=30)
    a_year_ago = date.today() - timedelta(days=365)
    # Update the account_type for each Client from the registration date
    SalesPlan.objects.update(
        valid_type=Case(
            When(dend__lte=a_year_ago,
            then=Value(valid_type.PLATINUM)),
            When(dent__lte=a_month_ago,
            then=Value(valid_type.GOLD)),
            default=Value(valid_type.REGULAR)
        ),
    )
#  Client.objects.values_list('name', 'account_type')
# <QuerySet [('Jane Doe', 'G'), ('James Smith', 'R'), ('Jack Black', 'P')]>


''' A Case() expression is like the if . . . elif . . . else statement in Python. Each condition in the provided
When() objects is evaluated in order, until one evaluates to a truthful value. The result expression from the
matc hing When() object is returned.
 Case() accepts any number of When() objects as individual arguments. Other options are provided using keyword arguments. If none of the conditions evaluate to TRUE, then the expression given with the default keyword
argument is returned. If a default argument isn’t provided, None is used. '''

# def 
# # Get the discount for each Client based on the account type
#  Client.objects.annotate(
#     discount=Case(
#     When(account_type=Client.GOLD, then=Value('5%')),
#     When(account_type=Client.PLATINUM, then=Value('10%')),
#     default=Value('0%'),
#     output_field=CharField(),
#     ),
#  ).values_list('name', 'discount')
# <QuerySet [('Jane Doe', '0%'), ('James Smith', '5%'), ('Jack Black', '10%')]>


''' Coalesce
class Coalesce(*expressions, **extra)
Accepts a list of at least two field names or expressions and returns the first non-null value (note that an empty string
is not considered a null value). Each argument must be of a similar type, so mixing text and numbers will result in a
database error. '''

 # Prevent an aggregate Sum() from returning None
# aggregated = Author.objects.aggregate(
#     combined_age=Coalesce(Sum('age'), V(0)),
#     combined_age_default=Sum('age'))
# print(aggregated['combined_age'])
# 0
# print(aggregated['combined_age_default'])
# None

# now = timezone.now()
# Coalesce('updated', Cast(now, DateTimeField()))

# total 
def total_2():
    '''    
    Get counts for each value of account_type 
    Conditional aggregation
    What if we want to find out how many clients there are for each account_type? We can use the filter argument
    of aggregate functions to achieve this: 
    '''  
    SalesPlan.objects.aggregate(
        approved=Sum('pk', filter=Q(status=status.approved)),
        draft=Sum('pk', filter=Q(status=status.draft)),
        wip=Sum('pk', filter=Q(status=status.wip)),
        )
#{'approved': 2, 'draft': 1, 'wip': 3}
# Publisher.objects.aggregate(oldest_pubdate=Min('book__pubdate'))
# Apply to foreign keys and many-to-many relations.
# Author.objects.aggregate(average_rating=Avg('book__rating'))
# Author.objects.annotate(total_pages=Sum('book__pages'))

''' Aggregations and other QuerySet clauses
filter() and exclude()
Aggregates can also participate in filters. Any filter() (or exclude()) applied to normal model fields will have
the effect of constraining the objects that are considered for aggregation.
When used with an annotate() clause, a filter has the effect of constraining the objects for which an annotation is
calculated. For example, you can generate an annotated list of all books that have a title starting with “Django” using
the query '''

# Book.objects.filter(name__startswith="Django").annotate(num_authors=Count('authors'))


''' Filtering on annotations
Annotated values can also be filtered. The alias for the annotation can be used in filter() and exclude() clauses
in the same way as any other model field.
For example, to generate a list of books that have more than one author, you can issue the query: '''

# Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)


''' This query generates an annotated result set, and then generates a filter based upon that annotation.
If you need two annotations with two separate filters you can use the filter argument with any aggregate. For
example, to generate a list of authors with a count of highly rated books: '''

# highly_rated = Count('books', filter=Q(books__rating__gte=7))
# Author.objects.annotate(num_books=Count('books'), highly_rated_books=highly_rated)

# Each Author in the result set will have the num_books and highly_rated_books attributes.



''' 
Unlike aggregate(), annotate() is not a terminal clause. The output of the annotate() clause is
a QuerySet; this QuerySet can be modified using any other QuerySet operation, including filter(),
order_by(), or even additional calls to annotate(). 

If you need two annotations with two separate filters you can use the filter argument with any aggregate. For
example, to generate a list of authors with a count of highly rated books:
'''

def get_month_and_year(date_instance):
    return str(short_month_name(date_instance.month)) + " " + str(date_instance.year)

#dynamic period
def get_last_n_months_periods(number):
    start_list={}#'7:2022':01/01/2022
    end_list={}#   7:2022" 31/07/2022
    end_list['Product'] = "This is product Heading" 
    #Loop backward (number of time including current month)
    for i in range (number +1):
        date1 = get_day_from_today(number-i,1,False)
        start_list[get_month_and_year(date1)] = date1

        date2 = last_day_of_month(date1)
        end_list[get_month_and_year(date2)] = date2
    return start_list,end_list


def production_report_current_6_months():
    p1_start = date.today().replace(day=1)# First day
    p1_end = last_day_of_month(date.today())#Las day
    p2_start = get_day_from_today(1,1,False)# back_wards
    p2_end = last_day_of_month(p2_start)
    p3_start = get_day_from_today(1,2,False)# back_wards
    p3_end = last_day_of_month(p3_start)
    p4_start = get_day_from_today(1,3,False)# back_wards
    p4_end = last_day_of_month(p4_start)
    p5_start = get_day_from_today(1,4,False)# back_wards
    p5_end = last_day_of_month(p5_start)
    p6_start = get_day_from_today(1,5,False)# back_wards
    p6_end = last_day_of_month(p6_start)

    #for each product, for each period for each company
    prod = Investment.objects.annotate(
            p1=Coalesce(Sum('production__qnty', filter=Q(date_gte=p1_start, date_lte=p1_end)), V(0)),
            p2=Coalesce(Sum('production__qnty', filter=Q(date_gte=p2_start, date_lte=p2_end)), V(0)),
            p3=Coalesce(Sum('production__qnty', filter=Q(date_gte=p3_start, date_lte=p3_end)), V(0)),
            p4=Coalesce(Sum('production__qnty', filter=Q(date_gte=p4_start, date_lte=p4_end)), V(0)),
            p5=Coalesce(Sum('production__qnty', filter=Q(date_gte=p5_start, date_lte=p5_end)), V(0)),
            p6=Coalesce(Sum('production__qnty', filter=Q(date_gte=p6_start, date_lte=p6_end)), V(0)),
            )

            # prod['pi']
            # prod['pi']
    return prod

def production_report_current_6_months_company(company_a):
    p1_start = date.today().replace(day=1)# First day
    p1_end = last_day_of_month(date.today())#Las day
    p2_start = get_day_from_today(1,1,False)# back_wards
    p2_end = last_day_of_month(p2_start)
    p3_start = get_day_from_today(1,2,False)# back_wards
    p3_end = last_day_of_month(p3_start)
    p4_start = get_day_from_today(1,3,False)# back_wards
    p4_end = last_day_of_month(p4_start)
    p5_start = get_day_from_today(1,4,False)# back_wards
    p5_end = last_day_of_month(p5_start)
    p6_start = get_day_from_today(1,5,False)# back_wards
    p6_end = last_day_of_month(p6_start)

    #for each product, for each period for each company
    prod = Product.objects.filter('production__company' ==company_a).annotate(
            p1=Coalesce(Sum('production__qnty', filter=Q(date_gte=p1_start, date_lte=p1_end)), V(0)),
            p2=Coalesce(Sum('production__qnty', filter=Q(date_gte=p2_start, date_lte=p2_end)), V(0)),
            p3=Coalesce(Sum('production__qnty', filter=Q(date_gte=p3_start, date_lte=p3_end)), V(0)),
            p4=Coalesce(Sum('production__qnty', filter=Q(date_gte=p4_start, date_lte=p4_end)), V(0)),
            p5=Coalesce(Sum('production__qnty', filter=Q(date_gte=p5_start, date_lte=p5_end)), V(0)),
            p6=Coalesce(Sum('production__qnty', filter=Q(date_gte=p6_start, date_lte=p6_end)), V(0)),
            )

            # prod['pi']
            # prod['pi']
    return prod


def production_report_period(p_start,p_end):
    # prodcts with prodcution per given period
    prod = Investment.objects.annotate(
                        prod_out=Coalesce
                           (
                                Sum
                                    (
                                        'production__qnty', 
                                        filter=Q(date_gte=p_start, 
                                                 date_lte=p_end
                                                )
                                    ), 
                                    V(0)
                            ) 
                        ).filter(prod_out_gte=1)
    return prod
 
def production_report_period_company(p_start,p_end, company_a):
    print("start: " + str(p_start) +  " end: " + str(p_end) + " company: " + str(company_a) )
    # # prodcts with prodcution per given period
    prod = Investment.objects.filter(company = company_a).annotate(
            prod_out=Coalesce
                (
                    Sum
                        (
                            'production__qnty', 
                            filter=Q(production__date__gte=p_start, 
                                    production__date__lte=p_end, 
                                    production__producer = company_a,
                                    ) #Many to many_field: only products belong to this company
                        ), 
                    V(0)
                )
            ).filter(prod_out__gte=1)
    return prod
 
def production_report_period(p_start,p_end):  
        # prodcts with prodcution per given period
    prod = Investment.objects.annotate(
            prod_out=Coalesce(
                Sum('production__qnty', 
                filter=Q(date_gte=p_start, date_lte=p_end)), V(0)
                )
            ).filter(prod_out_gte=1).aggregate(
                average_prod = Avg('prod_out'),
                min_prod = Min('prod_out'),
                max_prod = Max('prod_out'),
                )
    return prod

 
def get_day_from_today(months_added, day_month, add):
    if add==True:
        date_output = (date.today() + relativedelta(months=months_added)).replace(day=day_month)
    else:
        date_output = (date.today() - relativedelta(months=months_added)).replace(day=day_month)

    return date_output


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)



''' Following relationships backwards
In a way similar to Lookups that span relationships, aggregations and annotations on fields of models or models that
are related to the one you are querying can include traversing “reverse” relationships. The lowercase name of related
models and double-underscores are used here too.
For example, we can ask for all publishers, annotated with their respective total book stock counters (note how we use
'book' to specify the Publisher -> Book reverse foreign key hop '''

# Publisher.objects.annotate(Count('book'))
# # (Every Publisher in the resulting QuerySet will have an extra attribute called book__count.)

# Company.objects.annotate(num_of_prod=Count('product'))

# Every company product count



#In Django 3.2, the framework automatically follows relationships when using method QuerySet.filter()

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
""" Choice.objects.filter(question__pub_date__year=current_year) """
# This compiles to the following SQL query:

# SELECT
#     "polls_choice"."id",
#     "polls_choice"."question_id",
#     "polls_choice"."choice_text",
#     "polls_choice"."votes"
# FROM
#     "polls_choice"
# INNER JOIN "polls_question" ON
#     ("polls_choice"."question_id" = "polls_question"."id")
# WHERE
#     "polls_question"."pub_date" BETWEEN 2020-12-31 23:00:00 AND 2021-12-31 22:59:59.999999

""" 
Player.objects.filter(name="Bob").prefetch_related(
        'position__positionstats_set', 'playerstats_set') """
# Share
# Follow
# answered Oct 27 '12 at 1:25

# dokkaebi
# 8,32433 gold badges3838 silver badges5858 bronze badges
# Add a comment

# 11

# select_related() and prefetch_related() is your solution. They work almost same way but has some difference.

# select_related() works by creating an SQL join and including the fields of the related object in the SELECT statement. For this reason, select_related gets the related objects in the same database query. But it only works for one-to-one or one-to-many relation. Example is below-

""" entry = Entry.objects.select_related('blog').get(id=5) """
# or
""" entries = Entry.objects.filter(foo='bar').select_related('blog') """
# prefetch_related(), on the other hand, does a separate lookup for each relationship and does the ‘joining’ in Python. This allows it to prefetch many-to-many and many-to-one objects, which cannot be done using select_related. So prefetch_related will execute only one query for each relation. Example is given below-

""" Pizza.objects.all().prefetch_related('toppings') """

""" b = Book.objects.select_related('author__hometown').get(id=4)
p = b.author # Doesn't hit the database.
c = p.hometown # Doesn't hit the database.
# Without select_related()...
b = Book.objects.get(id=4) # Hits the database.
p = b.author # Hits the database.
c = p.hometown # Hits the database. """