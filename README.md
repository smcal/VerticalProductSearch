Vertical Search Engine
======================


----------


A simple Python application that allows you to search multiple online stores at once.

Features
------------
* Uses public published APIs which provides stability and you don't have to worry about website changes
* Provides a web interface to enter a query to get results
* Can be used as a standalone API to use in your own applications.  All you need is two lines of code (plus the import statement) to get results
* Adding new APIs is very simple. 
* Results are statistically analyzed to provide ranked list of products from all available sites
* You get to compare prices on the same item found in multiple sites in one page instead of surfing to each one

Note
------


----------

This is my very first Python application so I know the code can be done better.  If anyone forks this and uses it please let me know.  Would be very interested in seeing what can be done with this.

API Keys
------------
----------
The best environment for this project is a *nix platform.  There is no simpler system for getting a server up and running (and the price doesn't hurt either).  While this can be done on Windows and Mac since Python pip can be installed on it, on Linux you only have to pip install a few packages and you are up and running.  No convoluted setup required.

The first thing you will need is API credentials in order to access Amazon, Ebay and Walmart.  Of the three Amazon is the most convoluted.  You need to create an Amazon associates account as if you are setting up a storefront but once you do you go to Tools -> Product Advertising API to create your access keys (as of Dec 2017)

Amazon  - [Amazon Associates Account](https://affiliate-program.amazon.com/assoc_credentials/home)  
ebay       - [ebay developers program](https://go.developer.ebay.com/)  
Walmart - [Walmart Open API](https://developer.walmartlabs.com/)  

>Enter the values in sample-api-config.cfg and rename it to api-config.cfg

Dependencies (current as of Dec 20, 2017)
-----------------------------------------

----------
(Note some may be duplicated since you may not want to use certain product APIs)

**General Dependencies**
*  Install pip3 (apt-get install python3-pip)
*  Install metapy (pip3 install metapy)
*  Install Flask (pip3 install Flask)

**Amazon** 
Repository and instructions found at [Amazon Simple Product API](https://github.com/yoavaviram/python-amazon-simple-product-api)  

*  Install Bottlenose (pip3 install bottlenose)
*  Install lxml (pip3 install lxml)
*  Install dateutil (pip3 install python-dateutil)
*  Install Amazon Simple Product API (pip3 install python-amazon-simple-product-api)

**EBay**
Repository and instructions found at [eBay API SDK for Python](https://github.com/timotheus/ebaysdk-python)  

* Install lxml (apt-get install python3-lxml)
* Install eBay API SDK for Python (easy_install3 ebaysdk)

**Walmart**
Repository and instructions found at [Wapy](https://github.com/caroso1222/wapy)  

* Install requests (pip3 install requests)
* Install wapy (pip3 install wapy)

Usage
--------
----------
If you want to use the web interface:
>python3 flaskimplementation.py  

This starts the flask web server so just launch a browser and enter:
>localhost:5000

There are two way to perform a search.  One is to enter the query directly and the code will remove the stopwords and perform stemming on the rest.  This is good for some searches but may not be good for searches where the stopwords are part of the product name you are interested in (for example "Go Cubes" which is chewable coffee).  So if you surround the query in quotes the code will not process the query to remove the stopwords.  The results are still processed statistically to provide ranked list of results.

If you want to use this as an API in your own apps I have a mini test driver (tester.py) that prints out the data to the console and shows you how to make the api call.  The data strcture returned is an ordered list of tuples.
>python3 tester.py

