from django import http
from django.shortcuts import render_to_response, get_list_or_404
from django.template.loader import render_to_string, get_template
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext, Context
from meter.models import *
import datetime
from hr.helper import checkCredentials
from django.core.urlresolvers import reverse

def make_pdf(template, data):
    template = get_template(template)
    d= datetime.datetime.now()
    data['date'] = str(d.day)+'-'+str(d.month)+'-'+str(d.year)
    context = Context(data)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def pdf_view(request):
    template = get_template("reports/report.html")
    context = Context({'pagesize':'A4'})
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def active_accounts(request):
    data = {}
    data['active_accounts'] = get_list_or_404(Account, is_active = True)
    data['pagesize'] = 'A4'
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return make_pdf("reports/active_accounts.html", data)
