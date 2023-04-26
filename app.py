import sqlite3
from ping import *
from RenderGraph import *
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from datetime import *
import csv
import requests 

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

#route for the stock user input form
@app.route("/", methods={"GET", "POST"})
def index():

    chart = None
    symbol = None
    chart_type = None
    func = None
    format = '%Y-%m-%d'

    #read symbols from csv file
    file = open("sp500.csv", "r")
    symbols = list(csv.reader(file,delimiter=","))
    file.close()
    
    if request.method == "POST":
            #get form data
            symbol = request.form.get("symbol")
            chart_type = request.form.get("chart_type")
            func = int(request.form.get('func'))
            str_Start_Date = request.form.get("lowerDate")
            str_End_Date = request.form.get("upperDate")

            #validate form data and flash error if any
            if symbol == "":
                flash("Symbol is required")
            elif chart_type == "":
                flash("chart_type is required")
            elif func == "":
                flash("Time Series is required")
            elif str_Start_Date == "":
                flash("Start Date is required")
            elif str_End_Date == "":
                flash("End Date is required")
            else:
                if str_Start_Date and str_End_Date:
                    #convert date strings to datetime objects
                    #currently stuck somewhere around here where wont read date correctly
                    #"ValueError: time data '{' does not match format '%Y-%m-%d'"
                    start_Date = datetime.strptime(str_Start_Date, format)
                    end_Date = datetime.strptime(str_End_Date, format)

                    #if no errors, query api
                    processed_data = pingAPI(func, symbol, start_Date, end_Date)
                    if not processed_data:
                        flash("No data available for the selected range.")
                    else:
                        #calling the function to render graph
                        chart = render_graph(chart_type, str_Start_Date, str_End_Date, processed_data, symbol)

    #render the template with the chart data if any    
    return render_template("stock.html", chart = chart, symbols = symbols)

app.run(host="0.0.0.0")