from django.shortcuts import render, redirect

from record_management_app.forms import RecordForm  
from record_management_app.models import Record  

# Create your views here.

from django.http import JsonResponse
from django.core.serializers import serialize

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RecordForm
from .models import Record

from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import get_object_or_404


def index(request):
    employees = Record.objects.all()

    # Check if the request is made by Postman or similar API testing tool
    if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
        # If the request is from Postman, return JSON response
        serialized_data = serialize('json', employees)
        return JsonResponse(serialized_data, safe=False)
    else:
        # If it's a standard web browser request, return HTML response
        return render(request, "show.html", {'employees': employees})


@csrf_exempt
def addnew(request):
    if request.method == "POST":
        # Check if the request is made by Postman or similar API testing tool
        if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
            try:
                # Decode the request body and load JSON data
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError as e:
                # Handle JSON decoding error
                return JsonResponse({'error': 'Invalid JSON data: {}'.format(str(e))}, status=400)
            form = RecordForm(data)
        else:
            form = RecordForm(request.POST)
            
        if form.is_valid():
            form.save()
            # If the request is from Postman, return JSON response
            if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
                return JsonResponse({'message': 'Data saved successfully'}, status=201)
            else:
                # If it's a standard web form submission, redirect to homepage
                return redirect('/')
        else:
            # Handle invalid form data
            if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                # If it's a standard web form submission, render form with errors
                return render(request, "index.html", {'form': form})
    else:
        form = RecordForm()
        return render(request, "index.html", {'form': form})

    
def edit(request, id):  
    employee = Record.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  


@csrf_exempt
def update(request, id):
    # Retrieve the employee record to update
    employee = get_object_or_404(Record, id=id)
    
    if request.method == "POST":
        # Check if the request is made by Postman or similar API testing tool
        if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
            try:
                # Decode the request body and load JSON data
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError as e:
                # Handle JSON decoding error
                return JsonResponse({'error': 'Invalid JSON data: {}'.format(str(e))}, status=400)
            form = RecordForm(data, instance=employee)
        else:
            form = RecordForm(request.POST, instance=employee)
            
        if form.is_valid():
            form.save()
            # If the request is from Postman, return JSON response
            if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
                return JsonResponse({'message': 'Data updated successfully'}, status=200)
            else:
                # If it's a standard web form submission, redirect to homepage
                return redirect('/')
        else:
            # Handle invalid form data
            if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                # If it's a standard web form submission, render form with errors
                return render(request, 'edit.html', {'employee': employee, 'form': form})
    else:
        # If it's not a POST request, render the form with the employee data
        form = RecordForm(instance=employee)
        return render(request, 'edit.html', {'employee': employee, 'form': form})

@csrf_exempt
def destroy(request, id):
    # Retrieve the employee record to delete
    employee = get_object_or_404(Record, id=id)
    
    if request.method == "GET":
        # Check if the request is made by Postman or similar API testing tool
        if 'HTTP_USER_AGENT' in request.META and 'Postman' in request.META['HTTP_USER_AGENT']:
            # Delete the record
            employee.delete()
            return JsonResponse({'message': 'Data deleted successfully'}, status=200)
        else:
            # If it's a standard web form submission, redirect to homepage
            employee.delete()
            return redirect('/')
    elif request.method == "DELETE":
        # Check if the request is made using the DELETE method
        # Delete the record
        employee.delete()
        return JsonResponse({'message': 'Data deleted successfully'}, status=200)
    else:
        # If it's not a supported method, return a JSON response with an error message
        return JsonResponse({'error': 'Method not allowed'}, status=405)
