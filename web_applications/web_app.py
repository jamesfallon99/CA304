from flask import Flask, redirect, request, render_template
#request allows you to inspect the information a client sends(e.g. parameters, ip address etc)
import json
import csv

app = Flask(__name__) #Create the application object

@app.route('/')
def homepage():
    return render_template('index.html') #Looks into our templates folder and renders index.html ----part 1

#/showname?username=<their name>
@app.route('/showname') #A decorator to link the function to a url ---part 2
def showname():
    uname = request.args.get('username') if request.args.get('username') is not None else None #looks at the URL, checks the arguments and gets the value of the username argument, if none supplied, defaults to none
    return render_template('name.html',name=uname)#Pass the name into our template, need to bind name to a variable, so let name = uname

@app.route('/formtest', methods=["GET", "POST"])#We're going to be accepting POST requests on this route so we need to pass another argument to @app.route. We do this by passing the methods argument, along with a list of methods as the value.
def formtest(): #Display a web form asking a user for their name
    if request.method == "POST": #The form is submitted via POST back to the server

        req = request.form
        name = req.get("username")
        #showname(name)
        return redirect('/showname?username='+name) #The redirect function, redirects the client to the /showname page, this displays the name of the user using flask templates
    return render_template('form.html')


@app.route('/allegiances')#part 3
def allegiances():
    
    csvFilePath = "allegiance.csv"
    jsonFilePath = 'templates/'r'data.json'
    
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    #print(jsonArray)
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
    #f = open('data.json')
    #data = json.load(f)
    #print(data)
    return render_template('data.json')

#Fetching json data
#To be able to display this data in our HTML file, we first need to fetch the data with JavaScript.
#We will fetch this data by using the fetch API. We use the fetch API in the following way:
@app.route('/allegiancedashboard')#part 4
def allegiance_dash():
    return render_template('allegiance_dash.html')
    
if __name__ == "__main__":
    app.run()