# Consuming 3rd Party APIs & Webscraping with Django


## Road Map

1. Set up a new Django Project
2. Intro to Python's `request`
3. Hitting OpenWeatherMap's API
4. Rendering our weather data
5. Intro to Web Scraping
6. Beautiful Soup
7. Sifting through the soup
8. Rendering our news

## 1. Set up a new Django Project
We're going to start fresh with a new Django App for this project. From the terminal, we can do this with either:

`django-admin startproject homepage` or `python3 -m django startproject homepage`

This will create our project titled 'homepage'. `cd` into homepage and start our `main_app`:

`python manage.py startapp main_app`

Now let's spin up our server and head to localhost:8000 to make sure everything is working!
## 2. Intro to Python's `requests`

Python comes with a fantastic library called 'requests' that we can use to -- you guessed it -- issue requests! Let's spin up a python shell with `python3 manage.py shell` to have a look at what it does!

```python
# First we need to import the library
>>> import requests
# Lets start with something simple
>>> requests.get('https://spacejam.com/1996')
<Response [200]>
```

We got a resposne! What does the HTTP code 200 mean? Please tell me that my precious spacejam.com is still up.

Another way that we can just get the response code returned by chaining `.status_code` to the end of our get request. But what if we want some data back? Lets use everyone's favourite test API, [JSON Placeholder](https://jsonplaceholder.typicode.com/). We'll hit the endpoint to receive the first Todo.

```python
>>> requests.get('https://jsonplaceholder.typicode.com/todos/1').status_code
200
# All good! Let's pull some data out of the response
>>> requests.get('https://jsonplaceholder.typicode.com/todos/1').text
'{\n  "userId": 1,\n  "id": 1,\n  "title": "delectus aut autem",\n  "completed": false\n}'
# Hmmmm. That doesn't look quite right. It would be nice to get some JSON 
# returned instead of a string value
>>> requests.get('https://jsonplaceholder.typicode.com/todos/1').json()
{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
```

Beautiful! We can now hit an API, and have our data returned in a format that's nice and easy to work with! We can even continue to chain off of that request (as python is want to do) and try to get some more specific values from it! 

> Important! Even though the data has been parsed to JSON, we are still coding in Python! This means that we have to use square bracket notation to access the keys of our data, not dot notation as we do in Javascript.

```python
# With dot notation
>>> requests.get('https://jsonplaceholder.typicode.com/todos/1').json().completed
AttributeError: 'dict' object has no attribute 'completed'

# With Python's square bracket notation
>>> requests.get('https://jsonplaceholder.typicode.com/todos/1').json()['completed']
False
```

## 3. Hitting OpenWeatherMap's API

Now that we know how to hit an API, get a response, and pull the data out of that response, lets get connected to [OpenWeatherMaps]()'s API. This is a great (and free!) API that we can get a surprising amount of data from.  

Once you create an account, and get your API key set up...

... start talking about `python-dotenv`
## 4. Rendering our weather data
Basic
## 5. Intro to Web Scraping

Webscraping is something that has become quite popular in the coding community. Allow me to paint you a word picture:

You're building an app that needs some data from a pre-existing website. Of course, as a knowledgable developer, you check to see if they have an API that your app can consume. You're shocked to find that they don't! How are you going to get that juicy data into your app now?

Enter Webscraping, a way to, as the name suggests, scrape through a website, and extract just the information that we want. Come to think of it, lets go back to an eariler request that we made, and have a look at the data that is returned. 

Open a Python shell:
```python
>>> requests.get('https://spacejam.com/1996').text
'<html>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n<!-- Copyright 1996 Warner Bros. Online -->\r\n...'
```

Look at that! Right away we can tell that we're looking at the compiled HTML document for spacejam.com! It doesn't look that great though, does it. And the only way that we have access to it is in one giant string. In the words of every infomercial, "There has to be a better way!". Enter...
## 6. Beautiful Soup

Beautiful Soup is the go-to for webscraping with Python. In fact, it's the go-to for webscraping in general. It is a very powerful library, that allows us to find, filter, and even travel through the HTML returned from `requests` like we would a DOM tree. To start off, we just need to install it with `pip3 install beautifulsoup4` (Yes, we want version 4. If you just install `BeautifulSoup`, it is an older release). We'll also go ahead and install `html5lib` as our html-parser du-jour. 

## 7. Sifting through the soup

Now let's go back and have a look at that Space Jam Page. Our goal, is to pull the copyright statement out of the page and have it returned to us in the console. 

<screenshots, I'm sure>

If we have a look at the HTML of the site, we can see that all of the content is within these `<center>` tags, and the very last `<font>` tag holds our copyright statemtnt. So let's use BeautifulSoup to get us there:

```python
# first we need to import BeautifulSoup
>>> from bs4 import BeautifulSoup
# let's save the response of our request
>>> page = requests.get('https://spacejam.com/1996')
# now the magic
>>> soup = BeautifulSoup(page.content, 'html5lib')
# now if we have a look at soup, we'll see our html more clearly
# Let's put it to work!
>>> soup.find_all('font')
[<font class="footer-links" size="-1"><a href="https://policies.warnerbros.com/...
# Looks like a familiar data type! Let's access the last one only.
>>> soup.find_all('font')[-1]
<font size="-1">SPACE JAM, characters, names, and all related<br/>indicia...
# Looks good!
```
As you can see, Beautiful Soup has methods we can use to search through the html. There are many very useful ones, such as `find_all()` as we used above to return a list of results, `find()` which will return the first matching, `find_next()`, `find_parent()`, the list goes on. When we call these methods, the first argument we pass in is the HTML tag of the element we are looking for. So in our case, we were looking for all matching `<font>` tags (quite outdated, yes). Since `find_all()` is the most popular method, Beautiful Soup has given us a shortcut to it. 
```python
>>> soup.find_all('font')
# is the same as 
>>> soup('font')
```

Along with the tag name, we can also pass in a class, id, or even attributes to get more specific results:

```python
>>> soup.find_all('div', class_="nav")
# returns all <div>s with the class 'nav'
>>> soup.find_all('h1', id="title-124")
# returns any <h1> with the id 'title-124'

# if you want to search by CSS selectors, useful with selecting multiple classes
>>> css_soup.select("p.content.aside#1")
# returns <p class="aside content" id="1">
```

Of course, pulling the entire tag isn't going to be too helpful when we're just looking for the actual text inside of it. In our previous example, we have the enclosing `<font>` tags, and that pesky `<br/>` right in the middle. Unfortunately, that `<br/>` tag will be a bit of an issue, but simple to solve. We check both the contents and the children of a tag by calling `.contents` on it. So lets get back to Space Jam:

```python
>>> soup('font')[-1]
# this gets us the last <font> tag on the page with our shorthand syntax
>>> soup('font')[-1].contents
['SPACE JAM, characters, names, and all related', <br/>, 'indicia...'
# Ah ha! Another List! Lets' do a bit of formatting to print that out nicely
print(f"{soup('font')[-1].contents[0]} {soup('font')[-1].contents[2]}")
SPACE JAM, characters, names, and all related indicia are trademarks of Warner Bros. © 1996
```

## 8. On to the News!

Now, being completely comfortable in scraping absolutely anything out of any website ever, lets get down to business. Today we'll be scraping the developer news site dev.to. 
