#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import views
import DBnormalizer
form = cgi.FieldStorage()



def printResults(string):
	x = DBnormalizer.parseInput(string)
	if len(x)<3:
		return x[0]
	else:
		relation = x[0]
		fds = x[1]
		mvds = x[2]
		targetNf = x[3]
		keys, normalForms, newSchema = DBnormalizer.computeEverything(relation, fds, mvds, targetNf)
		return views.resultToString(relation, fds, mvds, keys, normalForms, targetNf, newSchema) 
	
print """
	<html>
		<head>
			<meta charset="utf-8">
			<title>DBnormalizer</title>
			<link rel="stylesheet" type="text/css" href="../../html-data/static/css/bootstrapcosmo.min.css" />
			<script src="../../html-data/static/js/jquery-1.11.3.min.js"></script>
			<script src="../../html-data/static/js/bootstrap.min.js"></script>
		</head>"""

def html(relation, fds, targetNfOptions):
	return  """
	<body>
	<div class="panel panel-default">
  	<div class="panel-body">
		<div class="row">
			<div class="col-md-6">
				<h1><big>DB->normalizer</big><sub><small>beta</small></sub></h1>
			</div>
			<div class="col-md-6">
				<p class="text-right"><button type="button" class="btn btn-primary btn-xs" data-toggle="modal" data-target="#helpModal">
		 			<span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span> Hilfe</button>
				</p>
			</div>
		</div>
		<br/>
		<br/>
		<div class="panel panel-default">
			<div class="panel-body">
			<span class="label label-success">DB-Fragen? DB fragen:</span> <a href="mailto:david.becher@mytum.de">david.becher@mytum.de</a>
			</div>
		</div>
		<br/>
		<form class="form" action="index.py" method="POST"> 
			<fieldset>
				<div class="form-group">
					<h4>Relation eingeben</h4>
					<input type="text" class="form-control" name="relation" value="
""" + relation+ """
"></input>
					<h4>FDs/MVDs eingeben</h4>
					<textarea type="text" class="form-control" rows="6" name="fds">
"""+ fds + """
</textarea>
					<h4>Ziel-Normalform auswählen</h4>
					 <select class="form-control" name="targetNf">
"""+targetNfOptions+"""
</select>
					<input type="hidden" value="showResults" name="mode"></input>
				</div>
				<div class="form-group">
						<button id="submitbutton" type="submit" class="btn btn-primary" value="send">Absenden</button>
				</div>
			</fieldset>				
		</form>
		<div class="col-xs-3">
		<form class="form" action="index.py" method="POST">
			<fieldset>
				<div class="form-group">
					<input type="hidden" value="generateFds" name="mode"></input>
					<button id="generateWithoutMvds" type="submit" class="btn btn-default" value="send">Generiere neues Schema (ohne MVDs)</button>
		   		</div>
			</fieldset>
		</form>
		</div>
		<div class="col-xs-3">
		<form class="form" action="index.py" method="POST">
	                <fieldset>
				<div class="form-group">
				        <input type="hidden" value="generateMvds" name="mode"></input>
				        <button id="generateWithMvds" type="submit" class="btn btn-default" value="send">Generiere neues Schema (mit MVDs)</button>
				</div>
	                </fieldset>
                </form>
		</div>
		</div>
		<br/>"""

htmlend="""	
	</div>
	</div>
		<!-- Modal: help -->
		<div id="helpModal" class="modal fade" role="dialog">
			<div class="modal-dialog">
			<!-- Modal content-->
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal">&times;</button>
					<h3 class="modal-title">Hilfe</h3>
				</div>
				<div class="modal-body">
					<p>Hier könnte ein hilfreicher Hilfetext oder ein informativer Informationstext stehen.</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-default" data-dismiss="modal">OK</button>
				</div>
			</div>
			</div>
		</div>
	</body>
</html>
"""


def targetNfOptions(targetNf):
	if (targetNf=="3NF"):
		option3NF = "<option selected>3NF</option>"
	else:
                option3NF = "<option>3NF</option>"
        if (targetNf=="BCNF"):
                optionBCNF = "<option selected>BCNF</option>"
        else:
                optionBCNF = "<option>BCNF</option>"
        if (targetNf=="4NF"):
                option4NF = "<option selected>4NF</option>"
        else:
                option4NF = "<option>4NF</option>"
	return option3NF+optionBCNF+option4NF

try:
	mode = form['mode'].value
	if mode=='generateFds':
		 relation, fds, mvds = DBnormalizer.generateNewProblem(5, False)
		 print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), targetNfOptions("3NF"))+htmlend
	elif mode=='generateMvds':
		 relation, fds, mvds = DBnormalizer.generateNewProblem(5, True)
		 print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), targetNfOptions("3NF"))+htmlend
	else:
		#Mode is showResults
		relation = str(form['relation'].value)
        	fds = str(form['fds'].value)
       	 	targetNf = form['targetNf'].value
		input = "["+relation+"]["+fds+"]["+targetNf+"]"
		print html(relation, fds, targetNfOptions(targetNf)) + printResults(input) + htmlend
except KeyError:
    relation, fds, mvds = DBnormalizer.generateNewProblem(5, False)
    print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), targetNfOptions("3NF"))+htmlend
