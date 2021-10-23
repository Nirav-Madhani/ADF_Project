from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json
from .api import *
from datetime import datetime
# Create your views here.
def home(request):
    ##Detail View For Each Ticker
    if request.method == 'POST':
        ticker = request.POST['ticker']
        # pk_56e9488bfddc4f64805631337556e19e    
        try:
             tickerData = GetSingleStock(ticker)             
        except Exception as e:
            api = "Error..."
        print(tickerData.price)
        return render(request, 'home.html', {'api':tickerData.summary_detail[ticker],'price':tickerData.price[ticker],
        'chart':tickerData.history(start='2021-10-22',interval='1m')[ticker]})
    else:
        return render(request, 'home.html', {'ticker':"Enter a Ticker Symbol Above..."})

    # return render(request, 'home.html', {'api':api}). Here, {'api':api} context dictionary


def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        tickerList = " ".join([t.ticker for t in ticker])
        print(tickerList)
        tickerData = GetAllStocks(tickerList)
        #tickerData = tickerData.summary_detail.update(tickerData.price)
        print(tickerData.summary_detail)

        return render(request, 'add_stock.html', {'ticker':tickerData.summary_detail|tickerData.price, 'output':output})

def delete(request, stock_id):
    item = Stock.objects.get(ticker=stock_id) # To call the database and delete data by using id which is created automaticly
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker':ticker})
