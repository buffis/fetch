#Fetch

Fetch is a domain-specific language, which allows for simple HTTP fetching and filtering.
It’s feature-set can be described as a combination of [HTTPie](https://github.com/jakubroztocil/httpie)/[curl](http://curl.haxx.se/), and simple filtering using libraries like [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) and regex.

Fetch makes it possible to write a short input file, which describes what data to fetch from a web-page, and how it should be manipulated and formatted for output.
Two sample fetch input files are provided further down in this README, along with their outputs.

It is built on top of Python, using the following libraries:
* [PLY](http://www.dabeaz.com/ply/) for lexin/parsing
* [Requests](http://docs.python-requests.org/en/latest/) for the fetching
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) for HTML parsing

Program execution is performed in (up to) four steps:

1. **Fetch URL**
  * Declare the target URL(s) to fetch
  * Declare headers, cookies and params for the URL(s)
2. **Filter results coarsely by doing:**
  * Line-based filtering (keep lines specified function(s))
  * HTML Tag-based filtering (keep tags matching specified function(s))
3. **Filter the coarsly filtered lines/TAGs more finely by doing things like:**
  * Strip away text matching a pattern from a line
  * Fetch attr/text from a TAG
  * or more… (currently existing filters described here)
4. **Format output for being read by external script**
  * Output is normally JSON, but can be output in other formats (set by flags to the executable)
  * For simple outputs, just assigning a variable “output” is sufficient.

A more in-depth walkthrough of the Fetch language is available in this document “Fetch in-depth description”. This document covers examples of all different fetch methods, filters and output options. The grammar of the Fetch language is also present here.

A short guide for installing and running Fetch programs are available in the section “Installing and running Fetch” further below.

##Sample programs 

###Program 1:
```
github <- 'https://github.com/buffis?tab=repositories'  # Fetch URL
repolist = [findall: '.repo-list-item'] github  # Filter coarsely
repolistnames = [findall: '.repo-list-name'] repolist  # Filter coarsely
repodescriptions = [children: '.repo-list-description'] repolist  # Filter coarsely
repolinks = [children: 'a'] repolistnames  # Filter coarsely
output = {text} repolinks   # Filter finely, output
```

**Output:**
```
[
  "swedbank-qif-export",
  "easyftpd",
  "danm8ku"
]
```

###Program 2:
```
github <- 'https://github.com/buffis?tab=repositories'  # Fetch URL
repolist = [findall: '.repo-list-item'] github  # Filter coarsely
repolistnames = [findall: '.repo-list-name'] repolist  # Filter coarsely
repodescriptions = [children: '.repo-list-description'] repolist  # Filter coarsely
repolinks = [children: 'a'] repolistnames  # Filter coarsely
names = {text: ''} repolinks  # Filter finely
hrefs = {attr: 'href'} repolinks  # Filter finely
descriptions = {text: ''} repodescriptions  # Filter finely
output = dict{'names': names, 'hrefs': hrefs, 'descriptions': descriptions}  # Output
```

**Output:**
```
{
  "hrefs": [
    "/buffis/swedbank-qif-export",
    "/buffis/easyftpd",
    "/buffis/danm8ku"
  ],
  "names": [
    "swedbank-qif-export",
    "easyftpd",
    "danm8ku"
  ],
  "descriptions": [
    "QIF export from Swedbank's internet bank service",
    "Automatically exported from code.google.com/p/easyftpd",
    "danm8ku"
  ]
}
```

##Downloading, installing and running Fetch

NOTE: Fetch has not yet been test on Python 3. Instructions are for 2.7, but any Python 2.X release above 2.5 should work.

####Download

The latest version of Fetch is 0.0.1, available as a ZIP here:

TODO: Add link

... or you could instead just clone this git repository by running:

```
TODO: add command
```

####Installation on Ubuntu/Debian (primary target platform)

**Install dependencies**

```
sudo apt-get install python python-ply python-beautifulsoup python-requests unzip
```

**Extract fetch and run**

```
unzip fetch.zip
python fetch.py sample/github_buffis_repoinfo.fetch
```

####Installation on Windows (works fine, but a bit unusual for scripting stuff)

* Install Python 2.X (includes pip)
* In cmd.exe do
  * ```pip install beautifulsoup ply requests```
* Unzip fetch.zip somewhere
* In cmd.exe do
  * ```python fetch sample/github_buffis_repoinfo.fetch```

####Installation on OSX (untested)

I haven’t actually tried this on OSX, but installation should be similar to Windows.

Install Python, install deps through PIP, run.
