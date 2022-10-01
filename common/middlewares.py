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

from investments_appraisal.models import UserProfile

#Session model stores the session data
from django.contrib.sessions.models import Session
from common.models import LoggedInUser


import threading

request_local = threading.local()

def get_request():
    return getattr(request_local, 'request', None)
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

""" 
class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            session_key = request.session.session_key

            try:
                logged_in_user = request.user.logged_in_user
                stored_session_key = logged_in_user.session_key
                # stored_session_key exists so delete it if it's different
                if stored_session_key and stored_session_key != request.session.session_key:
                    Session.objects.get(session_key=stored_session_key).delete()
                request.user.logged_in_user.session_key = request.session.session_key
                request.user.logged_in_user.save()
            except LoggedInUser.DoesNotExist:
                LoggedInUser.objects.create(user=request.user, session_key=session_key)
            stored_session_key = request.user.logged_in_user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                Session.objects.get(session_key=stored_session_key).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response
 """
#Session model stores the session data
from django.contrib.sessions.models import Session

class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                try:
                    Session.objects.get(session_key=stored_session_key).delete()
                except:
                    pass

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response