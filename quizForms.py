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
	return views.getJumbotron("Kandidatenschlüssel.", "<p>Gib ALLE Kandidatenschlüssel an. Schreibe dazu alle Attribute eines Schlüssels in das Textfeld und verwende für jeden Schlüssel eine neue Zeile.</p><p>" + html +"</p>")



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
	html = """<form class="form-inline" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
"""
	for i, fd in enumerate(fds):
		html = html + "<input type=\"text\" class=\"form-control input-lg\" id=\"fd"+str(i)+"\" name=\"fd"+str(i)+"\" value=\""+views.setOfAttributesToString(fd[0])+"\"><h4 style=\"display:inline;\"> -> "+views.setOfAttributesToString(fd[1]) + "</h4><br/>"
	html = html + """</div>
		</div><input type="hidden" value="
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
	html = """<form class="form-inline" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
"""
	for i, fd in enumerate(fds):
		html = html + "<h4 style=\"display:inline;\">" + views.setOfAttributesToString(fd[0]) +" -> </h4><input type=\"text\" class=\"form-control input-lg\" id=\"fd"+str(i)+"\" name=\"fd"+str(i)+"\" value=\""+views.setOfAttributesToString(fd[1])+"\"><br/>"
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



def choosePrimaryKeys(relationString, fdsString, fds, relations, keyrelation):
	html = """<form class="form-inline" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
"""
	for i, relation in enumerate(relations):
		html = html + "<h4 style=\"display:inline;\">" + views.relationToString(relation, i+1) +" </h4><input type=\"text\" class=\"form-control input-lg\" id=\"pk"+str(i)+"\" name=\"pk"+str(i)+"\"><br/>"
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
		<button id="step" name="step" type="submit" class="btn btn-primary" value="8">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Synthesealgorithmus. Primärschlüssel.", "<p>Gib für jede Relation <b>einen</b> möglichen Primärschlüssel an.</p><p>" + html +"</p>")


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
