""" 
Here's a middleware that will keep track of user last activity and
count separated by intervals of time. Using the interval creates discrete
"sessions" which can be tracked/counted along with the benefit of minimizing 
writes to the database.

Every time an auth user performs a request, will hit the cache to find their 
last activity, and then update the cache with a new timestamp. If the activity 
has had a gap of at least "interval" time, then it will update the database timestamp.
 """

from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from django.db.models.expressions import F
from dateutil.parser import parse

from .models import UserProfile


class LastUserActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last-activity')

            too_old_time = timezone.now() - td(seconds=settings.LAST_ACTIVITY_INTERVAL_SECS)
            #print('Time Delta >>>>>', too_old_time, parse(last_activity) < too_old_time, parse(last_activity)- too_old_time )
            if not last_activity or parse(last_activity) < too_old_time:
                user_obj= UserProfile.objects.filter(user=request.user)
                if user_obj:
                    user_obj.update(last_login=timezone.now(),   login_count=F('login_count') + 1)
                else:
                    #create
                    UserProfile.objects.create(user=request.user, last_login=timezone.now(),   login_count=1 )

                request.session['last-activity'] = timezone.now().isoformat()

        response = self.get_response(request)

        return response