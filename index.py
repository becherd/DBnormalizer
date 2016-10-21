#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import views
import DBnormalizer
import quizForms
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
		result = DBnormalizer.computeEverything(relation, fds, mvds)
		return views.resultToString(relation, x[1], x[2], result) 


def printQuizStart(string):
	x = DBnormalizer.parseInput(string)
	if len(x)<3:
		return x[0]
	else:
		relation = x[0]
		fds = x[1][:]
		mvds = x[2][:]
		return quizForms.formQuizStart(relation, fds, mvds)


	
print """
	<html>
		<head>
			<meta charset="utf-8">
			<title>DBnormalizer</title>
			<link rel="stylesheet" type="text/css" href="http://home.in.tum.de/~becher/static/css/bootstrapcosmo.min.css" />
			<script src="http://home.in.tum.de/~becher/static/js/jquery-1.11.3.min.js"></script>
			<script src="http://home.in.tum.de/~becher/static/js/bootstrap.min.js"></script>
		</head>"""



def html(relation, fds, numberOfAttributes, funMode):
	attributesOptions = views.numberOfAttributesOptions(numberOfAttributes)
	if funMode==1:
		funModeURL="?fun=1"
		funModeAlert="""<div class="alert alert-info">
  <strong>Du befindest dich im Fun-Mode!</strong> Zu viel Fun?  <a href="./index.py" class="alert-link">Bring mich wieder zurück!</a>
</div>"""
	else:
		funModeURL=""
		funModeAlert=""
	return  htmlstart(funModeAlert) + """
		<form id="inputform" class="form" action="index.py"""+funModeURL+"""" method="POST"> 
				<div class="form-group">
					<h4>Relation eingeben</h4>
					<input type="text" class="form-control" id="relation" name="relation" value="
""" + relation+ """"></input>
					<h4>FDs/MVDs eingeben</h4>
					<textarea type="text" class="form-control" rows="6" id="fds" name="fds">
"""+ fds + """
</textarea>
					<input type="hidden" value="
"""+str(funMode)+"""" name="fun"></input>
					<input type="hidden" value="
"""+str(numberOfAttributes)+"""
" name="numberOfAttributes"></input>
					<input type="hidden" value="1" name="step"></input>
				</div>
				<div class="form-group">
						<button id="submitbutton" name="mode" type="submit" class="btn btn-default" value="showResults">Absenden</button>
						<button id="quizButton" name="mode" type="submit" class="btn btn-primary" value="quiz">Quiz</button>
						<div class="btn-group pull-right">					
						<button href="#" class="btn btn-default btn-sm dropdown-toggle" data-loading-text="Lädt..." data-toggle="dropdown" id="schemaDropdownButton">
							Schema laden
							<span class="caret"></span>
						</button>
						<ul class="dropdown-menu" id="schemaDropdown">
						</ul>
						</div>
				</div>			
		</form>
		<form class="form-inline" action="index.py"""+funModeURL+"""" method="POST">
				<div class="form-group">
				<h4>Neues Schema generieren</h4>
				Generiere neues Schema mit
				<select class="form-control input-sm" name="numberOfAttributes">
"""+attributesOptions+"""
</select> <input type="hidden" value="
"""+str(funMode)+"""" name="fun"></input>Attributen
			<button id="mode" name="mode" type="submit" class="btn btn-default btn-sm" value="generateFds">nur mit FDs</button>
			<button id="mode" name="mode"  type="submit" class="btn btn-default btn-sm" value="generateMvds">auch mit MVDs</button>	
		</div>
                </form>
		</div>
		<br/>"""


def htmlstart(funModeAlert = ""):
	return """<body>
	<div class="panel panel-default">
  	<div class="panel-body">
		<div class="row">
			<div class="col-md-6">
"""+views.getHeading()+"""</div>
			<div class="col-md-6">
				<p class="text-right"><button type="button" class="btn btn-primary btn-xs" data-toggle="modal" data-target="#helpModal">
		 			<span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span> Hilfe</button>
				</p>
			</div>
		</div>
"""+funModeAlert+"""
		<br/>
		<div class="panel panel-default">
			<div class="panel-body">
			<span class="label label-success">DB-Fragen? DB fragen:</span> <a href="mailto:david.becher@mytum.de">david.becher@mytum.de</a>
			</div>
		</div>
		<br/>
"""


