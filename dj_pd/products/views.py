from django.shortcuts import render
from .models import Product,Purchase
import pandas as pd
from .utils import get_simple_plot
from .forms import PurchaseForm
# Create your views here.
def chart_select_view(request):
     graph=None
     error_msg=None
     df=None#init
     price=None
     #qs=Product.objects.all()
     try:
         product_df = pd.DataFrame(Product.objects.all().values()) 
         purchase_df = pd.DataFrame(Purchase.objects.all().values())#.values_list()for indexs
         product_df['product_id']= product_df['id']
     except:
         product_df=None
         purchase_df=None
     if purchase_df:    
       if purchase_df.shape[0]>0 :
           df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)#manipulating dataframe
           price=df['price']
           print(df['date'][0])#date of the first object
           print(type(df['date'][0]))#date of the first object
           if request.method == 'POST':
              
               chart_type=request.POST.get('sales')
               date_from=request.POST.get('date_from')
               date_to=request.POST.get('date_to')
               #print(chart_type)
               df ['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
               df2 = df.groupby( 'date', as_index=False)['total_price'].agg('sum')
              # print(df2['date'])
               if chart_type !="":
                     if date_from !="" and date_to != "":
                         df = df[(df['date']>date_from) & (df['date']< date_to)]
                         #print(type(df))
                         df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                            # function to get a graph
                     graph=get_simple_plot(chart_type,x=df2['date'],y=df2['total_price'],data=df)
               else:
                    error_msg = 'Please select a chart type to continue'
     else:
                error_msg='No records in the database'
               

               
     context={
          
         #'products':product_df.to_html(),
         #'purchase':purchase_df.to_html(),
      #   'df':df.to_html(),
         'price':price,
         'graph':graph,
         'error_msg':error_msg, 
         #'df':df,
    }
     return render(request, 'products/main.html',context)



def add_purchase_view(request):
   
   form=PurchaseForm(request.POST or None)
   added_msg=None
   if form.is_valid():
      obj=form.save(commit=False)
      obj.salesman=request.user
      obj.save()
      form=PurchaseForm()
      added_msg="the purchase has been added"
   context={'form':form,'added_msg':added_msg}
   return render(request,'products/add.html',context)
