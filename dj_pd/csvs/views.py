from os import read
from django.shortcuts import render
from numpy import product
from .forms import CsvForm
from .models import Csv
import csv
from django.contrib.auth.models import User
from products.models import Product,Purchase
# Create your views here.

def upload_file_view( request):
     form = CsvForm( request.POST or None, request.FILES or None)
     if form.is_valid():
          form.save()
          form = CsvForm()
          obj=Csv.objects.get(activated=False)#process it 
          obj.activated=True#change it 
          obj.save()
          with open(obj.file_name.path,'r')as f:
               reader=csv.reader(f)
               for row in reader:
                    #print(row)
                    #row="".join(row)
                    #print(row)
                    #row=row.replace(",","")    
                    print(row)
                    #row=row.split()
                    print(type(row))
                   # user=User.objects.get(id=row[3])
                  #  Prod,_=Product.object.get_or_create(name=row[0])
                    
                   # print(user)
         
     context={
          'form': form,}
     return render(request, 'csvs/upload.html', context)    
    