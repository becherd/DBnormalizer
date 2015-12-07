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
		fds = x[1][:]
		mvds = x[2][:]
		numberOfAttributes = x[3]
		keys, normalForms, newSchema = DBnormalizer.computeEverything(relation, fds, mvds)
		return views.resultToString(relation, x[1], x[2], keys, normalForms, newSchema) 
	
print """
	<html>
		<head>
			<meta charset="utf-8">
			<title>DBnormalizer</title>
			<link rel="stylesheet" type="text/css" href="http://home.in.tum.de/~becher/static/css/bootstrapcosmo.min.css" />
			<script src="http://home.in.tum.de/~becher/static/js/jquery-1.11.3.min.js"></script>
			<script src="http://home.in.tum.de/~becher/static/js/bootstrap.min.js"></script>
		</head>"""

def html(relation, fds, numberOfAttributes):
	attributesOptions = views.numberOfAttributesOptions(numberOfAttributes)
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
				<div class="form-group">
					<h4>Relation eingeben</h4>
					<input type="text" class="form-control" name="relation" value="
""" + relation+ """
"></input>
					<h4>FDs/MVDs eingeben</h4>
					<textarea type="text" class="form-control" rows="6" name="fds">
"""+ fds + """
</textarea>
					<input type="hidden" value="showResults" name="mode"></input>
					<input type="hidden" value="
"""+str(numberOfAttributes)+"""
" name="numberOfAttributes"></input>
				</div>
				<div class="form-group">
						<button id="submitbutton" type="submit" class="btn btn-primary" value="send">Absenden</button>
				</div>			
		</form>
		<form class="form-inline" action="index.py" method="POST">
				<div class="form-group">
				<h4>Neues Schema generieren</h4>
				Generiere neues Schema mit
				<select class="form-control input-sm" name="numberOfAttributes">
"""+attributesOptions+"""
</select> Attributen
			<button id="mode" name="mode" type="submit" class="btn btn-default btn-sm" value="generateFds">ohne MVDs</button>
			<button id="mode" name="mode"  type="submit" class="btn btn-default btn-sm" value="generateMvds">mit MVDs</button>	
		</div>
                </form>
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





try:
	mode = form['mode'].value
	numberOfAttributes = form['numberOfAttributes'].value
	if mode=='generateFds':
		 relation, fds, mvds = DBnormalizer.generateNewProblem(numberOfAttributes, False)
		 print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), numberOfAttributes)+htmlend
	elif mode=='generateMvds':
		 relation, fds, mvds = DBnormalizer.generateNewProblem(numberOfAttributes, True)
		 print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), numberOfAttributes)+htmlend
	else:
		#Mode is showResults
		relation = str(form['relation'].value)
        	fds = str(form['fds'].value)
		input = "["+relation+"]["+fds+"]["+str(int(numberOfAttributes))+"]"
		print html(relation, fds, numberOfAttributes) + printResults(input) + htmlend
except KeyError:
    relation, fds, mvds = DBnormalizer.generateNewProblem(5, False)
    print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), 5)+htmlend
