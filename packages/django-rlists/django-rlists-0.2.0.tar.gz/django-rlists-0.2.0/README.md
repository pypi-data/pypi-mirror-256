django-rlists
=============


Django Rlists is a web application for processing the
[FIDE rating lists](https://en.wikipedia.org/FIDE) of chess players. It's written in
[Python](https://www.python.org) using [Django](https://www.djangoproject.com) and
[chart.js](https://www.chartjs.org).

Note that this project is not an official project of FIDE. Also note that this project is
still in a pre-alpha state so use it with care.


Overview
========

* The required inputs are XML files. Here are some examples:
```
static/rlists/frl/standard_aug12frl_xml.zip
static/rlists/frl/standard_feb24frl_xml.zip
```

* There are currently 139 FIDE rating lists that are available in XML format (the rest
  are avaible in a plain text format). Their download URLs are contained in these files:
```
static/rlists/frl/fide_rating_lists.txt
static/rlists/frl/fide_rating_lists.json
```


Copyright and License
=====================


Django Rlists is free software: you can redistribute it and/or modify it under the
terms of the [GNU General Public License](https://www.github.com/patrickwayodi/django-rlists/blob/gh-pages/LICENSE)
license as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

Django Rlists is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

