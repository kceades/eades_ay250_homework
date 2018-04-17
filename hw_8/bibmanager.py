import os
from flask import Flask,request,redirect,url_for,render_template
import sqlite3
from pybtex.database import parse_file

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # where uploaded files are kept

if not os.path.isdir(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
	"""
	Method to handle the home page routing.
	"""
	return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
	"""
	Method to handle file uploads and its relevant pages.
	"""
	if request.method == 'GET': # display the basic upload page
		return render_template('upload.html')
	else:
		file = request.files['file']
		try: # attempt to parse the upload POST request
			if file.filename != '' and request.form['collection'] != '':
				if file.filename[-4:]=='.bib': # make sure the file is .bib
					# svae the uploaded file to an upload folder
					file.save(os.path.join(app.config['UPLOAD_FOLDER']\
						,file.filename))
					# add the data in the file to the database
					add_to_database(file.filename,request.form['collection'])
					# return the success page
					return render_template('upload_success.html'\
						,file_name=file.filename\
						,collection_name=request.form['collection'])
				else:
					return render_template('upload_failure.html')
			else:
				return render_template('upload_failure.html')
		except: # if an unexpected error arises, default to a failure page
			return render_template('upload_failure.html')

@app.route('/search',methods=['GET','POST'])
def search():
	"""
	Search method to handle all the searching, both with GETs and POSTs
	"""
	if request.method=='GET': # display the basic search page
		return render_template('search.html')
	else:
		try: # in case files have been uploaded to the database
			if request.form['query'] != '':
				connection = sqlite3.connect('data.db')
				sql_cmd = """SELECT DISTINCT * FROM Data WHERE {}""".format(\
					request.form['query'])
				cursor = connection.cursor()
				cursor.execute(sql_cmd)
				results = cursor.fetchall()
				# build a list of dictionaries to render into the results page
				formatted = [{'Key':result[0]\
					,'Authors':result[1]\
					,'Journal':result[2]\
					,'Pages':result[3]\
					,'Year':result[4]\
					,'Title':result[5]\
					,'Collection':result[6]} for result in results]
				return render_template('search_success.html'\
					,query=request.form['query']\
					,results_dict=formatted)
			else:
				return render_template('search_failure.html')
		except: # no files yet uploaded to the database
			return render_template('search_failure.html')

def add_to_database(file_name,collection_name):
	"""
	Adds all the data in the specified file (presumed uploaded) to the database
	under the given collection name.

	:file_name: (str) the name of the bib file that has been uploaded
	:collection_name: (str) the name of the collection that file is associated
						with
	"""
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()
	# make a table if none exists already
	sql_cmd = """CREATE TABLE IF NOT EXISTS Data 
		(Key TEXT,
		Authors TEXT,
		Journal TEXT,
		Pages TEXT,
		Year INTEGER,
		Title TEXT,
		Collection TEXT)"""
	cursor.execute(sql_cmd)
	connection.commit()

	path = UPLOAD_FOLDER + '/' + file_name
	# parse the bib data
	bib_data = parse_file(path)
	for entry in bib_data.entries:
		# for each entry in the bib file, upload the important information to
		# the database table Data
		current = bib_data.entries[entry]
		key = current.key
		# check for the relevant fields and default all to empty strings (and
		# the year to 0)
		try:
			authors = [parse_author(str(author)) for author \
				in current.persons['author']]
			authors = ', '.join(authors)
		except:
			authors = ''
		if 'Journal' in current.fields:
			journal = str(current.fields['Journal'])
		elif 'Booktitle' in current.fields:
			journal = str(current.fields['Booktitle'])
		else:
			journal = ''
		if 'Pages' in current.fields:
			pages = str(current.fields['Pages'])
		else:
			pages = ''
		if 'Year' in current.fields:
			year = int(current.fields['Year'])
		else:
			year = 0
		if 'Title' in current.fields:
			title = str(current.fields['Title'])[1:-1]
		else:
			title = ''
		
		sql_cmd = f"""INSERT INTO Data VALUES
			("{key}",
			"{authors}",
			"{journal}",
			"{pages}",
			{year},
			"{title}",
			"{collection_name}")"""
		cursor.execute(sql_cmd)
	connection.commit()

def parse_author(name):
	"""
	Helper function for the add_to_database method. It takes a name as the bib
	parser persons field is formatted and returns it in a simple
	'first last' format.

	:name: (str) the name to reformat (as specified by the pybtex parser)

	:returns: (str) the reformatted name
	"""
	split = name.split(', ')
	first = split[1]
	last = split[0][1:-1]
	return first + ' ' + last

if __name__ == '__main__':
	# start the app with the command "python bibmanager.py" in the terminal
	app.run()