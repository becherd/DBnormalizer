#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 
import random
import views
EMPTY_SET_HTML="&empty;"
EMPTY_SET = "$"


def formQuizStart(relation, fds, mvds):
	inputString ="<div class=\"well\">Du hast folgendes eingegeben:</div>"
	if DBnormalizer.longAttributeNamesUsed():
		inputString = inputString = inputString + views.inputToString(relation, fds,mvds, "default")
		inputString = inputString + "<div class=\"well\">Dass du gleich nicht so viel tippen musst, machen wir daraus mal das hier:</div>"
	DBnormalizer.resetDictionaries()
	inputString = inputString +  views.inputToString(relation, fds,mvds, "default")
	relationString = views.setOfAttributesToString(relation)
	fdsString = views.fdsToString(fds)+views.mvdsToString(mvds)
	html = """<form class="form" action="quiz.py" method="POST">"""
	html = html + "<p>Willkommen beim Quiz.</p>" 
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="1">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return  views.getJumbotron("Hallo.", html ) + inputString

def candidateKeys(relationString, fdsString):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
		<textarea type="text" class="form-control input-lg" name="candidatekeys" id="candidatekeys" rows="5"></textarea>
		</div>
		</div>
		<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="2">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kandidatenschlüssel.", "<p>Gib <b>alle</b> Kandidatenschlüssel an. Schreibe dazu alle Attribute eines Schlüssels in das Textfeld und verwende für jeden Schlüssel eine neue Zeile.</p><p>" + html +"</p>")



def normalForm(relationString, fdsString):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
		<select class="form-control input-lg" name="normalform" id="normalform">
			<option value="0NF">keine Normalform</option>
			<option value="1NF">1NF</option>
			<option value="2NF">2NF</option>
			<option value="3NF">3NF</option>
			<option value="BCNF">BCNF</option>
			<option value="4NF">4NF</option>
		</select>
		</div>
		</div>
		<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-1">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Normalform.", "<p>Wähle die Normalform aus, in der sich die Relation befindet.</p><p>" + html +"</p>")



