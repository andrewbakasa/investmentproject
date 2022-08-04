from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
import os
import numpy as np
from datetime import datetime, date
import pandas as pd
from dateutil.relativedelta import relativedelta
import decimal
import pandas as pd
import functools
from django.http import HttpResponseRedirect
import math


from django.db.models.expressions import Func, Value
from django.db.models.query_utils import Q
from django.shortcuts import render

from trading.models import Investor

def updateInvestorApplicationState(request):

    #get_user_authorisation(request)   
    boole_admin = True if request.user.is_superuser  else False

    if boole_admin:
        qs = Investor.objects.filter(application_status='recieved')
         
    #approve all released
    qs.update(application_status ='verification') 