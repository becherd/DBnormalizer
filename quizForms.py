#! /usr/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 
import random
import views
EMPTY_SET_HTML="&empty;"
EMPTY_SET = "$"




def formQuizStart(relation, fds, mvds):
	inputString ="<div class=\"well\">Du hast folgendes eingegeben:</div>"
	if DBnormalizer.longAttributeNamesUsed():
		inputString = inputString = inputString + views.inputToString(relation, fds,mvds)
		inputString = inputString + "<div class=\"well\">Dass du gleich nicht so viel tippen musst, machen wir daraus mal das hier:</div>"
	DBnormalizer.resetDictionaries()
	inputString = inputString +  views.inputToString(relation, fds,mvds)
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
		<button id="step" name="step" type="submit" class="btn btn-primary" value="1">Start</button>
		</div>
		</div>
		</form>
	"""
	return  views.getJumbotron("Hallo.", html ) + inputString

def candidateKeys(numberOfTries, numberOfSteps, relationString, fdsString, candidateKeys, noRightSideAttributes):
	hints =views.getCandidateKeyHints(candidateKeys, noRightSideAttributes)

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
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		"""+hints+"""<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="2">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kandidatenschlüssel.", "<p>Gib <b>alle</b> Kandidatenschlüssel an. Schreibe dazu jeweils alle Attribute eines Schlüssels in das Textfeld und verwende für jeden Schlüssel eine neue Zeile."+views.getHintPopover("Gib z.B. für die Kandidatenschlüssel {ABC} und {DE} ein:<br/><br/><pre>ABC<br/>DE</pre>")+"</p><p>" + html +"</p>")



def normalForm(numberOfTries, numberOfSteps, relationString, fdsString):
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
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-1">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Normalform.", "<p>Wähle die höchste Normalform aus, in der sich die Relation befindet.</p><p>" + html +"</p>")



def canonicalCoverLeftReduction(numberOfTries, numberOfSteps, relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">
"""
	for i, fd in enumerate(fds):
		html = html + "<div class=\"row\"><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"fd"+str(i)+"\" name=\"fd"+str(i)+"\" value=\""+views.setOfAttributesToString(fd[0])+"\" style=\"text-align:right;\"></div><div class=\"col-md-1 text-center\" style=\"max-width:80px;\"><br/><h2 style=\"display:inline;\"><sub>-></sub></h2></div> <div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" value=\""+views.setOfAttributesToString(fd[1])+"\" disabled=\"disabled\"></div></div></br>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-left">
                <button class="btn btn-xs btn-default" type="reset"><span class="glyphicon glyphicon-repeat aria-hidden="true"></span> Eingabe zurücksetzen</button>
                </div>
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-2">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. Linksreduktion.", "<p>Gib die neuen linken Seiten der FDs an."+views.getHintPopover("Um die leere Menge &empty; einzugeben, lasse das Feld einfach leer.")+"</p><p>" + html +"</p>")



def canonicalCoverRightReduction(numberOfTries, numberOfSteps, relationString, fdsString, fds):
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
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-left">
                <button class="btn btn-xs btn-default" type="reset"><span class="glyphicon glyphicon-repeat aria-hidden="true"></span> Eingabe zurücksetzen</button>
                </div>
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-3">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. Rechtsreduktion.", "<p>Gib die neuen rechten Seiten der FDs an."+views.getHintPopover("Um die leere Menge &empty; einzugeben, lasse das Feld einfach leer.")+"</p><p>" + html +"</p>")


def canonicalCoverRemoveEmptyRight(numberOfTries, numberOfSteps, relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12"><pre>
"""
	for i, fd in enumerate(fds):
		html = html + "<div class=\"checkbox\"><label><h4 style=\"display:inline;\"><input type=\"checkbox\" name=\"removeindices\" value=\""+str(i)+"\">"+views.fdToHtmlString(fd)+"</h4></label></div>"
	html = html + """</pre></div>
		</div><input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="3-4">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. FDs entfernen.", "<p>Möglicherweise musst du FDs entfernen. Markiere alle FDs, die entfernt werden sollen.</p><p>" + html +"</p>")


def canonicalCoverCollapse(numberOfTries, numberOfSteps, relationString, fdsString, fds):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
		<textarea class="form-control input-lg" name="finalfds" id="finalfds" rows="5">"""+views.fdsToString(fds).replace(EMPTY_SET, "")+"""</textarea>
		<br/>
		</div>
		</div>
		<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-left">
                <button class="btn btn-xs btn-default" type="reset"><span class="glyphicon glyphicon-repeat aria-hidden="true"></span> Eingabe zurücksetzen</button>
                </div>
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="4">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Kanonische Überdeckung. FDs zusammenfassen.", "<p>Möglicherweise musst du FDs zusammenfassen. Gib hier alle FDs an, die übrig bleiben."+views.getHintPopover("Editiere die FDs so, dass die finale kanonische Überdeckung im Eingabefeld steht.")+"</p><p>" + html +"</p>")


def formRelationSchemas(numberOfTries, numberOfSteps, relationString, fdsString, fds, relations):
	html = """<form class="form" action="quiz.py" method="POST">
		"""
	html = html + "<p>Du hast die kanonische Überdeckung gefunden:</p>" 
	html = html + "<pre><h4 style=\"display:inline;\">"+views.fdsToHtmlString(fds)+"</h4></pre><br/>"
	html = html + "<p>Daraus entstehen diese Relationen:</p>"
	html = html + "<pre><h4 style=\"display:inline;\">"+views.schemaToString(relations)+"</h4></pre>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="5">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Glückwunsch.", html )