htmlend="""
	</div>
	</div>
	<br/>
	<br/>	
	<br/>
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
					<p>
						<h4>Relationen und FDs/MVDs eingeben</h4>
						<p>Eine Relation kann z.B. als <code>ABCD</code> eingegeben werden, wobei dann jeder Buchstabe ein Attribut bezeichet (hier gäbe es Attribute A,B,C,D). Alternativ können auch längere Attributnamen verwendet werden, diese sind dann durch Kommata zu trennen, z.B. <code>AttributA,AttributB,AttributC</code></p>
						<p>FDs werden mittels <code>-></code> eingegeben, wobei links und rechts des Pfeils Attribute stehen können. Diese können wieder entweder ohne Kommata eingegeben werden (jeder Buchstabe ein Attribut, z.B. <code>ABC->D</code>), oder durch Kommata getrennt (z.B. <code>AttributA,AttributB->AttributC</code>). Wird kein Attribut angegeben, wird dies als leere Menge (&empty;) interpretiert.</p>
						<p>MVDs werden mittels <code>->></code> angegeben, ansonsten analog zu FDs
					</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-default" data-dismiss="modal">OK</button>
				</div>
			</div>
			</div>
		</div>

	<script>
		$(document).ready(function(){
   		 $('[data-toggle="tooltip"]').tooltip();   
		});
	</script>
	<script>
		$('[data-toggle="popover"]').each(function(){
   		 $(this).popover(
				{
				trigger: 'hover',
				container:$(this)
				}
			);   
		});
	</script>
	<script>
		$(document).ready(function(){
			$.get('predefinedSchemas.py', function(result) {
				$('#schemaDropdown').html(result.trim());
			});
			
		});
	</script>
	<script>
		function setContent(r){
			var btn = $('#schemaDropdownButton').button('loading');
			$.get('predefinedSchemas.py?schema='+r, function(result) {
				var schema = result.trim().split(";");
				$('#relation').val(schema[0]);
				$('#fds').val(schema.slice(1).join("\\n"));
				btn.button('reset');
			});
		}
	</script>
	</body>
</html>
"""


try:
	numberOfAttributes = form['numberOfAttributes'].value
except KeyError:
	numberOfAttributes = 5
try:
	mode = form['mode'].value
	try:
		funMode=int(form['fun'].value)
	except:
		funMode=0
	if mode=='generateFds':
		 relation, fds, mvds = DBnormalizer.generateNewProblem(numberOfAttributes, False, funMode)
		 print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), numberOfAttributes, funMode)+views.getAlgorithmTutorial() + htmlend
	elif mode=='generateMvds':
		 relation, fds, mvds = DBnormalizer.generateNewProblem(numberOfAttributes, True, funMode)
		 print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), numberOfAttributes, funMode)+views.getAlgorithmTutorial()+htmlend
	else:
		#Mode is showResults or Quiz
		relation = str(form['relation'].value)
		fds = str(form['fds'].value)
		input = "["+relation+"]["+fds+"]["+str(int(numberOfAttributes))+"]"
		if mode=='quiz':
			x = DBnormalizer.parseInput(input)
			if len(x)<3:
				print html(relation, fds, numberOfAttributes, funMode) +  printResults(input) + htmlend
			else:
				print htmlstart() + printQuizStart(input)+ htmlend
		else:
			print html(relation, fds, numberOfAttributes, funMode) + printResults(input) + htmlend
except KeyError:
	try:
		funMode=int(form['fun'].value)
	except:
		funMode=0
	relation, fds, mvds = DBnormalizer.generateNewProblem(numberOfAttributes, False, funMode)
	print html(views.setOfAttributesToString(relation), views.fdsToString(fds)+views.mvdsToString(mvds), 5, funMode)+ views.getAlgorithmTutorial() +htmlend
