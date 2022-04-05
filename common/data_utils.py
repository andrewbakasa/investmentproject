from investments_appraisal.models import Downloads, ModelCategory
from django.db.models.expressions import F

def create_downloads_instance(request, uniqueid):
    model_cat= ModelCategory.objects.filter(uniqueid=uniqueid).first()
    if model_cat:
        Downloads.objects.create(user=request.user, model_type=model_cat)

        ModelCategory.objects.filter(uniqueid=uniqueid).update(hits=F('hits') + 1)
    else:
        Downloads.objects.create(user=request.user)
       

    
