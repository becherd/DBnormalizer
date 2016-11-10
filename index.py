#!/usr/bin/python
# -*- coding: utf8 -*-
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


print "Content-Type: text/html"	
print """
	<html>
		<head>
			<meta charset="utf-8">
			<title>DB->normalizer</title>
			<link rel="stylesheet" type="text/css" href="/becher/static/css/bootstrapcosmo.min.css" />
			<script src="/becher/static/js/jquery-1.11.3.min.js"></script>
			<script src="/becher/static/js/bootstrap.min.js"></script>
			<script src="/becher/static/js/js.cookie.js"></script>
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
"""+str(numberOfAttributes)+"""
" name="numberOfAttributes"></input>
					<input type="hidden" value="1" name="step"></input>
				</div>
				<div class="form-group">
						<button id="submitbutton" name="mode" type="submit" class="btn btn-default" value="showResults">Ergebnis anzeigen</button>
						<button id="quizButton" name="mode" type="submit" class="btn btn-primary" value="quiz">Quiz</button>
						<div class="pull-right dropup">					
						<a href="#" class="btn btn-default btn-sm" id="saveSchema" onclick="saveSchema();"><span class="glyphicon glyphicon-floppy-disk" aria-hidden="true"></span> Schema speichern</a>
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
</select> Attributen
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
			<div class="modal-dialog modal-lg">
			<!-- Modal content-->
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal">&times;</button>
					<h3 class="modal-title">Hilfe</h3>
				</div>
				<div class="modal-body">
					<p>
						<h4>Relation eingeben</h4>
						<p>Du kannst eine Relation eingeben, indem du Attribute in das obere Textfeld schreibst. Hier hast du zwei Möglichkeiten:
						<ul><li>Jeder Buchstabe ein Attribut: Wenn du die Attribute nicht durch Kommas trennst, bezeichnet jeder Buchstabe ein Attribut. <code>ABCD</code> bedeutet also, dass die Relation die Attribute <code>A</code>, <code>B</code>, <code>C</code> und <code>D</code> enthält.</li>
						<li>Lange Attributnamen: Du kannst auch längere Attributnamen verwenden, diese musst du dann durch Kommas trennen. Beispiel: <code>AttributA,AttributB,AttributC</code>
						</ul>	
						</p>
						<h4>FDs/MVDs eingeben</h4>
						<p>
						Abhängigkeiten kannst du ins untere Textfeld schreiben; verwende für jede Abhängigkeit eine neue Zeile. Verwende <code>-></code>, um eine FD bzw. <code>->></code>, um eine MVD einzugeben. Links und rechts vom Pfeil kannst du Attribute in der gleichen Form angeben wie oben in der Relation. Wenn du auf einer Seite kein Attribut angibst, wird dies als leere Menge (<code>&empty;</code>) interpretiert. 
						</p>
						<h4>Schema generieren</h4>
						<p>
						Du kannst ein neues, zufälliges Schema generieren, indem du die gewünschte Attributzahl über das Dropdown wählst und dann über Klick auf <span class="btn btn-default btn-xs">nur mit FDs</span> oder <span class="btn btn-default btn-xs">auch mit MVDs</span> entscheidest, ob im generierten Schema MVDs enthalten sein sollen oder nicht. Ein manuelles Neuladen der Webseite generiert immer ein Schema mit 5 Attributen ohne MVDs.
						</p>
						<h4>Schema speichern</h4>
						<p>
						Mit Klick auf <span class="btn btn-default btn-xs">Schema speichern</span> kannst du das aktuell eingegebene Schema speichern, um es später wieder laden zu können. Das Schema wird dabei als Cookie gespeichert; ist also verloren, wenn du die Cookies für diese Seite löschst.
						</p>
						<h4>Schema laden</h4>
						<p>
						Mit Klick auf <span class="btn btn-default btn-xs">Schema laden</span> kannst du deine gespeicherten Schemata laden. Zusätzlich sind auch GDB-Schemata hinterlegt; das sind Übungsaufgaben aus der GDB-Übung.
						</p>
						<h4>Ergebnis anzeigen</h4>
						<p>
						Mit Klick auf <span class="btn btn-default btn-xs">Ergebnis anzeigen</span> werden alle relevanten Eigenschaften des Schemas berechnet und das Schema anschließend in höhere Normalformen überführt. Es werden dabei von allen Algorithmen alle Zwischenschritte angezeigt. Es wird allerdings jeweils nur eine mögliche Lösung angezeigt, möglicherweise gibt es noch andere, richtige Lösungen.
						</p>
						<h4>Quiz</h4>
						<p>
						Mit Klick auf <span class="btn btn-default btn-xs">Quiz</span> kannst du das Quiz starten. Hier wirst du nacheinander alles abgefragt (Eigenschaften des Schemas sowie Überführung in höhere Normalformen) und bekommst nach jedem Schritt Feedback, ob deine Lösung richtig ist oder nicht. 
						</p>
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
		function addSchemaToList(id){
			$('#schemaDropdown').append("<li name='"+id+"'><a href='#'><span onclick='setContent(\\""+id+"\\")'>Schema "+id+"</span> <span class='glyphicon glyphicon-trash btn-xs' onclick='deleteSchema(\\""+id+"\\")'></span></a></li>");			
		}
		function appendDropdownHeader(){
			 $('#schemaDropdown').append("<span id='dropdownHeader'><li role='separator' class='divider'></li><li class='dropdown-header'>Meine Schemata</li></span>");
		}
		function removeDropdownHeader(){
			 $('#dropdownHeader').remove();
		}

		$(document).ready(function(){
                       //saved user schemas
                        savedSchemas = getSavedSchemas();
			if(Object.keys(savedSchemas).length > 0){
				appendDropdownHeader();
                       	}
			$.each(savedSchemas, function(id){
				addSchemaToList(id);
                       	});
			//predefined schemas
			$.get('predefinedSchemas.py', function(result) {
				$('#schemaDropdown').prepend(result.trim());
				$('#schemaDropdown').prepend("<li class='dropdown-header'>GDB Schemata</li>");
			});
		});

		function setContent(r){
			var btn = $('#schemaDropdownButton').button('loading');
                        if(r.match('^s.+')){
                                //predefined
                                $.get('predefinedSchemas.py?schema='+r, function(result) {
					var schema = result.trim().split(";");
					$('#relation').val(schema[0]);
                        		$('#fds').val(schema.slice(1).join("\\n"));
                        		btn.button('reset');
                                });
                        }
                        else{
                                //user-defined
                                var schema = Cookies.get(r).trim().split(";");
				$('#relation').val(schema[0]);
                                $('#fds').val(schema.slice(1).join("\\n"));
                                btn.button('reset');
                        }
		}

                function getSavedSchemas(){
                        var schemas = Cookies.get();
			var result = {};
			for(var s in schemas){
				if ($.isNumeric(s)){
					result[s] = schemas[s];
				}
			}
			return result;
                }
		var pathVisible = '/~becher';
                function saveSchema(){
                       schemas = getSavedSchemas();
			var newSchemaId = 1;
			if (Object.keys(schemas).length>0){
				var schemaIds = Object.keys(schemas);
	                       	newSchemaId = Math.max.apply(Math,schemaIds)+1;
			}
			else{
				appendDropdownHeader();
			}
			addSchemaToList(newSchemaId);
			Cookies.set(newSchemaId, $('#relation').val()+';'+$('#fds').val().replace('\\n', ';'), { expires: 180, path: pathVisible });
			alert('Schema gespeichert als "Schema '+newSchemaId+'"');
                }
		
		function deleteSchema(id){
			$('#schemaDropdown').find('li[name='+id+']').remove();
			Cookies.remove(id, { path: pathVisible });
			schemas = getSavedSchemas();
			if (Object.keys(schemas).length == 0){
				removeDropdownHeader();
			}
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
