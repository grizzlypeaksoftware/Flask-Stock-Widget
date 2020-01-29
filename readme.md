### Introduction

In this repo, we are going to make a quick and simple webpage using Python Flask, jQuery and Bootstrap.  This is a simple back-end for freont-end style microservice, except that we're also hosting a single-page app with the same API.  

This simple Python based microservice using Flask will returns stock quote and historical data. We'll also make a quick website using Flask's template system, called Jinja to make an easy Bootstrap 4 site.  The site will feature a graph of the stock's performance over the period of 12 months. 

We'e going to use the yFinance module for Python.  This module uses the Yahoo Finance API to provide it's data. This API is publicly accessible, but not guaranteed to perform for long-term production use. 

Just some history here.  Yahoo Finance used to provide a comma-separated, and later a JSON api in their YUI library that provided awesome and reliable stock quote data.  Unfortunately, the times changed and the classic Yahoo Finance API was taken out of prod.

Some awesome people have worked hard to provide this current Python lib for yFinance.  I checked out two or three of them, one for Node and another one for Python.  The one we're using in this code is the best one I could find at the time of this writing.  For now at least, it will provide us with a great data source for our sample Python code.

### Sample Code for this Project

Thank you for checking out "OUR" code!  This is a public repository under the Apache License.  If you want to clone or fork the code to your local machine, by all means please do!  Thank you for looking at the code, and you're always welcoe to send a pull request if you want to make a change.

from command line...
```bash
git clone https://github.com/grizzlypeaksoftware/Flask-Stock-Widget
```

### Installing Python and Flask

This guide assumes that you have at least a basic understanding of Python programming and how to perform general OS level tasks. You will need a code editor to create this application. I used Visual Studio code.

