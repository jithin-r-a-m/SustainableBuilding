from flask import Flask,render_template,request,redirect, url_for
import pymongo



app= Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/second")
def feature():
      return render_template('features.html')
@app.route("/form")
def form():
      return render_template('form.html')

@app.route("/input",methods=["POST","GET"])
def input():
      if request.method=="POST":
          
            ba=int(request.form.get("area"))
            numfloor=request.form.get("numfloor")
            numhouse=request.form.get("numhouse")
            numpeople=int(request.form.get("numpeople"))
            totalbill=int(request.form.get("totalbill"))
            
            waste=calculate_waste(numpeople)
            swaste=calculate_swaste(numpeople)
            units=calculate_units(totalbill)
            biogas=calculate_bio(waste)
            water=calculate_water(numpeople)
            if numpeople<6:
                if units<105:
                    grade='A'
                elif units>600:
                    grade='C'
                elif units>300:
                    grade='B'
            elif numpeople>6:
                 if units<400:
                      grade='A'
                 elif units>800:
                      grade='C'
              
            evaluate={
                
                 'Area':ba,
                 'Number_of_floors':numfloor,
                 'Number_of_houses':numhouse,
                 'Number_of_people':numpeople,
                 'Total_bill':totalbill
            }
            energy_com={
                 
                 'power':units,
                 'waste_generated':waste,
                 'sewage_waste_generated':swaste,
                 'water_consumption':water,
                 'biiogas_generation':biogas 
            }
            
            db.evaluate.insert_one(evaluate)
            db.energy.insert_one(energy_com)
            avg=105
            p=int(units-105)
            pp=abs(round((((p/avg)*100)-100),2))
            if ba>1200:
                 si="3kW"
                 sa=12
                 totalsa=int(12*30)
            elif ba<600:
                 si="1kW"
                 sa=4
                 totalsa=int(4*30)
            else:
                 si="2kW"
                 sa=8
                 totalsa=int(8*30)
            sss=abs(units-totalsa)
            ss=int(totalsa-units)
            return render_template('dashboard.html',units=units,pp=pp,sa=sa,totalsa=totalsa,ss=ss,si=si,waste=waste,water=water,sss=sss,swaste=swaste,biogas=biogas)
      return render_template(form.html)
def calculate_water(numpeople):
     numpeopleww=int(numpeople)
     ww=(numpeopleww*150)
     wwm=(ww*30)
     water=wwm/1000
     return(water)
def calculate_waste(numpeople):
     numpeoplew=int(numpeople)
     wg=(numpeoplew*0.45)
     waste=(wg*30)
     return int(waste)
def calculate_swaste(numpeople):
     numpeoplew=int(numpeople)
     sw=(numpeoplew*300)
     swm=sw*30
     swaste=swm/1000
     return(swaste)
def calculate_bio(waste):
     wastes=int(waste)
     biogas=waste/0.6
     return round((biogas),2)
def calculate_units(totalbill):
    # calculate bill without tax
        totalbills=int(totalbill)
        tax = (0.09*totalbills)
    # initialize variables
        if totalbills>487.5:
            bill_without_tax =totalbills -100 -tax -110
        else:
            bill_without_tax = totalbills -100 -tax
        units = 0
        remaining_bill = bill_without_tax

        # calculate units for first 40 units (charged at 4.05 Rs per unit)
        if remaining_bill >= 40 * 4.15:
            units += 40
            remaining_bill -= 40 * 4.15
        else:
            units += remaining_bill / 4.15
            remaining_bill = 0

        # calculate units for next 50 units (charged at 5.5 Rs per unit)
        if remaining_bill >= 50 * 5.60:
            units += 50
            remaining_bill -= 50 * 5.60
        else:
            units += remaining_bill / 5.60
            remaining_bill = 0

        # calculate units for next 100 units (charged at 7.10 Rs per unit)
        if remaining_bill >= 100 * 7.15:
            units += 100
            remaining_bill -= 100 * 7.15
        else:
            units += remaining_bill / 7.15
            remaining_bill = 0

        # calculate units for remaining units (charged at 8.15 Rs per unit)
        units += remaining_bill / 8.2

        return int(units)

@app.route('/submitf', methods=['POST'])
def submitf():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    if db.register.find_one({'email': email}):
            return render_template("register.html" ,alert_message="email exsits")
    else:
            # Insert new user into the database
        db.register.insert_one({'email': email})
        return render_template("index.html",name=name)
    register= {
        'name': name,
        'email': email,
        'password': password
    }

    db.users.insert_one(register)
    
    return "User data submitted successfully!"
@app.route('/submitl', methods=['POST'])
def submitl():
    if request.method == 'POST':
        uname = request.form['uname']
        passw = request.form['pass']
        userc = db.users.find_one({'name':uname, 'password':passw})
        if userc:
        # Redirect to the desired page if login is successful
            return render_template("index.html",name=uname)
        else:
        # Redirect to the login page with an error message if login fails
           return render_template("register.html" ,alert_message="invalid user details")

@app.route("/dash")
def dash():
      return render_template('dashboard.html')
@app.route("/grading")
def grading():
     return render_template('gradding.html')
@app.route("/contact")
def contact():
     return render_template('contactnew.html')
@app.route("/register")
def register():
     return render_template('register.html')

if __name__=="__main__":
       app.run()