def canonicalCoverLeftReduction(relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">
"""
	for i, fd in enumerate(fds):
		html = html + "<div class=\"row\"><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"fd"+str(i)+"\" name=\"fd"+str(i)+"\" value=\""+views.setOfAttributesToString(fd[0])+"\" style=\"text-align:right;\"></div><div class=\"col-md-1 text-center\" style=\"max-width:80px;\"><br/><h2 style=\"display:inline;\"><sub>-></sub></h2></div> <div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" value=\""+views.setOfAttributesToString(fd[1])+"\" disabled=\"disabled\"></div></div></br>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-2">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. Linksreduktion.", "<p>Gib die neuen linken Seiten der FDs an.</p><p>" + html +"</p>")



def canonicalCoverRightReduction(relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">	
"""
	for i, fd in enumerate(fds):
		html = html + "<div class=\"row\"><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" value=\""+views.setOfAttributesToString(fd[0])+"\" disabled=\"disabled\" style=\"text-align:right;\"></div><div class=\"col-md-1 text-center\" style=\"max-width:80px;\"><br/><h2 style=\"display:inline;\"><sub>-></sub></h2></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"fd"+str(i)+"\" name=\"fd"+str(i)+"\" value=\""+views.setOfAttributesToString(fd[1])+"\"></div></div><br/>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-3">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. Rechtsreduktion.", "<p>Gib die neuen rechten Seiten der FDs an.</p><p>" + html +"</p>")


def canonicalCoverRemoveEmptyRight(relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
"""
	for i, fd in enumerate(fds):
		html = html + "<div class=\"checkbox\"><label><h4 style=\"display:inline;\"><input type=\"checkbox\" name=\"removeindices\" value=\""+str(i)+"\">"+views.fdToHtmlString(fd)+"</h4></label></div>"
	html = html + """</div>
		</div><input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-4">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. FDs entfernen.", "<p>Möglicherweise musst du FDs entfernen. Markiere alle FDs, die entfernt werden sollen.</p><p>" + html +"</p>")


def canonicalCoverCollapse(relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
		<textarea class="form-control input-lg" name="finalfds" id="finalfds" rows="5">"""+views.fdsToString(fds).replace(EMPTY_SET, "")+"""</textarea>
		</div>
		</div>
		<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="4">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. FDs zusammenfassen.", "<p>Möglicherweise musst du FDs zusammenfassen. Gib hier alle FDs an, die übrig bleiben.</p><p>" + html +"</p>")


def formRelationSchemas(relationString, fdsString, fds, relations):
	html = """<form class="form" action="quiz.py" method="POST">
		"""
	html = html + "<p>Du hast die kanonische Überdeckung gefunden:</p>" 
	html = html + "<h4 style=\"display:inline;\">"+views.fdsToHtmlString(fds)+"</h4></br/>"
	html = html + "<p>Daraus entstehen diese Relationen:</p>"
	html = html + "<h4 style=\"display:inline;\">"+views.schemaToString(relations)+"</h4>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="5">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Glückwunsch.", html )


def addKeyRelation(relationString, fdsString, fds, relations):
	html = """<form class="form" action="quiz.py" method="POST">"""
	html = html + views.schemaToString(relations)
	html = html + """<div class="row">
			<div class="col-sm-12">"""
	html = html + "<div class=\"checkbox\"><label><h4 style=\"display:inline;\"><input type=\"checkbox\" id=\"addkeyrelation\" name=\"addkeyrelation\" value=\"true\">neue Relation hinzufügen</h4></label></div>"
	html = html + "<input type=\"text\" class=\"form-control input-lg\" id=\"newrelation\" name=\"newrelation\">"
	html = html + """</div>
		</div><input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="6">Weiter</button>
		</div>
		</div>
		</form>
		<script>
			$('#addkeyrelation').on('change', function(){
				if($(this).prop('checked')){
					$('#newrelation').prop('disabled', false);
				}
				else{
					$('#newrelation').prop('disabled', true);
				}
			}).change();
		</script>
	"""
	return views.getJumbotron("Synthesealgorithmus. Relation hinzufügen.", "<p>Möglicherweise musst du eine neue Relation hinzufügen.</p><p>" + html +"</p>")





def removeRedundantRelations(relationString, fdsString, fds, relations, keyrelation):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">"""
	for i, relation in enumerate(relations):
		html = html + "<div class=\"checkbox\"><label><h4 style=\"display:inline;\"><input type=\"checkbox\" name=\"removeindices\" value=\""+str(i)+"\">"+views.relationToString(relation, i+1)+"</h4></label></div>"
	html = html + """</div>
		</div><input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+keyrelation+"""" name="keyrelation"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="7">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Synthesealgorithmus. Relationen entfernen.", "<p>Möglicherweise musst du überflüssige Relationen entfernen. Kreuze alle Relationen an, die entfernt werden müssen.</p><p>" + html +"</p>")