If you do not already have Python installed, you should install it. The installation for your operating system can be found at the following location. [https://www.python.org/about/gettingstarted/](https://www.python.org/about/gettingstarted/ "Python Getting Started Guide")

Once you have successfully installed Python on your operating system, first create a virtual environment in the application directory and activate it.

```bash
cd Flask-Stock-Widget
virtualenv -p python3 venv
source venv/bin/activate
```

Then you will want to install Flask.

```bash
pip install flask
```

Once the installation is complete you should now have Python and Flask running in your development environment.

### Installing the yfinance Module and associated dependencies

The next step will be to install the Yahoo Finance Python module along with the [lxml XML toolkit](https://lxml.de/) and the HTML parser [html5lib](https://pypi.org/project/html5lib/). Much like installing Flask, we will use PIP.

```bash
pip install yfinance lxml html5lib
```

You can learn all about the Yahoo Finance module on their Github website. [https://github.com/ranaroussi/yfinance](https://github.com/ranaroussi/yfinance). If you really want to get into coding using this module, I would recommend exploring their code because some features are not documented on their website.

This module leverages internal Yahoo API's that were built for their website. There are no guarantees on the data that gets returned from Yahoo Finance using this module.

### Getting started with the API Controller

We will create a file called `app.py`, an we will start with the following code.

```python
from flask import Flask, request, render_template
```

This means we will import the Flask module that we installed earlier, and we're going to use Flask, request and render_template for this project.

* Flask - the main Flask module
* request - provides a handler for the HTTP  request object
* render_template - provides Flask with a handler for rendering HTML templates. We will use this later in the tutorial to create the demo website.

Next we will import the yfinance module.

```python
import yfinance as yf
```

Next in `app.py` we will instantiate the Flask application.

```python
app = Flask(__name__)
```

And from here we are ready to finish off the first API call. Here is the completed code.

```python
from flask import Flask, request, render_template
import yfinance as yf

app = Flask(____name____)

@app.route("/quote")
def display_quote():
  symbol = request.args.get('symbol', default="AAPL")

  quote = yf.Ticker(symbol

  return quote.info

if ____name____ == "____main____":
  app.run(debug=True)
```

This creates a single URL for the website that will contact Yahoo Finance and pull stock quote information in JSON format. So let's run the app!

From the command line type `python app.py`. This will start the app running and should surface the API on it's default port (5000).

```bash
python app.py
* Serving Flask app "app" (lazy loading)
* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
* Debug mode: on
* Restarting with stat
* Debugger is active!
* Debugger PIN: 146-068-908
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

If you were to go to the following URL, you should now see stock quote information for Apple listed in JSON in the Browser.

[http://localhost:5000/quote](http://localhost:5000/quote)

```json
{
  "52WeekChange": 1.0365322,
  "SandP52WeekChange": 0.24646628,
  "address1": "One Apple Park Way",
  "algorithm": null,
  "annualHoldingsTurnover": null,
  "annualReportExpenseRatio": null,
  "ask": 309.42,
  "askSize": 1100,
  ...
}
```

Congrats! You are now getting stock quotes back from a simple API. But before we can draw a chart we will also need to pull some historical info.

### Pulling Historical Data

We will do this by creating a new route called `/history`. We're going to set the period of time to be 1 year (`1y`), and the interval to be monthly (`1mo`).

```python
@app.route("/history")
def display_history():

    symbol = request.args.get('symbol', default="AAPL")
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")        
    quote = yf.Ticker(symbol)   
    hist = quote.history(period=period, interval=interval)
    data = hist.to_json()
    return data
```

This works in much the same way as pulling the stock quote, except returns historical stock quote data so that you can render it into a price chart!

Once you hit save on the application, you should be able to access this new API route by going to [http://localhost:5000/history](http://localhost:5000/history)

On both API's you can pass the symbol on the query string by adding `?symbol=<ticker symbol>`. For example [http://localhost:5000/history?symbol=TSLA](http://localhost:5000/history?symbol=TSLA)

Congrats!  You now have a working stock quote API that you can use to create a simple widget with a chart. Let's get started.

### Setting up the Homepage using Flask

Flask comes with a simple template renderer called Jinja. We will use it to pull some HTML from the file system and render it to the browser. This is what we will use to create our website demo.

In order to do this you will need to create a folder in your project called "templates" because Jinja always looks in the templates folder. If you look in that folder you will find the HTML template. We're using a bunch of libraries in this HTML to make things easy so let's take a look.

You can find the HTML for this template at the following location. [https://github.com/grizzlypeaksoftware/Flask-Stock-Widget/blob/master/templates/homepage.html](https://github.com/grizzlypeaksoftware/Flask-Stock-Widget/blob/master/templates/homepage.html)

First you will see that we're pulling in the CSS for Bootstrap 4 via CDN. We are also using some of the Jinja markup in this template to pull in our static css file that is found in `static/css`.

```html
<!-- Bootstrap core CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

<!-- Custom styles for this template -->
<link href="{{ url_for('static', filename='css/site.css') }}" rel="stylesheet">
```

In the lower area of the HTML we are calling a number of JavaScript libraries from CDN.

* jquery - A cross-browser all-purpose JavaScript library
* Bootstrap 4 - a UI framework for HTML5
* Highcharts - A javascript charting library
* Moment.js - A date/time converter for JavaScript
* Number.js - A number formatter for JavaScript

All of these scripts are referenced as follows...

```html
<script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/export-data.js"></script>
<script src="https://code.highcharts.com/modules/accessibility.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/numeral.js/2.0.6/numeral.min.js"></script>
```

Finally, we will reference our own page's javascript file so that we can finish off the project.

```html
<script src="{{ url_for('static', filename='scripts/site.js')}}"></script>
```

### Rendering the template as a Web Page

Finally we will create a route in `app.py` in which we render the template as HTML on the page and test it.

```python
@app.route("/")
def home():
	return render_template("homepage.html")
```

If you run the application again from the command line and then navigate to http://localhost:5000/ you should now see a website that looks roughly like this..

![Partially Completed Stock Market Widget](//images.ctfassets.net/j3qbf0mggam8/1Ku5yomC3P9qksMRJWQXsK/2589f2773a9bb2be537efbf4a5a8baf4/stock_widget_partial.png)

### Pulling the API Content with AJAX

Now everything else will be done directly from JavaScript. We will query the stock API using jQuery's AJAX method, and get the quote and historical information. Since here are two calls, first we will get the quote, and then we will pull the history. This could also be done a little differently by pulling the quote and history simultaneously, but that's not how I set it up this time.

First this that happens with the page's DOM is loaded is that the page will call the Init() function, where we will initiate the request to get the Stock Quote.

```javascript
Site.prototype.GetQuote = function(){
    // store the site context.
    var that = this;

    // pull the HTTP REquest
    $.ajax({
        url: "/quote?symbol=" + that.symbol,
        method: "GET",
        cache: false
    }).done(function(data) {

        // set up a data context for just what we need.
        var context = {};
        context.shortName = data.shortName;
        context.symbol = data.symbol;
        context.price = data.ask;

        if(data.quoteType="MUTUALFUND"){
            context.price = data.previousClose
        }      

        // call the request to load the chart and pass the data context with it.
        that.LoadChart(context);
    });
};
```

Next we will load the chart data and pass it to the chart rendering function.

```javascript
Site.prototype.LoadChart = function(quote){
    var that = this;
    $.ajax({
        url: "/history?symbol=" + that.symbol,
        method: "GET",
        cache: false
    }).done(function(data) {
        that.RenderChart(JSON.parse(data), quote);
    });
};
```

Once the data has been received, RenderChart is called, with the data that has been collected. We will then use Highcharts to render the chart data.

```javascript
Site.prototype.RenderChart = function(data, quote){
    var priceData = [];
    var dates = [];

    var title = quote.shortName + " (" + quote.symbol + ") - " + numeral(quote.price).format('$0,0.00');

    for(var i in data.Close){
        var dt = i.slice(0,i.length-3);
        var dateString = moment.unix(dt).format("MM/YY");
        var close = data.Close[i];
        if(close != null){
            priceData.push(data.Close[i]);  
            dates.push(dateString);
        }       
    }

    Highcharts.chart('chart_container', {
        title: {
            text: title
        },  
        yAxis: {
            title: {
                text: ''
            }
        },  
        xAxis: {
            categories :dates,
        },  
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },  
        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                }
            },
            area: {
            }
        },  
        series: [{
            type: 'area',
            color: '#85bb65',
            name: 'Price',
            data: priceData
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 640
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }    
    });
};
```

So, putting this all together, we should now have a stock market widget all complete that will pull all of the data and then draw the Stock Market widget on the page. We have added a little input form so that you can change the symbol by typing in a new symbol, like TSLA, MSFT, or VTSAX in order to show the information that that particular type of investment.

Once it's completed the finished website should look roughly like this...

![Create a Python and Flask based stock quote widget](//images.ctfassets.net/j3qbf0mggam8/3k2i2QH0adGADRqXEdEfhL/62f34eef2bb589f701cfb88f522501f2/stock_widget.png)

### Conclusion

In this article we used Python and Flask to make a simple stock market API that can pull data form Yahoo Finance and then apply it to create a simple website that shows a stock market chart.

I hope that you enjoyed this tutorial!  

If you are interested in reading any of our other programming articles, some good ones to check out are...

Building an API Gateway with NGINX
[https://www.grizzlypeaksoftware.com/articles?id=4vlfDp2ZanpAh3bSuUzPeZ](https://www.grizzlypeaksoftware.com/articles?id=4vlfDp2ZanpAh3bSuUzPeZ)

Build a simple Node.js OAuth server with JWT
[https://www.grizzlypeaksoftware.com/articles?id=6G3prVhXnUeSYUEqEoCqq2](https://www.grizzlypeaksoftware.com/articles?id=6G3prVhXnUeSYUEqEoCqq2)

Create a secure web server in Node.js
[https://www.grizzlypeaksoftware.com/articles?id=JDcsPW2raSic6oc6MCYaM](https://www.grizzlypeaksoftware.com/articles?id=JDcsPW2raSic6oc6MCYaM)
