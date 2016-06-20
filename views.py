#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 
import random
EMPTY_SET_HTML="&empty;"



def keysToString(keys):
	keyString=""
	for key in keys:
		keyString = keyString + "{"
		keyString = keyString + setOfAttributesToString(key)
		keyString = keyString + "}<br/>"
	return keyString
	
	
def setOfAttributesToString(attributes, key=None):
	setOfAttributesString=""
	delimiter=""
	for i,attr in enumerate(sortSet(attributes)):
		if attr != DBnormalizer.EMPTY_SET:
			if key is not None and attr in key:
				underlineAttribute=True
			else:
				underlineAttribute=False

			if DBnormalizer.longAttributeNamesUsed():
				attr = DBnormalizer.dictionaryReplToName[attr]
				if i < len(attributes)-1:
					delimiter=", "
				else:
					delimiter=""
			elif len(attr)>1:
				#fun mode
				if DBnormalizer.EMPTY_SET in attributes:
					offset = 2
				else:
					offset=1
				if i < len(attributes)-offset :
					delimiter=", "
				else:
					delimiter=""

			setOfAttributesString = setOfAttributesString + underlineString(attr, underlineAttribute) + delimiter
	return setOfAttributesString


def sortSet(s):
	return sorted(list(s))

def underlineString(string, underline):
	if underline:
		return "<u>"+string+"</u>"
	else:
		return string

	
def relationToString(relation, i, candidateKeys = None, fds = [], mvds = [], additionalFds = []):
	if candidateKeys is not None:
		if mvds:
			show = "FDs/MVDs"
		else:
			show = "FDs"

		primaryKey = DBnormalizer.getFirstKey(candidateKeys)
		tooltiptext = "<div class='panel panel-primary'><div class='panel-heading'><h5 class='panel-title'>"+show+"</h5></div><div class='panel-body'>"
		if not fds:
			tooltiptext = tooltiptext + "In dieser Relation gelten keine nicht-trivialen Abhängigkeiten."
		else:
			tooltiptext = tooltiptext + fdsToHtmlString(fds, additionalFds)+mvdsToHtmlString(mvds)
		tooltiptext = tooltiptext + "</div></div><div class='panel panel-primary'><div class='panel-heading'><h3 class='panel-title'>Kandidatenschlüssel</h3></div><div class='panel-body'>"+ keysToString(candidateKeys)+"</div></div>"
		if "*" in tooltiptext:
			tooltiptext = tooltiptext + "<h6><small>* Unter anderem diese FD kann mithilfe der Armstrong-Axiome zusätzlich hergeleitet werden</small></h6>"
        else:
		#Do not show tooltip, only blank relation
		primaryKey = None
		tooltiptext = ""



	relationString="R<sub>"+str(i)+"</sub>:={"
	relationString=relationString+setOfAttributesToString(relation, primaryKey)
	relationString = relationString + "}"

	relationString =  addPopoverText(relationString, relationString, tooltiptext)
	
	return relationString
	
	
def fdsToString(fds):
	return fdsMvdsToString(fds, True)

	
def fdsToHtmlString(fds, additionalFds = []):
	string =  fdsToString([fd for fd in fds if fd not in additionalFds]).replace("\n", "<br/>")
	string = string + fdsToString(additionalFds).replace("\n", "*<br/>")
	return string
	


def mvdsToString(mvds):
	return fdsMvdsToString(mvds, False)

def mvdsToHtmlString(mvds):
        return mvdsToString(mvds).replace("\n", "<br/>")



def fdsMvdsToString(fdMvds, isFds):
	if isFds:
		delimiter="->"
	else:
		delimiter="->>"
	fdMvdString=""
	for fdMvd in fdMvds:
		left = setOfAttributesToString(fdMvd[0])
		right = setOfAttributesToString(fdMvd[1])
		if left == "":
			left = EMPTY_SET_HTML
		if right == "":
			right = EMPTY_SET_HTML
		fdMvdString = fdMvdString + left
		fdMvdString = fdMvdString + delimiter
		fdMvdString = fdMvdString + right
		fdMvdString = fdMvdString + "\n"
	return fdMvdString



	


	
