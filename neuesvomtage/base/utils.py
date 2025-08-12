#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import csv
import time
import urllib
import datetime
from random import randint

from decimal import Decimal
from django.conf import settings
from django.core.cache import cache, parse_backend_uri
from django.core.mail import send_mail
from django.db import connection
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

def random_items(model, key="id", count=1):
    """ Selects a random item by using random.randint instead of the database RANDOM() 
    yields one item at a time (generator)"""
    _max = model.objects.aggregate(Max(key))[key+'__max']
    i = 0

    while i<count:
        try:
            yield model.objects.get(pk=randint(1, _max))
            i += 1
        except model.DoesNotExist:
            pass

def csv_response_for_queryset(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response, quoting=csv.QUOTE_ALL)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                if isinstance(val, basestring):
                    val = val.encode('utf8')
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def addorincrease(adict, akey, avalue):
    """" adds a value to a dict or - if already present - increases the value"""
    if adict.get(akey, None):
        adict[akey] += avalue
    else:
        adict[akey] = avalue

def cached(key, func, subkey=None):
    """ Calls a function and caches the result if it's not already in cache.

    if a subkey is given this function will cache the function result in a 
    dict referenced by the subkey. In this case None will also be returned
    if the cache key exists, but the value is no dict or the dict doesn't 
    contain the subkey.

    usage: cached('my_key', lambda: Product.objects.get(pk=1))
           cached('my_key', lambda: Product.objects.get(pk=1), 'products')
    """
    key = key.replace(' ', '')
    cdata = cache.get(key)
    if cdata is None:
        val = func()
        if subkey:
            cache.add(key, {subkey:val})
        else:
            cache.add(key, val)
        return val
    else:
        if not subkey:
            return cdata
        else:
            if isinstance(cdata, dict):
                if cdata.get(subkey, None):
                    return cdata.get(subkey)
                else: # cache the function result
                    cdata[subkey] = func()
                    cache.set(key, cdata)
                    return cdata.get(subkey)
            else: # subkey present but no dict in the cache
                raise Exception("trying to access a subkey where no subkey was stored")

def cache_clean():
    try:
        import cmemcache as memcache
    except ImportError:
        try:
            import memcache
        except:
            return
    scheme, host, params = parse_backend_uri(settings.CACHE_BACKEND)
    c = memcache.Client(host.split(";"))
    c.flush_all()

def send_template_mail(subject, template, recipientlist, context_dict={}):
    """ Renders a template with the given context and mails the result.
    """
    body = render_to_string(template, context_dict)
    send_mail(subject, body, settings.DEFAULT_TO_EMAIL, recipientlist)

def is_request_secure(request):
    """ additional is_secure() method which pays attention to the ssl fields set
    by proxies """
    if request.is_secure():
        return True
    #Handle the Webfaction case until this gets resolved in the request.is_secure()
    if 'HTTP_X_FORWARDED_SSL' in request.META:
        return request.META['HTTP_X_FORWARDED_SSL'] == 'on'
    #Handle the lighty/gunicorn case 
    if 'HTTP_X_FORWARDED_PROTO' in request.META:
        return request.META['HTTP_X_FORWARDED_PROTO'] == 'https'
    return False
