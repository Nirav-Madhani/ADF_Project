from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm,NewUserForm
from django.contrib import messages
import requests
import json
from .api import *
from datetime import datetime
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from finance.settings import STOCKS_API_KEY,STOCKS_API_URL
import requests
import json
from django.contrib.auth.decorators import login_required

def home(request):
    import requests
    import json
    if request.method == 'GET':
        ticker = request.GET['ticker']
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + ticker + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
    
        # for error handling
        try:
            api = json.loads(api_request.content)
        #create an exception
        except Exception as e:
            api = "Sorry there is an error"
        return render(request, 'home.html', {'api': api} )
    else:
        return render(request, 'home.html', {'ticker': "Enter Ticker Symbol"} )

@csrf_exempt
def view_stock(request):
    usr_msg = dict(success=False,
                   message='Send something from view')
    if request.method == 'POST':
        ajax_data = request.body.decode('utf-8')
        company = ajax_data.split('=')[1]
        print("ajax_data", ajax_data.split('=')[1])
        response = requests.get(STOCKS_API_URL+company+'.csv?api_key='+STOCKS_API_KEY)
        result = response.content #.decode('utf-8')
       
        with open('quotes/static/csvfile.csv','wb') as file:
            file.write(result)
        user_msg = dict(success = True, message=ajax_data)

        return JsonResponse(user_msg)
      
        
    if request.method == 'GET':
        response = requests.get(STOCKS_API_URL+'AAPL.csv?api_key='+STOCKS_API_KEY)
        result = response.content #.decode('utf-8')
        with open('quotes/static/csvfile.csv','wb') as file:
            file.write(result)
                # file.write('\n')

        return render(request,'stocks.html',{'stock_data' : result})
    return JsonResponse(usr_msg)

def register_request(request):
    if (request.method == "POST"):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def about(request):
    return render(request, 'about.html', {})

class ProfileView(LoginRequiredMixin ,TemplateView):
    template_name = 'profile.html'
@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, ("Stock ticker has been added to your Portfolio!"))
            return redirect('add_stock')
    else:

        if request.user.is_anonymous:
            ticker = []
        else:
            ticker = Stock.objects.filter(user=request.user)
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
            
            # for error handling
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Sorry there is an error"
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})
    
def list_stock_old(request):
    output = []
    if request.user.is_anonymous:
        tickerList = ''
    else:
        ticker = Stock.objects.filter(user=request.user)        
        tickerList = " ".join([t.ticker for t in ticker])
    print(tickerList)
    tickerData = GetAllStocks(tickerList)
    #tickerData = tickerData.summary_detail.update(tickerData.price)
    #print(tickerData.summary_detail)
    return render(request, 'stockList.html', {'ticker':tickerData.summary_detail|tickerData.price, 'output':output})
@login_required
def list_stock(request):
    if request.user.is_anonymous:
        ticker = []
    else:
        ticker = Stock.objects.filter(user=request.user)
    output = []
    for ticker_item in ticker:
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
        
        # for error handling
        try:
            api = json.loads(api_request.content)
            output.append(api)
        except Exception as e:
            api = "Sorry there is an error"
    return render(request, 'stockList.html', {'ticker': ticker, 'output': output})
@login_required
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock ticker has been removed from your Portfolio!"))
    return redirect(list_stock)


def delete_stock(request):    
    ticker = Stock.objects.filter(user=request.user)
    return render(request, 'delete_stock.html', {'ticker': ticker})

def searchView(request):
    if len (request.GET['ticker']) < 1:
        return HttpResponse("")
    data = get_symbol_list(request.GET['ticker'])
    print(data)
    return render(request,'search.html',{'data':data})
