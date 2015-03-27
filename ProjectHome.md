# Django SEO App #
This little Django SEO App enables you to manage deep links exchange.


## Manage ##
  * Campaigns: site information
  * Links information: anchor, url, additional text
  * Links customization: specific css classes, target, additional javascript (ie: tracker)
  * BackLinks : url, anchor
  * Check Backlinks automatically via Admin's Action (we are using http://code.google.com/p/scrapemark/ to analyze the backlinking page)

## Usage ##

### In your project's settings.py ###
```
    INSTALLED_APPS += ('link_exchange')
```

### In your template's files ###
  * to publish a link directly through the template
```
{%load link_ex%}
{%link "name"%}
```
  * to publish a link through an object's field containing html AND the {%link "name"%} tag
```
{%load link_ex%}
{% autoescape off %}
{%evaluate object.textfield%}
{% endautoescape %}
```