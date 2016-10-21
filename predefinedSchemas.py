#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()

param = cgi.FieldStorage()

#this file contains some schemas appearing in the exercise sheets of the tum gdb course
#if no parameter is given, this script prints all schema keys as html list items. If parameter "schema" is given, the corresponding schema will be printed.

schemas = {}
schemas["s0"] = "ABCDEF;A->BC;C->DA;E->ABC;F->CD;CD->BEF"
schemas["s1"] = "Name,Aufgabe,Max,Erzielt,ErzieltSumme,MaxSumme,KNote,Bonus,GNote;KNote,Bonus->GNote;Aufgabe->Max;ErzieltSumme->KNote;Name,Aufgabe->Erzielt;Name->ErzieltSumme,Bonus,GNote;->MaxSumme"
schemas["s2"] = "ABCDEFG;A->BC;DE->B;F->A;E->BF;A->DE;C->A"
schemas["s3"] = "ABCD;AB->>C;BC->>D;BA->CD;DA->B"
schemas["s4"] = "person,kindName,kindAlter,fahrradTyp,fahrradFarbe;person->>kindName,kindAlter;person->>fahrradTyp,fahrradFarbe;kindName->kindAlter"

def getSchemaIds():
	schema_ids = []
	for schema_id in schemas:
		schema_ids.append(schema_id)
	return sorted(schema_ids)

print """
"""
try:
	schema_id = param['schema'].value
	print schemas[schema_id]
except KeyError:
	predefindedSchemaIds = getSchemaIds()
	schemaList = ""
	for i, schemaId in enumerate(predefindedSchemaIds):
		schemaList = schemaList + "<li><a href=\"#\" onclick=\"setContent('"+str(schemaId)+"')\">Schema "+str(i+1)+"</a></li>"
	print schemaList
