from recordkeeper.models import Person, PersonStatus, FormulaFields
from .serializers import PersonSerializer, PersonStatusSerializer, FormulaFieldsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.utils import timezone
import string, secrets, time
from django.db.models import Subquery, F, OuterRef
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def my_timer(prefix):
    def get_time(original_func):
        def wrapper_func(*args, **kwargs):
            t1 = time.time()
            result = original_func(*args, **kwargs)
            t2 = time.time() - t1
            print (prefix, '{} function ran in {}'.format(original_func.__name__, t2))
            return result
        return wrapper_func
    return get_time

@my_timer('Total Time Taken:')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def get_records(request):
    page = request.GET.get('page', 1)
    data_count_per_page = 20
    full_name = str(request.GET.get('full_name', ''))
    status = str(request.GET.get('status', ''))
    personstatus_qs = PersonStatus.objects.filter(
        person=OuterRef('pk'))
    person_dataset = Person.objects.values().annotate(
        status=Subquery(personstatus_qs.values('status_text')),
        person_id=Subquery(personstatus_qs.values('person')))
    for data in person_dataset:
        data.update({'full_name': "%s %s" % (data.get('first_name', ''), data.get('last_name', ''))})
        age_calc_str = "(int(time.time()) - %s) / (3600 * 24 * 365)" % data.get('date_of_birth', 0)
        age = eval(age_calc_str)
        if age >= 18:
            data.update({'is_adult': 'Yes'})
        else:
            data.update({'is_adult': 'No'})
    if full_name:
        person_dataset = list(filter(lambda x: full_name.lower() in x.get('full_name').lower(), person_dataset))
    if status:
        person_dataset = list(filter(lambda x: status.lower() in x.get('status').lower(), person_dataset))
    
    paginator = Paginator(person_dataset, 20)
    try:
        person_dataset = paginator.page(page)
    except PageNotAnInteger:
        person_dataset = paginator.page(1)
    except EmptyPage:
        person_dataset = paginator.page(paginator.num_pages)
    final_dict = {'person_record': person_dataset}
    return Response({'final_dict': final_dict, 'full_name': full_name, 'status': status, 'person_dataset': person_dataset, 'data_count_per_page': data_count_per_page}, template_name='record-list-template.html')

@my_timer('Total Time Taken:')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def dump_data_to_database(request):
    entries = int(request.GET.get('entries', 0))
    if entries:
        for i in range(entries):
            person_obj = Person()
            person_obj.created_at = timezone.now()
            person_obj.first_name = (''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(7)).capitalize())
            person_obj.last_name = (''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(9)).capitalize())
            if i % 5 == 0:
                person_obj.date_of_birth = time.time() - (86400 * 365 * 16)
            else:
                person_obj.date_of_birth = time.time() - (86400 * 365 * 20)
            if i % 2 == 0:
                person_obj.gender = 'Male'
            else:
                person_obj.gender = 'Female'
            person_obj.save()
            if i % 5 == 0:
                person_status_obj = PersonStatus(person=Person.objects.get(id=person_obj.id), status_text='Unmarried', created_at=timezone.now())
                person_status_obj.save()
            else:
                person_status_obj = PersonStatus(person=Person.objects.get(id=person_obj.id), status_text='Married', created_at=timezone.now())
                person_status_obj.save()
        formula_fd_obj = FormulaFields(formula='%s %s', column_number=5)
        formula_fd_obj.save()
        formula_fd_obj = FormulaFields(formula='(int(time.time()) - %s) / (3600 * 24 * 365)', column_number=6)
        formula_fd_obj.save()
        return Response({'msg': 'Table insertion is completed.'}, template_name='dump-data-to-db-template.html')
    else:
        return Response({'msg': 'Some value is required!'}, template_name='dump-data-to-db-template.html')