def addKeyRelation(numberOfTries, numberOfSteps, relationString, fdsString, fds, relations):
	html = """<form class="form" action="quiz.py" method="POST">"""
	html = html + "<pre><h4 style=\"display:inline;\">"+views.schemaToString(relations)+"</h4></pre>"
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
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
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
	return views.getJumbotron("Synthesealgorithmus. Relation hinzufügen.", "<p>Möglicherweise musst du eine neue Relation hinzufügen."+views.getHintPopover("Wenn du eine neue Relation hinzufügen möchtest, markiere die Checkbox und gib die Attribute der neuen Relation in das Textfeld ein. Um z.B. die Relation R<sub>x</sub>:={ABCDE} hinzuzufügen, gib ein:<br/><br/><pre>ABCDE</pre>")+"</p><p>" + html +"</p>")





def removeRedundantRelations(numberOfTries, numberOfSteps, relationString, fdsString, fds, relations, keyrelation):
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12"><pre>"""
	for i, relation in enumerate(relations):
		html = html + "<div class=\"checkbox\"><label><h4 style=\"display:inline;\"><input type=\"checkbox\" name=\"removeindices\" value=\""+str(i)+"\">"+views.relationToString(relation, i+1)+"</h4></label></div>"
	html = html + """</pre></div>
		</div><input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+keyrelation+"""" name="keyrelation"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="7">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Synthesealgorithmus. Relationen entfernen.", "<p>Möglicherweise musst du überflüssige Relationen entfernen. Kreuze alle Relationen an, die entfernt werden müssen.</p><p>" + html +"</p>")



def choosePrimaryKeys(numberOfTries, numberOfSteps, relationString, fdsString, fds, relations, targetnf = "3NF", relationnumbers=[]):
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
		html = html + "<div class=\"row\"><div class=\"col-md-2\" style=\"text-align:right;\"><br/><h4 style=\"display:inline;\">" + views.relationToString(relation, relationnumber) +" </h4></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"pk"+str(i)+"\" name=\"pk"+str(i)+"\"></div></div><br/>"
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
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="
"""+nextstep+"""">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron(algorithm+". Primärschlüssel.", "<p>Gib für jede Relation <b>einen</b> möglichen Primärschlüssel an."+views.getHintPopover("Schreibe dazu für jede Relation die Attribute des Primärschlüssels in das zugehörige Textfeld. Um z.B. für die erste Relation den Primärschlüssel {ABCDE} hinzuzufügen, gib in das erste Textfeld ein:<br/><br/><pre>ABCDE</pre>")+"</p><p>" + html +"</p>")


def formResultSyntheseAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, fds, relations, keysAndFDs, primarykeys):
	html = """<form class="form" action="quiz.py" method="POST">
		"""
	html = html + "<p>Folgende Relationen sind entstanden:</p>"
	html = html + "<pre><h4 style=\"display:inline;\">"+views.schemaToString(relations, keysAndFDs, primarykeys)+"</h4></pre>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="
"""+views.fdsToString(fds)+"""" name="currentfds"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="9">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Glückwunsch.", "<p>Du hast die ursprüngliche Relation in die 3NF überführt.</p><p>" + html +"</p>")





def decompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, relations, relationnumbers, targetnf = "BCNF"):
	currentRelations = []
	html = """<form class="form" action="quiz.py" method="POST">
		<div class="row">
		<div class="col-sm-12">
"""
	for i, r in enumerate(relations):
		currentRelations.append(views.setOfAttributesToString(r))
		html = html + "<div class=\"radio\"><label><h4 style=\"display:inline;\"><input type=\"radio\" name=\"splitrelation\" value=\""+str(i)+"\">"+views.relationToString(r, relationnumbers[i])+"</h4></label></div>"
		html = html + "<div class=\"row\"><div class=\"col-md-1\" style=\"text-align:right;\"><br/><h4 style=\"display:inline;\">R<sub>"+ relationnumbers[i].strip() +"1:=</sub></h4></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"first"+str(i)+"\" name=\"first"+str(i)+"\" disabled=\"disabled\"></div><div class=\"col-md-1\" style=\"text-align:right;\"><br/><h4 style=\"display:inline;\">R<sub>"+ relationnumbers[i].strip() +"2:=</sub></h4></div><div class=\"col-md-2\"><input type=\"text\" class=\"form-control input-lg\" id=\"second"+str(i)+"\" name=\"second"+str(i)+"\" disabled=\"disabled\"></div></div><br/>"
	html = html + "<div class=\"radio\"><label><h4 style=\"display:inline;\"><input type=\"radio\" name=\"splitrelation\" value=\"-1\" checked>keine Relation aufspalten</h4></label></div>"
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
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
		<div class="row">
		<div class="col-xs-2 pull-right">
		<br/>
		<button id="step" name="step" type="submit" class="btn btn-primary" value="9">Weiter</button>
		</div>
		</div>
		</form>
	"""
	return views.getJumbotron("Dekompositionsalgorithmus. "+targetnf+".", "<p>Gib an, ob Relationen aufgespalten werden müssen und welche Relationen entstehen."+views.getHintPopover("Wähle zunächst die Relation aus, die du aufspalten willst, oder wähle <em>keine Relation aufspalten</em>. Wenn du eine Relation aufspalten willst, gib die Attribute der Relationen ein, die neu entstehen.")+"</p><p>" + html +"</p>")




def formResultDecompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, mvds, relations, relationnumbers, keysAndFDsMVDs, primarykeys, targetnf = "BCNF"):
	if targetnf == "BCNF" and mvds:
		#decomposition algorithm 4NF
		nextstep = "9"
	else:
		#end of quiz
		nextstep = "11"
	html = """<form class="form" action="quiz.py" method="POST">
		"""
	html = html + "<p>Folgende Relationen sind entstanden:</p>"
	html = html + "<pre><h4 style=\"display:inline;\">"+views.schemaToString(relations, keysAndFDsMVDs, primarykeys)+"</h4></pre>"
	html = html + """<input type="hidden" value="
"""+relationString+"""" name="relation"></input>
		<input type="hidden" value="
"""+fdsString+"""" name="fds"></input>
		<input type="hidden" value="4NF" name="targetnf"></input>
		<input type="hidden" value="
"""+str(numberOfTries)+"""" name="numberOfTries"></input>
		<input type="hidden" value="
"""+str(numberOfSteps)+"""" name="numberOfSteps"></input>
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




def quizFinal(numberOfTries, numberOfSteps, relationString, fdsString):
	score = numberOfSteps*100 / numberOfTries
	foodScore = scoreToFood(score)
	headings = """
		<div id="heading1" style="visibility:hidden">Geschafft.</div>
		<div id="heading2" style="visibility:hidden">Deine Skills sind wie """ + foodScore[0] + """.</div>
""" 
	contents = """
		<div id="content1" style="visibility:hidden">Du hast für 
"""+str(numberOfSteps) + """ Schritte 
""" + str(numberOfTries) + """ Versuche gebraucht und somit einen Score von 
""" + str(score) + """% erreicht.</div>
		<div id="content2" style="visibility:hidden">
""" + str(score) + """% Fett.</div>
		<script>
		$(document).ready(function(){
			$('#content').html($('#content1').html());
			$('#heading').html($('#heading1').html());
		$('#dasquiz').on('click', function () {
			if ($('#heading').html() == $('#heading1').html()){
				$('#heading').html($('#heading2').html());
				$('#content').html($('#content2').html());
			}
			else{
				$('#heading').html($('#heading1').html());
				$('#content').html($('#content1').html());
			}
		}).change();
		}).change();
		</script>
"""
	progressBar = """<div class="progress">
  				<div class="progress-bar" role="progressbar" style="width: 
"""+str(score)+"""%;">
  				</div>	
			</div>
"""

	html = """<form class="form" action="index.py" method="POST">"""
	html = html + "<input type=\"hidden\" value=\""+relationString+"\" name=\"relation\"></input>"
	html = html + "<input type=\"hidden\" value=\""+fdsString+"\" name=\"fds\"></input>"
	html = html + """<div class="row">
		<div class="col-xs-3 pull-right">
		<br/>
		<a href="index.py" class="btn btn-default" role="button">Neu</a>
		<button id="submitbutton" name="mode" type="submit" class="btn btn-primary" value="showResults">Ergebnis anzeigen</button>
		</div>
		</div></form>"""
	return views.getJumbotron("<span id=\"heading\"></span>", "<p><span id=\"content\"></span></p><p>"+progressBar+"</p><p>" + html +"</p>") + headings + contents


def getFoodsFat():
	foodsFat = {
	"Butterschmalz": 100,
	"Speck": 89,
	"Butter": 83,
	"Nüsse": 71,
	"Weichkäse": 67,
	"Cheddar": 48,
	"Frischkäse": 44
	}
	return foodsFat

def scoreToFood(score):
	foodsFat = getFoodsFat()
	result = ("x",1000)
	for food, fat in foodsFat.iteritems():
		if score <= fat and fat-score < result[1]-score:
			result = (food, fat)
	return result

