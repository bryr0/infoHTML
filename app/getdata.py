# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint
from bs4 import BeautifulSoup
import re
import json
from copy import copy

class Info:
	def __init__(self):
		pass

	def subDirs(path):
		return [ os.path.join(dirpath, file) for dirpath, subdirList, fileList in os.walk(path) for file in fileList]


	def th(tr):
		return len(tr.find_all("th"))


	def tables(self,table,string):
		for key,value in enumerate(table):
			tr = value.find_all("tr")

			for i in value.find_all("center"):
				if string in i.text:
					return table[key+1]


	def tablesRow(self,table,rows):
		Rows = copy(rows)
		data={}
		KEYS = None
		key = None
		TableRow= None

		if isinstance(Rows[0], list):
			KEYS = Rows.pop(0)
		else:
			key = Rows.pop(0)-1

		#return Rows,KEYS,key
		for tr in table.find_all("tr"):
			TableRow = tr.find_all("td")
			for c,_ in enumerate(TableRow):
				if TableRow[0].text.strip():
					row = []
					for n in Rows:
						if c == n-1:
							if TableRow[c].text.strip():
								row.append(TableRow[c].text.strip().replace(",",""))
					if row:
						if KEYS:
							data.update({ KEYS[c].strip() : row})
						else:
							data.update({ TableRow[key].text.strip().replace(",","") : row})
		return data



	def extract(self,file,REP):
		RES={}
		soup =None
		TABLE= None
		MONTHS ={"jan" : "Enero","ene" : "Enero","feb": "Febrero","mar": "Marzo","apr":"Abril","abr":"Abril","may" : "Mayo","jun":"Junio",
				"jul":"Julio","ago":"Agosto","aug":"Agosto","sep":"septiembre","oct":"Octubre","nov":"Noviembre","dec":"Diciembre","dic":"Diciembre"}

		if os.path.exists(file):
			with open(file,"r") as f:
				
				soup = BeautifulSoup(f.read().replace("\n", ""), "html.parser")
				TABLE = soup.find_all('table',width="90%")

				for x in REP:
					RES.update({x:self.tablesRow(self.tables(TABLE,x),REP[x])})

				if self.getDate(TABLE).lower() in MONTHS:
					RES.update({"date" : MONTHS[self.getDate(TABLE).lower()] })
		else:
			print("file dont exist")

		return RES



	def getDate(self,TABLE):
		for x in TABLE:
			for i in x.select("tr > td", recursive=False):
				if(re.search("\d{2}\ \d{4}\ \d{2}\:\d{2}\:\d{2}", i.text)):
					return i.text.strip().split()[1]



