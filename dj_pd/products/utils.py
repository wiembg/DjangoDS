#keep external
import base64
from re import X
from tkinter import Y
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
def get_image():
    #create a buytes buffer for the image to save
    buffer=BytesIO()
    #create the plot with the use of BytesI0 object as its 'file
    plt.savefig(buffer,format='png')
    #pass
    buffer.seek(0)
    # retreive the entire content of the 'file'
    img=buffer.getvalue()
    graph=base64.b64encode(img)
    graph=graph.decode('utf-8')
    #free to memory of the buffer
    buffer.close()
    return graph
def get_simple_plot(chart_type, *args, **kwargs):
    #https://matplotlib.org/faq/usage_faq.html?highlight=backend#wl
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    x=kwargs.get('x')
    y=kwargs.get('y')                                                     
    data=kwargs.get('data') 
    #df=kwargs.get('df') 
    if chart_type =='bar plot':
        title="total price by day"
        plt.title(title)
        plt.bar(x,y)
    elif chart_type=='line plot':
        title="total price by day"
        plt.title(title)
        plt.bar(x,y)
    else:
        title="Product count"
        plt.title(title)
        sns.countplot('name',data=data)
    plt.xticks(rotation=45)
    plt.tight_layout()#fitter

    graph=get_image()
    return graph