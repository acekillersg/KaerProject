# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from io import BytesIO
from django.conf import settings
from django.shortcuts import render
from Storage.forms import PageToRenderForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from Storage import reportpdf
from Storage.models import Building, JPLogging, SAALogging


# Create your views here.
def index(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    if request.method == "POST":
        form = PageToRenderForm(request.POST)
        if form.is_valid():

            building_name = form.cleaned_data['building_choice']
            options = form.cleaned_data['options']
            from_date = form.cleaned_data.get('from_date')
            from_time = form.cleaned_data.get('from_time')
            to_date = form.cleaned_data.get('to_date')
            to_time = form.cleaned_data.get('to_time')

            print from_date, from_time, to_date, to_time

            # jplogging = JPLogging.objects.filter(chwshdr__gte=11.1334)
            # print jplogging[0]
            print "Data is valid, generating report!"
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            tempbuffer = BytesIO()
            resultsbuffer = building_name
            p = canvas.Canvas(tempbuffer)
            reportpdf.userPDF(p, resultsbuffer)
            pdf = tempbuffer.getvalue()
            tempbuffer.close()
            response.write(pdf)
            print "Report generated successfully!"

            return response

            # form.save(commit=True)
            # return render(request, "Storage/index.html", locals())
        # else:
        #     print form.errors
    else:
        form = PageToRenderForm()

    # return response
    return render(request, "Storage/index.html", locals())


def pdfview(request):
    with open(os.path.join(settings.BASE_DIR, 'Storage/data/Storage/mongodb.pdf')) as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline; filename=report.pdf'
        return response
    pdf.closed


def genpdf():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    tempBuffer = BytesIO()
    resultsbuffer = " "
    p = canvas.Canvas(tempBuffer)
    reportpdf.userPDF(p, resultsbuffer)
    pdf = tempBuffer.getvalue()
    tempBuffer.close()
    response.write(pdf)

    return response