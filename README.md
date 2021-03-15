# python-web-automatation-selenium
Various tests with Selenium using Python to scrape the River Island website (UK)

The project idea is to collect all the products in every single River Island shop around the user location (which will be "london" by default).

The program will collect ONLY "men shoes", size 8.

Therefore, the software should first collect all the products in the website page (category "men shoes") and then check in which stores those products are located.
The software is based on the layout of the website; after "studying" the components of it, I was able to navigate the automata through the dynamic pages.

Thanks to the option "FIND IN STORE", a normal user is able to check whether the product is nearby or not. 

So why not using an automata to check ALL the products locations available ?

The first step: 

COLLECT PRODUCTS LINKS

The second step:

NAVIGATE THROUGH EACH LINK AND COLLECT THE PRODUCTS' LOCATIONS

All the data will be collected on a local file.

IMPROVEMENTS:

The data could be savev into a database to speed up the process. I have noticed that Python goes a bit slow with file management.

To speed up the search process, I have thought to multiprocessing; executing multiple searches on multiple products could improve the speed of the whole software.

Note: The software is not 100% accurate; the products and the layout update continuously. 

DUE TO COVID-19 THE WEBSITE HAS REMOVED THE "FIND IN STORE" LINK, THEREFORE THE SOFTWARE OBVIOUSLY WILL NOT WORK.