def normalFormsToString(normalForms):
	allNormalForms = ["1NF", "2NF", "3NF", "BCNF", "4NF"]
	nfString = ""
	for i in range(len(allNormalForms)):
		nfString = nfString+"""<span class="label label-"""
		if(normalForms[i]):
			label="success"
			glyphicon = "ok"
		else:
			label="danger"
			glyphicon = "flash"
		nfString = nfString+label+"""">"""+allNormalForms[i]+""" <span class="glyphicon glyphicon-"""+glyphicon+"""" aria-hidden=" """+glyphicon+""""></span></span>   """
	return nfString


#schema to string. Input is a list of relations (schema) and a list of candidate keys (one set of candicate keys for each relation in schema)
def schemaToString(schema, keysAndFDs=None):
	schemaString=""
	i=0
	for relation in schema:
		i=i+1
		schemaString = schemaString + relationToString(relation, i, keysAndFDs[i-1]["keys"], keysAndFDs[i-1]["FDs"])+"<br/>"

	return schemaString	


def addTooltipText(string, tooltip):
	if tooltip == "":
		return string
	else:
		return "<span data-toggle=\"tooltip\" data-placement=\"right\"  data-html=\"true\" title=\""+tooltip+"\">"+string+"</span>"


def addPopoverText(string, title, tooltip):
	if tooltip == "":
		return string
	else:
		return "<span data-toggle=\"popover\" data-placement=\"right\"  data-html=\"true\" title=\""+title+"\" data-content=\""+tooltip+"\">"+string+"</span>"


def numberOfAttributesOptions(x):
	options=""
	for i in range(3,DBnormalizer.MAX_NUM_OF_ATTRIBUTES+1):
		options = options + "<option"
		if i==int(x):
			options = options + " selected"
		options = options + ">"+str(i)+"</option>"
	return options
		
		
def wrapInPanel(heading, content, numberOfColumns, panelType="primary"):
	if numberOfColumns == 1:
		x = 12
	elif numberOfColumns == 2:
		x = 6
	elif numberOfColumns == 3:
		x = 4
	else:
		x = 3
	panelString = "<div class=\"col-xs-8 col-sm-6 col-md-"+str(x)+"\"><div class=\"panel panel-"+panelType+"\"><div class=\"panel-heading\"><h3 class=\"panel-title\">"+heading+"</h3></div><div class=\"panel-body\">"+content+"</div></div></div>"
	return panelString
	
	
def getErrorMessageBox(message):
		return """<div class="row"><div class="col-md-12"><div class="alert alert-danger" role="alert"><span class="glyphicon glyphicon-exclamation-sign" aria-hidden="exclamation"></span><span class="sr-only">Error:</span> """+message+"""</div></div></div>"""
	

def getPanelHeading(id, expanded=False, info=""):
	if id=="canonicalCover":
		heading = "Kanonische Überdeckung"
	elif id=="synthese":
		 heading = "Synthesealgorithmus (überführt R in 3NF)"
	elif id=="decompositionBCNF":
                 heading = "Dekompositionsalgorithmus (überführt R in BCNF)"
	elif id=="decomposition4NF":
                 heading = "Dekompositionsalgorithmus (überführt R in 4NF)"
	else:
		heading = id
	if expanded:
		collapse = "in"
	else:
		collapse = ""
	return """<br/><span id=\"collapse"""+id+"""\" data-toggle=\"collapse\" href=\"#container"""+id+"""\">
		<div class=\"panel panel-default\">
			<div class=\"panel-heading\">"""+info+"""<h4><span name=\"menuicon\" class=\"glyphicon glyphicon-menu-right\" aria-hidden\"true\"></span> """+heading+"""</h4></div>
		</div>
		</span>
		<div class=\"panel-collapse collapse """+collapse+"""\" id=\"container"""+id+"""\">"""+getAlgorithmString(id)+"""</div>
		<script>
			$('#collapse"""+id+"""').on('click', function () {
			if($('#container"""+id+"""').is(':visible')){
    			$('#collapse"""+id+"""').find('span[name="menuicon"]').removeClass().addClass('glyphicon glyphicon-menu-right'); 
			}
			else{      
    			 $('#collapse"""+id+"""').find('span[name="menuicon"]').removeClass().addClass('glyphicon glyphicon-menu-down');
			}
			});
		</script>


		"""