def choosePrimaryKeys(relationString, fdsString, fds, relations, targetnf = "3NF", relationnumbers=[]):
	html = """<form class="form" action="quiz.py" method="POST">
"""
	currentRelations = []
	for i, relation in enumerate(relations):
		currentRelations.append(views.setOfAttributesToString(relation))
		if relationnumbers:
			relationnumber = relationnumbers[i]
		else:
			relationnumber = i+1
		if targetnf == "3NF":
			algorithm = "Synthesealgorithmus"
			nextstep = "8"
		elif targetnf == "BCNF":
			algorithm = "Dekompositionsalgorithmus für BCNF"
			nextstep = "10"
		else:
			algorithm = "Dekompositionsalgorithmus für 4NF"
			nextstep = "10"
		html = html + "<div class=\"row\"><div class=\"col-md-1\"><br/><h4 style=\"display:inline;\">" + views.relationToString(relation, relationnumber) +" </h4></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"pk"+str(i)+"\" name=\"pk"+str(i)+"\"></div></div><br/>"
	currentRelationsString = ",".join(currentRelations)
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+currentRelationsString+"""" name="currentrelations"></input>
		<input type="hidden" value="
"""+",".join(relationnumbers)+"""" name="relationnumbers"></input>
		<input type="hidden" value="
"""+str(targetnf)+"""" name="targetnf"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="
"""+nextstep+"""">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron(algorithm+". Primärschlüssel.", "<p>Gib für jede Relation <b>einen</b> möglichen Primärschlüssel an.</p><p>" + html +"</p>")


def formResultSyntheseAlgorithm(relationString, fdsString, fds, relations, keysAndFDs, primarykeys):
	html = """<form class="form" action="quiz.py" method="POST">
		"""
	html = html + "<p>Folgende Relationen sind entstanden:</p>"
	html = html + "<h4 style=\"display:inline;\">"+views.schemaToString(relations, keysAndFDs, primarykeys)+"</h4>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="9">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Glückwunsch.", "<p>Du hast die ursprüngliche Relation in die 3NF überführt.</p><p>" + html +"</p>")





def decompositionAlgorithm(relationString, fdsString, relations, relationnumbers, targetnf = "BCNF"):
	currentRelations = []
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
"""
	for i, r in enumerate(relations):
		currentRelations.append(views.setOfAttributesToString(r))
		html = html + "<div class=\"radio\"><label><h4 style=\"display:inline;\"><input type=\"radio\" name=\"splitrelation\" value=\""+str(i)+"\">"+views.relationToString(r, relationnumbers[i])+"</h4></label></div>"
		html = html + "<div class=\"row\"><div class=\"col-md-1\" style=\"text-align:right;\"><br/><h4 style=\"display:inline;\">R<sub>"+ relationnumbers[i].strip() +"1:=</sub></h4></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"first"+str(i)+"\" name=\"first"+str(i)+"\" disabled=\"disabled\"></div><div class=\"col-md-1\" style=\"text-align:right;\"><br/><h4 style=\"display:inline;\">R<sub>"+ relationnumbers[i].strip() +"2:=</sub></h4></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"second"+str(i)+"\" name=\"second"+str(i)+"\" disabled=\"disabled\"></div></div><br/>"
	html = html + "<div class=\"radio\"><label><h4 style=\"display:inline;\"><input type=\"radio\" name=\"splitrelation\" value=\"-1\">keine</h4></label></div>"
	html = html + """<script>
			$('[name="splitrelation"]').on('change', function(){
				if($(this).prop('checked')){
					$('[id^="first"]').prop('disabled', true);
					$('[id^="second"]').prop('disabled', true);
					$('#first'+$(this).val()).prop('disabled', false);
					$('#second'+$(this).val()).prop('disabled', false);				
				}
			}).change();
		</script>"""
	currentRelationsString = ",".join(currentRelations)
	html = html + """</div>
		</div><input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+currentRelationsString+"""" name="currentrelations"></input>
		<input type="hidden" value="
"""+",".join(relationnumbers)+"""" name="relationnumbers"></input>
		<input type="hidden" value="
"""+str(targetnf)+"""" name="targetnf"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="9">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Dekompositionsalgorithmus. "+targetnf+".", "<p>Gib an, ob Relationen aufgespalten werden müssen und welche Relationen entstehen.</p><p>" + html +"</p>")




def formResultDecompositionAlgorithm(relationString, fdsString, relations, relationnumbers, keysAndFDs, primarykeys, targetnf = "BCNF"):
	if targetnf == "BCNF":
		#decomposition algorithm 4NF
		nextstep = "9"
	else:
		#end of quiz
		nextstep = "11"
	html = """<form class="form" action="quiz.py" method="POST">
		"""
	html = html + "<p>Folgende Relationen sind entstanden:</p>"
	html = html + "<h4 style=\"display:inline;\">"+views.schemaToString(relations, keysAndFDs, primarykeys)+"</h4>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="4NF" name="targetnf"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="
"""+nextstep+"""">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Glückwunsch.", "<p>Du hast die ursprüngliche Relation in die "+targetnf+" überführt.</p><p>" + html +"</p>")




def quizFinal(relationString, fdsString):
	html = """<form class="form" action="index.py" method="POST">"""
	html = html + "<input type=\"hidden\" value=\""+relationString+"\" name=\"relation\"></input>"
	html = html + "<input type=\"hidden\" value=\""+fdsString+"\" name=\"fds\"></input>"
	html = html + """<div class="row">
		<div class="col-xs-3 pull-right">
		<br/>
		<a href="index.py" class=\"btn btn-default" role="button">Neu</a>
		<button id="submitbutton" name="mode" type="submit" class="btn btn-primary" value="showResults">Ergebnis anzeigen</button>
		</div>
		</div></form>"""
	return views.getJumbotron("Glückwunsch.", "<p>Du hast das Quiz geschafft.</p><p>" + html +"</p>")
