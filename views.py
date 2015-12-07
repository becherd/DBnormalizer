#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 


def keysToString(keys):
	keyString=""
	for key in keys:
		keyString = keyString + "{"
		for attr in key:
			keyString = keyString + attr
		keyString = keyString + "}<br/>"
	return keyString
	
	
def setOfAttributesToString(attributes):
	setOfAttributesString=""
	for attr in attributes:
		setOfAttributesString = setOfAttributesString + attr
	return setOfAttributesString
	
def relationToString(relation, i):
	relationString="R<sub>"+i+"</sub>:={"
	relationString=relationString+setOfAttributesToString(relation)
	relationString = relationString + "}"
	return relationString
	
	
def fdsToString(fds):
	fdString=""
	for fd in fds:
		for attr in fd[0]:
			fdString = fdString + attr
		fdString = fdString + "->"
		for attr in fd[1]:
			fdString = fdString + attr
		fdString = fdString + "\n"
	return fdString

	
def fdsToHtmlString(fds):
	return fdsToString(fds).replace("\n", "<br/>")
	
	
def mvdsToString(mvds):
	mvdString=""
	for mvd in mvds:
		for attr in mvd[0]:
			mvdString = mvdString + attr
		mvdString = mvdString + "->>"
		for attr in mvd[1]:
			mvdString = mvdString + attr
		mvdString = mvdString + "\n"
	return mvdString

def mvdsToHtmlString(mvds):
        return mvdsToString(mvds).replace("\n", "<br/>")

	
def normalFormsToString(normalForms):
	nfString = ""
	for nf in normalForms:
		nfString = nfString + nf + "<br/>"
	return nfString

	
def schemaToString(schema):
	schemaString=""
	i=0
	for relation in schema:
		i=i+1
		schemaString = schemaString + relationToString(relation, str(i)) + "<br/>"
	return schemaString
		
		
		
def wrapInPanel(heading, content):
	panelString = "<div class=\"col-xs-6 col-md-4\"><div class=\"panel panel-primary\"><div class=\"panel-heading\"><h3 class=\"panel-title\">"+heading+"</h3></div><div class=\"panel-body\">"+content+"</div></div></div>"
	return panelString
	
	
def getErrorMessageBox(message):
		return "<div class=\"container\"><div class=\"col-md-8\"><div class=\"alert alert-danger\" role=\"alert\"><span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span><span class=\"sr-only\">Error:</span> "+message+"</div></div></div>"
	
	
def resultToString(relation, fds, mvds, keys, normalForms, targetNf, newSchema) :
	keysPanel = wrapInPanel("Kandidatenschlüssel", keysToString(keys))
	relationPanel = wrapInPanel("Relation", relationToString(relation,""))
	fdsPanel = wrapInPanel("FDs", fdsToHtmlString(fds))
	if mvds != []:
		mvdsPanel = wrapInPanel("MVDs", mvdsToHtmlString(mvds))
	else:
		mvdsPanel= ""
	normalformsPanel = wrapInPanel("Normalformen", normalFormsToString(normalForms))
	if newSchema != []:
		newschemaPanel = wrapInPanel("Schema in "+targetNf, schemaToString(newSchema))
 	else:
		newschemaPanel=""
	return "<div class=\"panel-body\"><h3>Eingabe</h3><div class=\"row\">"+relationPanel + "" + fdsPanel + "" + mvdsPanel + "</div><br/><h3>Ergebnis</h3><div class=\"row\">"+ keysPanel + "" + normalformsPanel+ ""+ newschemaPanel+ "</div></div>"
