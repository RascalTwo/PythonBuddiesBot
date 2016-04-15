#Comic Scraping Tutorial

The first thing you need to do is find a comic website that looks scrapable - or just pick one from the list of already-found comic websites that are scrapable.

##Getting the HTML code that Python sees

Find the webpage that has the latest comic shown. This will either be the homepage, or the page which contains a list of most recent/all comics.

Now you need to download this webpage - but not through your web browser. Python will see it diffirently, so we need to have Python save it.

This little script will do fine:

```Python
import requests
with open("page.html", "w") as temp_file:
    temp_file.write(requests.get("URL GOES HERE").text)
```

##Finding the latest comic in the code

Now this is where you have to do your own thing, but don't worry. I'll explain the process I used for the example comic page:

![HTML pattern](http://i.imgur.com/qobCUpD.jpg)

Now as expected, there is a pattern here. Each comic starts with a `div` with a class of `excerpt`. This will be useful later on when finding a random comic.

Now we're provided with four bits of information here: the URL to the comics page, the thumbnail for the comic, a logo, and the title of the comic.

![Labled Pattern](http://i.imgur.com/7ZKEY4Z.jpg)

Now we could either (1) get the comic title now or (2) get the comic title later. This is up to you. I decided to get the comic title later.

Either way, we still need the actual comic image URL, which should be located on the found url. So we need to scrape the Comic URL from the jumble of text.

*****

> In this example, `page_raw_html` represents the raw html of the page.

First splitting the `page_raw_html` by `<div class="excerpt">` splits the text like so:

~[Div Split](http://i.imgur.com/Q2fqgen.jpg)

> The 0th element is all the code before the first `<div class="excerpt">`

So from this, we want the 1st element from the list.

```Python
latest_raw_html = page_raw_html.split('<div class="excerpt">')[1]
```

Next we want the actual URL. So we split by `<a href="`, which splits the text like so:

![a href Split](http://i.imgur.com/21jQDX3.png)

We want the 1st element, like so:

```Python
almost_comic_url = latest_raw_html.split('<a href="')[1]
```

Now we need to get rid of the trailing `"` and everything after it, which can be acomplished with one last simple split by `"`:

![quote Split](http://i.imgur.com/AfOki9n.png)

As you can see, we want the 0th element like so:

```Python
comic_url = almost_comic_url.split('"')[0]
```

So now we do it again! Fetch the new page, and scrape both the title and url to the image.

*****

Now upon fetching the `comic_url`, we find something like this:

~[Comic page HTML](http://i.imgur.com/lrClkvZ.jpg)

This website has yet again been kind and gave unique features to the divs that contain what we need, with the `entry-title` holding our title, and `entry-content` holding the url to the comic image.

We do nearly the same thing we did when getting the `comic_url`: get the 1st element of splitting by `<h1 class="entry-title">`, and then the 0th element of splitting by `</h1>`.

```Python
comic_title = page_raw_html.split('<h1 class="entry-title">')[1].split("</h1>")[0]
```

Next is the image, which is a combination of two things we've done before.

So first we get the 1st element when splitting by `<div class="entry-content">`, and then the 1st element when splitting by `<img src="`, and finally the 0th element when splitting by `"`

```Python
comic_image_url = comic_html.split('<div class="entry-content">')[1].split("<img src="')[1].split('"')[0]
```

That's all the scraping! Now just wrap it all up in bot commands and we're done!