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

# Create your views here.
def home(request):
    ##Detail View For Each Ticker
    if  request.method == 'GET' and 'ticker' in request.GET:
        ticker = request.GET['ticker']
        print(ticker)
        # pk_56e9488bfddc4f64805631337556e19e    
        try:
             tickerData = GetSingleStock(ticker)     
             print(type(tickerData.history(period='1d', interval='1m')  ))
        except Exception as e:
            api = "Error..."
        #print(tickerData.price)
        
        df = tickerData.history(period='1d', interval='1m')
        
        print(df.to_csv())
        return render(request, 'home.html', {'api':tickerData.summary_detail[ticker],'price':tickerData.price,'chart':
        df.to_csv()})# to_json for charts
        #'chart':str(tickerData.history(start=datetime.now().strftime(r'%Y-%m-%d') ,interval='1m')[ticker]['indicators']['quote'])})
    else:
        return render(request, 'home.html', {'ticker':"Enter a Ticker Symbol Above..."})

    # return render(request, 'home.html', {'api':api}). Here, {'api':api} context dictionary

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

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect('list_stock')
    else:
        ticker = Stock.objects.filter(user=request.user)
        output = []
        tickerList = " ".join([t.ticker for t in ticker])
        print(tickerList)
        tickerData = GetAllStocks(tickerList)
        #tickerData = tickerData.summary_detail.update(tickerData.price)
        print(tickerData.summary_detail)

        return render(request, 'add_stock.html', {'ticker':tickerData.summary_detail|tickerData.price, 'output':output})

def list_stock(request):
    ticker = Stock.objects.filter(user=request.user)
    output = []
    tickerList = " ".join([t.ticker for t in ticker])
    print(tickerList)
    tickerData = GetAllStocks(tickerList)
    #tickerData = tickerData.summary_detail.update(tickerData.price)
    #print(tickerData.summary_detail)
    return render(request, 'stockList.html', {'ticker':tickerData.summary_detail|tickerData.price, 'output':output})


def delete(request, stock_id):
    item = Stock.objects.filter(ticker=stock_id,user=request.user) # To call the database and delete data by using id which is created automaticly
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.filter(user=request.user)
    return render(request, 'delete_stock.html', {'ticker':ticker})
