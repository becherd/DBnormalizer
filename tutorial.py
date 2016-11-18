#!/usr/bin/python
# -*- coding: utf8 -*-
import cgi
import cgitb; cgitb.enable()
import views


print "Content-Type: text/html"	
print """
	<html>
		<head>
			<meta charset="utf-8">
			<title>DB->normalizer</title>
			<link rel="stylesheet" type="text/css" href="/becher/static/css/bootstrapcosmo.min.css" />
			<script src="/becher/static/js/jquery-1.11.3.min.js"></script>
			<script src="/becher/static/js/bootstrap.js"></script>
			<script src="/becher/static/js/js.cookie.js"></script>
		</head><body>
	<div class="panel panel-default">
  	<div class="panel-body">
			<div class="row">
			<div class="col-md-6">
"""+views.getHeading("Das Tutorial")+"""</div>
			</div>
		<br/>
		<div class="panel panel-default">
			<div class="panel-body">
			<span class="label label-success">DB-Fragen? DB fragen:</span> <a href="mailto:david.becher@mytum.de">david.becher@mytum.de</a>
			</div>
		</div>
		<br/>

		<h1>Tutorial</h1>
		<p>Gegeben ist immer ein Schema bestehend aus den Attributen der Relation und den Funktionalen Abhängigkeiten (FDs) bzw. Mehrwertigen Abhängigkeiten (MVDs).</p>
		<p>Beispiel:
		<div class="well well-lg">
		  R:={ABCDE}
		</div>
		<div class="well well-lg">
			AB->C<br/>
			B->DA<br/>
			D->AC<br/>
			B->C<br/>
			C->>A<br/>
		</div>
		</p>
<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="keys">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseKeys" aria-expanded="false" aria-controls="collapseKeys">
          Schlüsselbestimmung
        </a>
      </h4>
    </div>
    <div id="collapseKeys" class="panel-collapse collapse" role="tabpanel" aria-labelledby="keys">
      <div class="panel-body">
		<h1>Schlüsselbestimmung</h1>
		<p>Zunächst müssen wir alle Kandidatenschlüssel bestimmen, das sind alle Mengen von Attributen, die minimal sind und mithilfe denen sich alle anderen Attribute über die FDs erreichen lassen. Am einfachsten ist es, erstmal alle Attribute zu finden, die nirgendwo rechts stehen. Alle diese Attribute müssen auf jeden Fall in jeden Schlüssel. Wir betrachten das Schema von oben: hier tauchen die Attribute <code>B</code> und <code>E</code> nirgendwo rechts auf. Achtung, vergiss hier nicht das Attribut <code>E</code>! Das Attribut <code>E</code> kommt nämlich in keiner FD irgendwo vor und wird somit oft fälschlicherweise übersehen.
		</p>
		<p>
		Jetzt schauen wir, ob <code>BE</code> tatsächlich ein Schlüssel ist. Durch die zweite FD erreichen wir <code>DA</code> von <code>B</code> aus, über alle anderen FDs danach auch noch das <code>C</code>, womit wir alle Attribute entweder vorher schon hatten oder über die FDs erreichen konnten. Aber pass auf, es muss nicht unbedingt so sein, dass alles, was rechts nirgendwo steht, auch der Schlüssel ist; möglicherweise reicht das nicht aus, um alles andere zu erreichen. In diesem Fall muss man dann schauen, welche Attribute noch hinzugefügt werden müssen, damit man alles erreichen kann. Auch mehrere Kandidatenschlüssel sind möglich. Außerdem wichtig: MVDs werden bei der Schlüsselbestimmung komplett ignoriert; nur die FDs müssen hier betrachtet werden.
		</p>	
		<p>
		Wir wissen jetzt also, dass wir genau einen Kandidatenschlüssel haben, nämlich
		<div class="well well-lg">
		  {BE}
		</div>
		</p>
		<br/>
		<a class="btn btn-primary" data-toggle="collapse" data-parent="#accordion" href="#collapseNormalForm" aria-expanded="false" aria-controls="collapseNormalForm">
		  Ok, weiter
		</a>	
      </div>
    </div>
  </div>
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="normalForm">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseNormalForm" aria-expanded="false" aria-controls="collapseNormalForm">
          Normalform bestimmen
        </a>
      </h4>
    </div>
    <div id="collapseNormalForm" class="panel-collapse collapse" role="tabpanel" aria-labelledby="normalForm">
      <div class="panel-body">
		<h1>Normalform bestimmen</h1>
		<p>Als nächstes bestimmen wir die höchste Normalform, in der sich die Relation befindet. Ein Schema ist in einer bestimmten Normalform, wenn entsprechende Bedingungen vom Schema erfüllt werden.
		</p>
		<h3>1NF</h3>
		<p>
Wir fangen bei der ersten Normalform (1NF) an:
		</p>
		<p>
		<div class="panel panel-default">
		  <div class="panel-heading">Das Schema ist in 1NF, wenn...</div>
		  <div class="panel-body">
		    ...alle Attribute atomar sind.
		  </div>
		</div>
		</p>
		<p>
		Das heißt, dass jedes Attribut <i>einen</i> Wert (und keine Liste/Menge von Werten) enthalten muss. Das ist bei uns (wenn nicht explizit anders angegeben) immer erfüllt. Die erste Normalform ist also auch für das obige Schema erfüllt:
		</p>
		<p>
		<div class="well well-lg">
		  <span class="label label-success">1NF <span class="glyphicon glyphicon-ok" aria-hidden="ok"></span></span>
		</div>
		</p>
		<h3>2NF</h3>
		<p>Die 1NF ist erfüllt, also überprüfen wir als nächstes die 2NF. Die ist nicht ganz so trivial:
		</p>
		<p>
		<div class="panel panel-default">
		  <div class="panel-heading">Das Schema ist in 2NF, wenn...</div>
		  <div class="panel-body">
		    ...es in 1NF ist und für jedes Attribut <code>b</code> auf der rechten Seite gilt:
		<ol>
			<li><code>b</code> ist Teil eines Kandidatenschlüssels <b>oder</b></li>
			<li><code>b</code> ist nicht von einer echten Teilmenge eines Kandidatenschlüssels abhängig</li>
		</ol>
		  </div>
		</div>
		</p>
		<p>
		Wir müssen jetzt also jede rechte Seite von jeder FD anschauen. Wenn wir ein Attribut rechts finden, das keine der beiden Bedingungen erfüllt, ist das Schema nicht in 2NF. 
		</p>
		<p>
		Also schauen wir uns mal die erste FD
		</p>
		<p>
		<div class="well well-lg">
		  AB->C
		</div>
		</p>
		<p>
		an. <code>C</code> (das einzige Attribut rechts) ist nicht Teil eines Kandidatenschlüssels (Bedingung 1), es ist aber auch nicht von einer echten Teilmenge eines Kandidatenschlüssels abhängig. <code>AB</code> ist nämlich keine echte Teilmenge unseres einzigen Kandidatenschlüssels <code>BE</code>, somit ist die zweite Bedingung erfüllt und die erste FD verletzt somit nicht die 2NF. Also machen wir weiter und betrachten die zweite FD
		</p>
		<p>
		<div class="well well-lg">
		  B->DA
		</div>
		</p>
		<p>
		  Schauen wir uns das erste Attribut rechts (<code>D</code>) an. <code>D</code> ist auch kein Teil eines Kandidatenschlüssels, ist aber abhängig von einer echten Teilmenge unseres Kandidatenschlüssels (<code>B</code> ist echte Teilmenge von <code>BE</code>). Hier ist also auch die zweite Bedingung verletzt, somit haben wir schon eine "böse" FD gefunden; wir können also direkt aufhören und sagen: die 2NF ist nicht erfüllt:
		</p>
		<p>
		<div class="well well-lg">
		<span class="label label-danger">2NF <span class="glyphicon glyphicon-flash" aria-hidden="flash"></span></span>
		</div>
		</p>
		<p>
		Da eine höhere Normalform alle niedrigeren Normalformen mit einschließt, können wir jetzt komplett aufhören und müssen gar nicht mehr die 3NF, BCNF und 4NF überprüfen. Heißt: wenn ein Schema nicht in 2NF ist, dann kann es auch nicht in 3NF usw. sein. Die höchste Normalform ist also für unser Beispiel die erste Normalform:
		</p>
		<p>
		<div class="well well-lg">
		  <span class="label label-success">1NF <span class="glyphicon glyphicon-ok" aria-hidden="ok"></span></span>
		</div>
		</p>
		<p>
			Wir schauen uns aber trotzdem noch die anderen Normalformen an. Hier wäre das wie beschrieben nicht nötig, weil wir schon wissen, dass die nicht erfüllt sind, aber sonst käm das ja gar nicht im Tutorial vor ;)
		</p>
		<h3>3NF</h3>
		<p>Hier also die Bedingungen für die 3NF:
		</p>
		<p>
		<div class="panel panel-default">
		  <div class="panel-heading">Das Schema ist in 3NF, wenn...</div>
		  <div class="panel-body">
		    ...jede FD <code>&#x3b1;->&#x3b2;</code> mindestens eine der folgenden Bedingungen erfüllt:
			<ol>
				<li><code>&#x3b1;->&#x3b2;</code> ist trivial (&#x3b2;&#x2286;&#x3b1;)</li>
				<li><code>&#x3b1;</code> ist Superschlüssel</li>
				<li>Jedes Attribut in <code>&#x3b2;</code> ist in einem Kandidatenschlüssel enthalten</li>
			</ol>
		  </div>
		</div>
		</p>
		<p>
			Offensichtlich ist z.B. die erste FD nicht in 3NF: <code>AB->C</code> ist weder trivial, noch steht links ein Superschlüssel, noch ist das <code>C</code> auf der rechten Seite in einem Kandidatenschlüssel enthalten. Wir können hier also schon aufhören und sagen: 3NF ist nicht erfüllt. In diesem Beispiel ist es sogar so, dass keine der FDs die Bedingungen für die 3NF erfüllen würde. Also ganz klar (was wir auch schon vorher wussten):
		</p>
		<p>
		<div class="well well-lg">
		  <span class="label label-danger">3NF <span class="glyphicon glyphicon-flash" aria-hidden="flash"></span></span>
		</div>
		</p>
		<h3>BCNF</h3>
		<p>Wenn wir die BCNF überprüfen wollen würden, dann würden wir folgendes checken:
		</p>
		<p>
		<div class="panel panel-default">
		  <div class="panel-heading">Das Schema ist in BCNF, wenn...</div>
		  <div class="panel-body">
		    ...jede FD <code>&#x3b1;->&#x3b2;</code> mindestens eine der folgenden Bedingungen erfüllt:
			<ol>
				<li><code>&#x3b1;->&#x3b2;</code> ist trivial (&#x3b2;&#x2286;&#x3b1;)</li>
				<li><code>&#x3b1;</code> ist Superschlüssel</li>
			</ol>
		  </div>
		</div>
		</p>
		<p>
			Man sieht sofort, dass im Vergleich zur 3NF nur die letzte Bedingung verschwunden ist. Man kann also 3NF und BCNF gleichzeitig prüfen: Wenn ein Schema in 3NF ist, aber man mal die dritte Bedingung "nutzen" muss, weiß man direkt, dass es zwar in 3NF ist, aber nicht in BCNF. Unser Beispiel war ja schon eh nicht in 3NF und deshalb schon lange nicht in BCNF. Sieht man natürlich auch an den Bedingungen der BCNF; keine der FDs erfüllt irgendeine davon.
		</p>
		<p>
		<div class="well well-lg">
		  <span class="label label-danger">BCNF <span class="glyphicon glyphicon-flash" aria-hidden="flash"></span></span>
		</div>
		</p>
		<h3>4NF</h3>
		<p>Für die 4NF betrachten wir erstmals auch zusätzlich die MVDs. Ansonsten sind die Bedingungen quasi die selben wie bei der BCNF:
		</p>
		<p>
		<div class="panel panel-default">
		  <div class="panel-heading">Das Schema ist in 4NF, wenn...</div>
		  <div class="panel-body">
		    ...jede MVD <code>&#x3b1;->>&#x3b2;</code> mindestens eine der folgenden Bedingungen erfüllt:
			<ol>
				<li><code>&#x3b1;->>&#x3b2;</code> ist trivial (&#x3b2;&#x2286;&#x3b1; oder &#x3b1;&#x222a;&#x3b2; = R)</li>
				<li><code>&#x3b1;</code> ist Superschlüssel</li>
			</ol>
		  </div>
		</div>
		</p>
		<p>Da jede FD auch eine MVD ist, kann ein Schema, das nicht in BCNF ist, auch nicht in 4NF sein. In unserem Beispiel stellen wir uns jetzt alle FDs als MVDs vor und sehen schon (wie vorher), dass z.B. die erste MVD <code>AB->>C</code> keine der Bedingungen erfüllt. Es ist sogar so, dass nichtmal <i>eine</i> MVD (also wie vorher keine der FDs und auch nicht die "reine" MVD <code>C->>A</code>) eine der Bedingungen erfüllt. Zu beachten ist, dass für MVDs eine leicht andere Definition von <i>trivial</i> gilt. Wir wussten es zwar schon vorher, aber haben jetzt nochmal gesehen:
		</p>
		<p>
		<div class="well well-lg">
		  <span class="label label-danger">4NF <span class="glyphicon glyphicon-flash" aria-hidden="flash"></span></span>
		</div>
		</p>
		<br/>
		<a class="btn btn-primary" data-toggle="collapse" data-parent="#accordion" href="#collapseCanonicalCover" aria-expanded="false" aria-controls="collapseCanonicalCover">
		  Ok, weiter
		</a>
      </div>
    </div>
  </div>
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="canonicalCover">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseCanonicalCover" aria-expanded="false" aria-controls="collapseCanonicalCover">
          Kanonische Überdeckung
        </a>
      </h4>
    </div>
    <div id="collapseCanonicalCover" class="panel-collapse collapse" role="tabpanel" aria-labelledby="canonicalCover">
      <div class="panel-body">
		<h1>Kanonische Überdeckung</h1>
		<p>Wir wollen nun die Kanonische Überdeckung der gegebenen FDs ermitteln. Die Kanonische Überdeckung ist äquivalent zu den ursprünglichen FDs, ist aber im Gegensatz zu den ursprünglichen FDs in jedem Fall minimal (d.h. es gibt keine "Redundanzen" mehr). Zur Bestimmung der Kanonischen Überdeckung müssen vier Schritte nacheinander durchgeführt werden:
		</p>
		<h3>Linksreduktion</h3>
		<p>Als erstes schauen wir, welche Attribute wir auf den linken Seiten weglassen können, ohne die Aussage der FDs zu verändern. In unserem Beispiel können wir - wen überhaupt - nur die erste FD linksreduzieren; bei allen anderen FDs steht links nur ein Attribut. Würden wir da was weglassen stünde links die leere Menge und die Aussage der FD wäre komplett anders als vorher. Und das wollen wir nicht.
		</p>
		<p>
		Wir betrachten also die erste FD
		</p>
		<p>
		<div class="well well-lg">
                  AB->C
                </div>
		</p>
		<p>
		  Erste Frage lautet jetzt also: "<i>Kann ich A weglassen?</i>". Anders formuliert: "<i>Komme ich mit dem Rest trotzdem zur kompletten rechten Seite?</i>". Die Antwort: Ja, weil man kommt auch nur mit dem <code>B</code> zum <code>C</code>, sogar über zwei verschiedene Wege:
		  <ol>
			<li>ganz einfach über die letzte FD <code>B->C</code></li>
			<li>oder mithilfe der zweiten FD <code>B->DA</code>: Mit dem <code>B</code> bekomme ich das <code>A</code>, dann habe ich <code>AB</code> und kann wieder die erste FD gehen, um das <code>C</code> zu bekommen.
		  </ol>
		Hier haben wir jetzt zwei Wege, einer reicht aber aus. Wir können also <code>A</code> weglassen, weil wir auch nur mit dem <code>B</code> zum <code>C</code> kommen. <code>B</code> können wir natürlich nicht auch noch weglassen, dann hätten wir nämlich eine leere linke Seite.
		</p>
		<p>
			Die FDs sehen nach der Linksreduktion also so aus:
		</p>
		<p>
		<div class="well well-lg">
                        B->C<br/>
                        B->DA<br/>
                        D->AC<br/>
                        B->C<br/>
                </div>
		</p>
		<h3>Rechtsreduktion</h3>
		<p>
			Natürlich kommt nach der Links- auch eine Rechtsreduktion. Die funktioniert im Prinzip gleich. Auch hier fragen wir uns für jedes Attribut rechts, ob wir dieses Attribut weglassen können, ohne die Aussage der FDs zu verändern. Im Gegensatz zur Linksreduktion muss man hier wirklich alle Attribute rechts betrachten; hier ist es durchaus möglich (und erlaubt), dass rechts eine leere Menge entsteht.
		</p>
		<p>
			Wir betrachten also die erste FD aus der  Linksreduktion
		</p>
		<p>
		<div class="well well-lg">
                        B->C<br/>
                </div>
                </p>
		<p>
			und fragen uns: "<i>Kann ich C weglassen?</i>". Also: "<i>Komme ich mit dem B sonst noch irgendwie zum C?</i>". Die Antwort ist: Ja, klar, zum Beispiel über die letzte FD. Also lassen wir das <code>C</code> rechts weg und unsere FDs sehen jetzt so aus:
		</p>
		<p>
                <div class="well well-lg">
                        B->&empty;<br/>
                        B->DA<br/>
                        D->AC<br/>
                        B->C<br/>
                </div>
                </p>
		<p>
			Nächste Frage: "<i>Kann ich in der zweiten FD das D weglassen?</i>". Natürlich nicht, man sieht nämlich sofort, dass rechts nirgendwo sonst ein <code>D</code> steht. Wie sollen wir dann sonst irgendwie anders da hin kommen? <code>D</code> bleibt also. Was ist mit dem <code>A</code> in der zweiten FD, können wir das wegreduzieren? Die Antwort ist: Ja! Es gibt nämlich noch einen anderen Weg, um vom <code>B</code> zum <code>A</code> zu kommen, nämlich über die dritte FD: mit dem <code>B</code> haben wir ja das <code>D</code> (zweite FD), und mit dem <code>D</code> erreichen wir das <code>A</code> (dritte FD). Aktuell sehen unsere FDs also so aus:
		</p>
		<p>
                <div class="well well-lg">
                        B->&empty;<br/>
                        B->D<br/>
                        D->AC<br/>
                        B->C<br/>
                </div>
                </p>
		<p>
			Bei der dritten FD kann nichts rechtsreduziert werden, bei der letzten FD können wir das <code>C</code> weglassen. Die Begründungen seien dem Leser überlassen :). Wir haben nach der Rechtsreduktion also diese FDs:
		</p>
		<p>
                <div class="well well-lg">
                        B->&empty;<br/>
                        B->D<br/>
                        D->AC<br/>
                        B->&empty;<br/>
                </div>
                </p>
		<h3>&alpha;&rarr;&empty; entfernen</h3>
		<p>Der dritte Schritt ist einfach: Wir löschen alle FDs, bei denen die rechte Seite leer ist. Übrig bleiben also:
		</p>
                <p>
                <div class="well well-lg">
                        B->D<br/>
                        D->AC<br/>
                </div>
                </p>
		<h3>FDs zusammenfassen</h3>
		<p>
			Im letzten Schritt müssen wir FDs, die die gleiche linke Seite haben, zusammenfassen. Diesen Fall haben wir hier nicht, also sind wir fertig. Zusammenfassen heißt: Wenn wir z.B. die FDs <code>A->BC</code> und <code>A->E</code> hätten, würden wir diese zu <code>A->BCE</code> zusammenfassen.
		<p>
		<p>
			Wir haben jetzt also die Kanonische Überdeckung unserer Beispiel-FDs bestimmt, nämlich
		</p>
                <p>
                <div class="well well-lg">
                        B->D<br/>
                        D->AC<br/>
                </div>
                </p>
		<a class="btn btn-primary" data-toggle="collapse" data-parent="#accordion" href="#collapseSyntheseAlgorithm" aria-expanded="false" aria-controls="collapseSyntheseAlgorithm">
                  Ok, weiter
                </a> 
      </div>
    </div>
  </div>
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="syntheseAlgorithm">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseSyntheseAlgorithm" aria-expanded="false" aria-controls="collapseSyntheseAlgorithm">
          Synthesealgorithmus
        </a>
      </h4>
    </div>
    <div id="collapseSyntheseAlgorithm" class="panel-collapse collapse" role="tabpanel" aria-labelledby="syntheseAlgorithm">
      <div class="panel-body">
                <h1>Synthesealgorithmus</h1>
                <p>
		Mit dem Synthesealgorithmus können wir jedes beliebige Schema verlustlos und abhängigkeitsbewahrend in die 3NF überführen. Da unser Beispiel-Schema nur in der 1NF ist, machen wir das natürlich! Auch hier sind vier Schritte notwendig: 
                </p>
		<h3>Kanonische Überdeckung bestimmen</h3>
		<p>
			Das haben wir gerade schon erledigt :). Zur Erinnerung, die kanonische Überdeckung für unser Beispiel ist
                </p>
		<p>
                <div class="well well-lg">
                        B->D<br/>
                        D->AC<br/>
                </div>
                </p>
		<h3>Relationsschemata formen</h3>
		<p>
			Da unsere Relation nicht in 3NF ist, müssen wir diese in mehrere kleinere Relationen aufteilen, die dann jeweils in 3NF sein sollen. Zunächst entsteht aus jeder FD der kanonischen Überdeckung eine neue Relation, indem wir alle Attribute einer FD in eine Relation packen. Wir erhalten also zwei Relationen:
		</p>
		<p>
                <div class="well well-lg">
                        R<sub>1</sub>:={BD}<br/>
                        R<sub>2</sub>:={ACD}<br/>
                </div>
                </p>
		<h3>Schema mit Schlüssel hinzufügen</h3>
		<p>
			Wenn keiner der Kandidatenschlüssel der ursprünglichen Relation in irgend einem der neuen Relationen enthalten ist, müssen wir nochmal eine neue Relation hinzufügen, die die Attribute von irgend einem Kandidatenschlüssel enthält (da sucht man sich dann einfach einen aus; niemals alle Kandidatenschlüssel hinzufügen!). Unser (einziger) Kandidatenschlüssel <code>BE</code> ist weder in <code>R<sub>1</sub></code> noch in <code>R<sub>2</sub></code> enthalten, somit fügen wir ein neues Schema <code>R<sub>3</sub></code> hinzu:
		</p>
                <p>
                <div class="well well-lg">
                        R<sub>1</sub>:={BD}<br/>
                        R<sub>2</sub>:={ACD}<br/>
			R<sub>3</sub>:={BE}<br/>
                </div>
                </p>
		<h3>Redundante Schemata eliminieren</h3>
		<p>
			Wenn ein Schema in einem anderen komplett enthalten ist, dann können wir das "kleinere" Schema entfernen. Diesen Fall haben wir hier nicht. Kurz ein Beispiel, wo man ein Schema eliminieren müsste: Wenn wir <code>R<sub>1</sub>:={ABD}</code> und <code>R<sub>2</sub>:={AB}</code> hätten, würden wir <code>R<sub>2</sub></code> streichen.
		</p>
		<p>
			Unser Schema in 3NF besteht also aus den drei Relationen
		</p>
		<p>
                <div class="well well-lg">
                        R<sub>1</sub>:={BD}<br/>
                        R<sub>2</sub>:={ACD}<br/>
                        R<sub>3</sub>:={BE}<br/>
                </div>
                </p>
		<h3>Schlüssel bestimmen</h3>
		<p>
			Wir wollen jetzt noch für jede neue Relation einen Primärschlüssel bestimmen und unterstreichen. Dazu müssen wir erstmal für jede Relation schauen, welche FDs in dieser Relation gelten. Zum Beispiel:
		</p>
		<p>
                <div class="well well-lg">
                        In R<sub>1</sub>:={BD} gilt:<br/>
			B->D<br/>
                </div>
                </p>
		<p>
			Hier gilt <code>B->D</code>. Dies ist genau die erste FD der kanonischen Überdeckung (bzw. ein Teil der zweiten FD des ursprünglichen Schemas. Die FD <code>B->DA</code> ist nämlich nichts anderes als <code>B->D</code> und <code>B->A</code>. <code>B->A</code> gilt natürlich nicht, aber <code>B->D</code> offensichtlich schon).
		</p>
		<p>
			Jetzt haben wir eine Relation mit FDs und können ganz normal wie <a data-toggle="collapse" data-parent="#accordion" href="#collapseKeys"  aria-expanded="false" aria-controls="collapseKeys">oben</a> die (Kandidaten-)Schlüssel bestimmen. <code>R<sub>1</sub></code> hätte hier den (einzigen) Kandidatenschlüssel <code>B</code>, den wir dann auch als Primärschlüssel wählen und entsprechend unterstreichen. Die Herleitung aller (Kandidaten-)Schlüssel der anderen beiden Relationen sei dem Leser überlassen. Hier das Endergebnis:
		</p>
		<p>
                <div class="well well-lg">
                        R<sub>1</sub>:={<u>B</u>D}<br/>
                        R<sub>2</sub>:={AC<u>D</u>}<br/>
                        R<sub>3</sub>:={<u>BE</u>}<br/>
                </div>
                </p>
		<br/>
                <a class="btn btn-primary" data-toggle="collapse" data-parent="#accordion" href="#collapseDecompositionAlgorithmBCNF" aria-expanded="false" aria-controls="collapseDecompositionAlgorithmBCNF">
                  Ok, weiter
                </a>    
      </div>
    </div>
  </div>
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="decompositionAlgorithmBCNF">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseDecompositionAlgorithmBCNF" aria-expanded="false" aria-controls="collapseDecompositionAlgorithmBCNF">
          Dekompositionsalgorithmus für BCNF
        </a>
      </h4>
    </div>
    <div id="collapseDecompositionAlgorithmBCNF" class="panel-collapse collapse" role="tabpanel" aria-labelledby="decompositionAlgorithmBCNF">
      <div class="panel-body">
		<h1>Dekompositionsalgorithmus für BCNF</h1>
		<p>
			Mit dem Dekompositionsalgorithmus kann man ein Schema verlustlos (aber nicht unbedingt abhängigkeitsbewahrend!) in die BCNF überführen. Dazu sucht man sich eine FD, die die BCNF verletzt, und teilt die Relation <code>R<sub>i</sub></code> anhand dieser FD (bezeichnen wir die FD mal als <code>&#x3b1;->&#x3b2;</code>) in zwei neue Relationen folgendermaßen auf:
		</p>
		<p>
		<div class="well well-lg">
			R<sub>i1</sub> = &#x3b1; &#x222a; &#x3b2;  <br/>
			R<sub>i2</sub> = R<sub>i</sub> - &#x3b2; <br/>
		</div>
		</p>
		<p>
 		Für diese neuen Relationen überprüft man wiederum die Normalform und teilt sie wieder auf, sofern sie nicht in BCNF sind.
		</p>
			In unserem Beispiel verletzt z.B. die erste FD <code>AB->C</code> die BCNF (weder trivial noch steht links ein Superschlüssel). Wir wählen diese FD und spalten die Relation folgendermaßen auf: 
		</p>
		<p>
		<div class="well well-lg">
				R<sub>1</sub>:= {ABC}<br/>
				R<sub>2</sub>:= {ABDE}<br/>
		</div>
		</p>
		<p>
			Die erste Relation erfüllt die BCNF (warum?), sodass wir die nicht weiter aufteilen müssen. In der zweiten Relation ist das aber nicht der Fall: hier verletzt z.B. die FD <code>B->DA</code> die BCNF (Kandidatenschlüssel in <code>R<sub>2</sub></code> ist <code>BE</code>, links steht also kein Superschlüssel und trivial ist die FD auch nicht). Also teilen wir  <code>R<sub>2</sub></code> anhand von <code>B->DA</code> folgendermaßen auf:
		</p>
		<p>
		<div class="well well-lg">
				R<sub>21</sub>:= {ABD}<br/>
				R<sub>22</sub>:= {BE}<br/>
		</div>
		</p>
		<p>
			Jetzt schauen wir wieder ob die Relationen in BCNF sind. In der zweiten Relation gilt keine FD, also kann auch keine FD die BCNF verletzen, also das passt. <code>R<sub>21</sub></code> ist allerdings noch nicht in BCNF. In <code>R<sub>21</sub></code> gelten nämlich die FDs
		</p>
		<p>
		<div class="well well-lg">
			B->DA<br/>
			D->A
		</div>
		</p>
		<p>
			Kandidatenschlüssel ist also <code>B</code>, somit ist die erste FD okay (links Superschlüssel), die zweite aber nicht (links kein Superschlüssel, und nicht trivial). Also teilen wir <code>R<sub>21</sub></code> wieder auf. Das Ergebnis ist dann
		</p>
		<p>
		<div class="well well-lg">
				R<sub>211</sub>:= {AD}<br/>
				R<sub>212</sub>:= {BD}<br/>
		</div>
		</p>
		<p>
			Jetzt sind wir fertig, beide Relationen sind in BCNF. Das Gesamtergebnis (also das komplette Schema in BCNF) ist also:
		</p>
		<p>
		<div class="well well-lg">
				R<sub>1</sub>:= {A<u>B</u>C}<br/>
				R<sub>22</sub>:= {<u>BE</u>}<br/>
				R<sub>211</sub>:= {A<u>D</u>}<br/>
				R<sub>212</sub>:= {<u>B</u>D}<br/>
		</div>
		</p>		
		<br/>
		<a class="btn btn-primary" data-toggle="collapse" data-parent="#accordion" href="#collapseDecompositionAlgorithm4NF" aria-expanded="false" aria-controls="collapseDecompositionAlgorithm4NF">
		  Ok, weiter
		</a>	
      </div>
    </div>
  </div>
  <div class="panel panel-default">
    <div class="panel-heading" role="tab" id="decompositionAlgorithm4NF">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseDecompositionAlgorithm4NF" aria-expanded="false" aria-controls="collapseDecompositionAlgorithm4NF">
          Dekompositionsalgorithmus für 4NF
        </a>
      </h4>
    </div>
    <div id="collapseDecompositionAlgorithm4NF" class="panel-collapse collapse" role="tabpanel" aria-labelledby="decompositionAlgorithm4NF">
      <div class="panel-body">
		<h1>Dekompositionsalgorithmus für 4NF</h1>
		<p>
			Der Dekompositionsalgorithmus für 4NF ist im Prinzip genau gleich wie der für BCNF, nur dass man jetzt eben MVDs statt FDs betrachtet (d.h. man denkt sich die FDs als MVDs und nimmt noch die "reinen" MVDs (im Beispiel <code>C->>A</code>) hinzu). Am Ende kommt in unserem Beispiel fast das gleiche Schema wie oben für BCNF raus, mit einem Unterschied: in <code>R<sub>1</sub></code> gilt ja die MVD, die wir jetzt neu betrachten (<code>C->>A</code>), und die ist in der Relation weder trivial noch steht links ein Superschlüssel. Im Gegensatz zu vorher sind wir hier also nicht fertig, sondern müssen <code>R<sub>1</sub></code> nochmal anhand <code>C->>A</code> splitten. Es entstehen die Relationen
		</p>	
		<p>
		<div class="well well-lg">
				R<sub>11</sub>:= {AC}<br/>
				R<sub>12</sub>:= {BC}<br/>
		</div>
		</p>
		<p>
			In <code>R<sub>11</sub></code> gilt nur die MVD <code>C->>A</code>, somit ist der Kandidatenschlüssel <code>AC</code>. Die linke Seite ist also kein Superschlüssel, aber die MVD ist trivial (schau nochmal die geänderte Definition für "triviale MVDs" im Vergleich zu "triviale FDs" an!). Also ist <code>R<sub>11</sub></code> okay. <code>R<sub>12</sub></code> ist auch okay, da gilt nur <code>B->C</code>, also erfüllt diese FD (bzw. hier im Kontext diese MVD) sogar beide Bedingungen: links steht ein Superschlüssel (sogar der Kandidatenschlüssel selbst), und die MVD ist auch trivial. 
		</p>
		<p>
			Wichtig bei der Suche nach den geltenden MVDs für eine Relation ist auch folgendes: eine MVD lässt sich (im Gegensatz zur FD) <b>nicht</b> anhand der rechten Seite aufteilen. Die MVD <code>A->>BC</code> ist also <b>nicht</b> das selbe wie <code>A->>B</code> und <code>A->>C</code>!
		</p>
		<p>Alle anderen Aufspaltungen sind wie oben bei der Transformation in BCNF, das Endergebnis in 4NF ist also:</p>
		<p>
		<div class="well well-lg">
				R<sub>11</sub>:= {<u>AC</u>}<br/>
				R<sub>12</sub>:= {<u>B</u>C}<br/>
				R<sub>22</sub>:= {<u>BE</u>}<br/>
				R<sub>211</sub>:= {A<u>D</u>}<br/>
				R<sub>212</sub>:= {<u>B</u>D}<br/>
		</div>
		</p>
		<br/>
		<a class="btn btn-primary" data-toggle="collapse" data-parent="#accordion" href="#collapseUsusEstMagisterOptimus" aria-expanded="false" aria-controls="collapseUsusEstMagisterOptimus">
		  Ok, weiter
		</a>				
      </div>
    </div>
  </div>
<div class="panel panel-default">
    <div class="panel-heading" role="tab" id="ususEstMagisterOptimus">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseUsusEstMagisterOptimus" aria-expanded="false" aria-controls="collapseUsusEstMagisterOptimus">
          Jetzt nur noch üben
        </a>
      </h4>
    </div>
    <div id="collapseUsusEstMagisterOptimus" class="panel-collapse collapse" role="tabpanel" aria-labelledby="ususEstMagisterOptimus">
      <div class="panel-body">
		<h1>Jetzt nur noch üben</h1>
		<p>Das wars schon!</p>
		<p>Am besten gleich üben:</p>
		<a class="btn btn-primary" href="index.py">DB->normalizer</a>
      </div>
    </div>
  </div>
<!-- end accordion -->
</div>

	</div>
	</div>
<script>
$(function () {
    $('#accordion').on('shown.bs.collapse', function (e) {
        var offset = $(this).find('.collapse.in').prev('.panel-heading');
        if(offset) {
            $('html,body').animate({
                scrollTop: $(offset).offset().top -20
            }, 500); 
        }
    }); 
});
</script>
	</body>
</html>
"""












