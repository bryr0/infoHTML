# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template import Context
import os
from pprint import pprint
from .getdata import Info
import json


# Create your views here.

def index(request):
	if request.method == 'GET':
		return render(request, 'info/index.html')

		#private_storage = FileSystemStorage(location=path.join(settings.MEDIA_ROOT,"new"))
def getdata(fn):

	REP = dict()
	DATA = dict()
	file = {"new":fn[0],"old":fn[1]}
	
	REP.update({"REP16":[1,5]})
	REP.update({"REP06":[1,2]})
	REP.update({"REP13":[1,2]})
	REP.update({"REP08":[['Sesiones','Actualmente','Concurrentes','WARNING','Name_Users'],1,2,3,4,5]})
	REP.update({"REP09":[["Sesiones","Devices ","dba_users"],1,2,3]})
	REP.update({"REP23":[["Lecturas Logicas","Lecturas Fisicas","Hit Ratio %","Escrituras Fisicas"],1,2,3,4]})
	REP.update({"REP24":[["GETS","GETHITS","HIT%","PINS","PINHITS","HIT%","RELOADS","MISSES%"],1,2,3,4,5,6,7,8]})
	REP.update({"REP25":[["DATA DICTIONARY GETS","DATA DICTIONARY GETMISSES","HIT%"],1,2,3]})

	i = Info()

	for x in file:
		DATA.update({ x: i.extract(os.path.join(x, file[x]),REP) })

	N = fn[0].split("\\")[-1]
	DBNAME = N[N.find("_")+1:-5]
	SERVERNAME=N.split("\\")
	SERVERNAME=N[:N.find("_")]
	DATA.update({ "dbname" : DBNAME,"servername": SERVERNAME })
	return DATA

def upload(request):
	#print(request.FILES['new'])
	if request.method == 'POST' and request.FILES['old'] and request.FILES['new']:
		
		d = []
		data = {}
		## upload new file
		for x in ["new","old"]:
			rp = os.path.join(settings.MEDIA_ROOT,x)

			myfile = request.FILES[x]
			fs = FileSystemStorage(location=rp)

			fp = os.path.join(rp,myfile.name)
			d.append(fp)

			if(os.path.exists(fp)):
				os.remove(fp)
			fs.save(myfile.name, myfile)
			
		data = getdata(d)

		if request.POST.get('newmoth'):
			data["new"]["date"] = request.POST.get('newmoth').lower().capitalize()

		if request.POST.get('oldmoth'):
			data["old"]["date"] = request.POST.get('oldmoth').lower().capitalize()
			
		return render(request, 'info/graphic.html',{"data":data})
		return HttpResponse(json.dumps(data), content_type="application/json")
		# 	return HttpResponse(json.dumps(response_data), content_type="application/json")
		# return redirect('graphic/')

def graphic(request):
	return HttpResponse(json.dumps(response_data), content_type="application/json")




