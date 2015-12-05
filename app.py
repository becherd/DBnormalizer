import web
import DBnormalizer
import views

def printResults(string):
	x = DBnormalizer.parseInput(string)
	print len(x)
	if len(x)<3:
		return x[0]
	else:
		relation = x[0]
		fds = x[1]
		mvds = x[2]
		targetNf = x[3]
		keys, normalForms, newSchema = DBnormalizer.computeEverything(relation, fds, mvds, targetNf)
		return views.resultToString(relation, fds, mvds, keys, normalForms, targetNf, newSchema) 

	

urls = ('/', 'dbnormalizer')
render = web.template.render('templates/')

app = web.application(urls, globals())


formRelation = web.form.Form(
                web.form.Textbox('Relation', class_='form-control', id='relation'),
                web.form.Textarea('FDs / MVDs', class_='form-control', id='fds'),
                web.form.Dropdown('In folgende Normalform umwandeln', [('None', 'Keine'), ('3NF', '3NF'), ('BCNF', 'BCNF'), ('4NF', '4NF')], class_='form-control', id='targetNf')
                )

class dbnormalizer:
    def GET(self):
		form = formRelation()
		return render.dbnormalizer(form, "Bitte Relation und FDs eingeben")
        
    def POST(self):
        form = formRelation()
        form.validates()
        result = form.value['inputfields']
        return printResults(result)

if __name__ == '__main__':
    app.run()