def canonicalCoverToString(algorithmResult):
	if DBnormalizer.longAttributeNamesUsed():
		numberOfColumns = 2
	else:
		numberOfColumns = 4
	resultString = getPanelHeading("canonicalCover",False)+"""<div class="row">"""
	resultString =  resultString+wrapInPanel("<span class='badge'>1</span> Linksreduktion", fdsToHtmlString(algorithmResult[0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("<span class='badge'>2</span> Rechtsreduktion", fdsToHtmlString(algorithmResult[1]),numberOfColumns)
	resultString =  resultString+wrapInPanel("<span class='badge'>3</span> &#x3b1;&rarr;&empty; entfernen", fdsToHtmlString(algorithmResult[2]),numberOfColumns)
	resultString =  resultString+wrapInPanel("<span class='badge'>4</span> FDs zusammenfassen", "<strong>"+fdsToHtmlString(algorithmResult[3])+"</strong>",numberOfColumns)
	resultString =  resultString + """</div>"""
	return resultString



def infoNFwasAlreadySatisfied(normalForm):
	return """<span class="label label-danger"><span class="glyphicon glyphicon-info-sign" aria-hidden="info"></span> Das ursprüngliche Schema war bereits in """+normalForm+"""!</span>"""


def synthesealgorithmToString(algorithmResult, satisfiedNormalForms):
	if DBnormalizer.longAttributeNamesUsed():
		numberOfColumns = 2
	else:
		numberOfColumns = 4

	if satisfiedNormalForms[2]:
		#original schema was already in 3NF. Let the user know this
		info = infoNFwasAlreadySatisfied("3NF")
	else:
		info = ""

	resultString = getPanelHeading("synthese",False,info)+"""<div class="row">"""
	resultString =  resultString+wrapInPanel("<span class='badge'>1</span> Kanonische Überdeckung", fdsToHtmlString(algorithmResult[0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("<span class='badge'>2</span> Relationsschemata formen", schemaToString(algorithmResult[1][0], algorithmResult[1][1]),numberOfColumns)
	resultString =  resultString+wrapInPanel("<span class='badge'>3</span> Schlüssel hinzufügen", schemaToString(algorithmResult[2][0], algorithmResult[2][1]),numberOfColumns)
	resultString =  resultString+wrapInPanel("<span class='badge'>4</span> Redundante Schemata eliminieren",  "<strong>"+schemaToString(algorithmResult[3][0], algorithmResult[3][1])+"</strong>",numberOfColumns)
	resultString =  resultString + """</div>"""
	return resultString

def decompositionAlgorithmToString(algorithmResult, normalForm, satisfiedNormalForms):
	numberOfColumns = 1
	if normalForm == "BCNF" and satisfiedNormalForms[3]:
		#original schema was already in 3NF. Let the user know this
		info = infoNFwasAlreadySatisfied("BCNF")
	elif normalForm == "4NF" and satisfiedNormalForms[4]:
		#original schema was already in 3NF. Let the user know this
		info = infoNFwasAlreadySatisfied("4NF")
	else:
		info = ""
	
	if normalForm=="BCNF":
        	algoResultString = algorithmResult[1]+algorithmResult[2]
	else:
		algoResultString =  algorithmResult[1]+algorithmResult[2]#wrapInPanel("Schema in "+normalForm, schemaToString(algorithmResult),numberOfColumns)


	resultString = getPanelHeading("decomposition"+normalForm, False, info)+"""<div class="row">"""
	resultString = resultString+ algoResultString
	resultString = resultString+ """</div>"""
	return resultString


	
def resultToString(relation, fds, mvds, result) :
	if mvds != []:
		#MVDs available
		numberOfColumns = 3
		mvdsPanel = wrapInPanel("MVDs", "<strong>"+mvdsToHtmlString(mvds)+"</strong>",numberOfColumns)
	else:
		#no MVDs, just FDs
		numberOfColumns = 2
		mvdsPanel= ""
	relationPanel = wrapInPanel("Relation", "<strong>"+relationToString(relation,"")+"</strong>",numberOfColumns)
	fdsPanel = wrapInPanel("FDs", "<strong>"+fdsToHtmlString(fds)+"</strong>",numberOfColumns)

	numberOfColumns = 2
	keysPanel = wrapInPanel("Kandidatenschlüssel", "<strong>"+keysToString(result['keys'])+"</strong>",numberOfColumns)
	normalformsPanel = wrapInPanel("Normalformen", normalFormsToString(result['normalForms']),numberOfColumns)
	newschema3NFPanel = synthesealgorithmToString(result['schema3NF'], result['normalForms'])
	canonicalCoverPanel = canonicalCoverToString(result['canonicalCover'])
	newschemaBCNFPanel = decompositionAlgorithmToString(result['schemaBCNF'], "BCNF", result['normalForms'])
	newschema4NFPanel = decompositionAlgorithmToString(result['schema4NF'], "4NF", result['normalForms'])

	return """<div class="panel-body"><h2>Eingabe</h2><div class="panel panel-default"><div class="panel-body"><div class="row">"""+relationPanel + fdsPanel + mvdsPanel + """</div></div></div><br/><h2>Ergebnis</h2><div class="panel panel-default"><div class="panel-body"><div class="row">"""+ keysPanel  + normalformsPanel+ """</div>"""+canonicalCoverPanel+newschema3NFPanel+newschemaBCNFPanel+newschema4NFPanel+ """</div></div></div>"""




def getAlgorithmString(algorithm):
	resultString = ""
	if algorithm == 'canonicalCover':
		resultString = """<div class="row">"""
		resultString =  resultString+wrapInPanel("<span class='badge'>1</span> Linksreduktion", "Was kann ich links weglassen?", 4, "info")
		resultString =  resultString+wrapInPanel("<span class='badge'>2</span> Rechtsreduktion", "Was kann ich rechts weglassen?", 4, "info")
		resultString =  resultString+wrapInPanel("<span class='badge'>3</span> &#x3b1;&rarr;&empty; entfernen", "FDs mit leerer rechter Seite entfernen", 4, "info")
		resultString =  resultString+wrapInPanel("<span class='badge'>4</span> FDs zusammenfassen", "FDs mit gleichen linken Seiten zusammenfassen", 4, "info")
		resultString =  resultString + """</div>"""
	elif algorithm == 'synthese':
		resultString = """<div class="row">"""
		resultString =  resultString+wrapInPanel("<span class='badge'>1</span> Kanonische Überdeckung", "Bestimme die kanonische Überdeckung (s. oben)", 4, "info")
		resultString =  resultString+wrapInPanel("<span class='badge'>2</span> Relationsschemata formen", "Aus jeder FD der kanonischen Überdeckung entsteht eine neue Relation", 4, "info")
		resultString =  resultString+wrapInPanel("<span class='badge'>3</span> Schlüssel hinzufügen", "Füge ein neues Relationsschema mit einem Kandidatenschlüssel hinzu, falls keiner der Kandidatenschlüssel vollständig in einem Schema enthalten ist", 4, "info")
		resultString =  resultString+wrapInPanel("<span class='badge'>4</span> Redundante Schemata eliminieren", "Eliminiere R<sub>a</sub>, wenn R<sub>a</sub> &#x2286; R<sub>a'</sub>", 4, "info")
		resultString =  resultString + """</div>"""
	elif algorithm == 'decompositionBCNF' or algorithm == 'decomposition4NF':
		if algorithm == 'decompositionBCNF':
			targetNF = "BCNF"
			consider="FD"
		else:
			targetNF = "4NF"
			consider="MVD"
		resultString = """<div class="row">"""
		resultString =  resultString+wrapInPanel("Initialisierung", "Starte mit Z={R}", 1, "info")
		resultString =  resultString+wrapInPanel("Solange es noch eine "+consider+" in einem Schema R<sub>i</sub> &#x2208; Z gibt, die die "+targetNF+" verletzt","""
				<ul style="list-style-type:square;">
					<li>Zerlege R<sub>i</sub> in
						<ul style="list-style-type:square;">
							<li>R<sub>i1</sub> = &#x3b1; &#x222a; &#x3b2;  </li>
							<li>R<sub>i2</sub> = R<sub>i</sub> - &#x3b2; </li>
						</ul>
					</li>
					<li>
						Entferne R<sub>i</sub> aus Z und füge R<sub>i1</sub> und R<sub>i2</sub> ein
					</li>
				</ul>
				""", 1, "info")
		resultString =  resultString + """</div>"""
	return resultString


def getAlgorithmTutorial():
	return """<div class="panel-body"><h2>Algorithmen</h2><div class="panel panel-default"><div class="panel-body">"""+getPanelHeading('canonicalCover')+  getPanelHeading('synthese') + getPanelHeading('decompositionBCNF') + getPanelHeading('decomposition4NF') + "</div></div></div>"


