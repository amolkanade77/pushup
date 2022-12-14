from flask import Flask,request,render_template
from twilio.twiml.messaging_response import MessagingResponse
from flask_sqlalchemy import SQLAlchemy
import datetime

 
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mmmpwvnmddqngm:ff013c1a0649a4f13da37c14d55d7ab4daa48570b3d8c95f1e7d162456e9e971@ec2-18-208-55-135.compute-1.amazonaws.com:5432/d44k3c675e1jqp'
db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopname=db.Column(db.String(20), unique=False, nullable=False)
    Orderone = db.Column(db.String(20), unique=False, nullable=False)
    ornumber =db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.String(20), unique=False, nullable=False)
    
    
class Orderdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopname=db.Column(db.String(120), unique=False, nullable=False)
    cover = db.Column(db.String(120), unique=False, nullable=False)
    glass =db.Column(db.String(120), unique=False, nullable=False)
    custome =db.Column(db.String(20), unique=False, nullable=False)
    order_date = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    

    
@app.route('/displaydata', methods=['GET'])
def home():
    users = Profile.query.all()
    return render_template("admin.html", data=users,len = len(users))



 
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    
    print(request.values.get)
    Finaldata=incoming_msg.splitlines()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'shopname' in incoming_msg:      
        new_user = Profile(shopname=Finaldata[0].split('-')[1],Orderone=Finaldata[1].split('-')[1],ornumber=Finaldata[2].split('-')[1],last_name=Finaldata[3].split('-')[1],age=Finaldata[4].split('-')[1])
        print(db.session.add(new_user))
       
        db.session.commit()
        quote="Your order saved SucessFully"
        msg.body(quote)
        responded = True
    if not responded:
        msg.body('Please place order!')
    return str(resp)
   
   
@app.route('/displaydata', methods=['GET'])
def display():
    print("In Loop")
    users = Profile.query.all()
    print(users)
    return render_template("admin.html", data=users,len = len(users))
  

@app.route('/', methods=['GET'])
def homemahakal():
    return render_template("index.html")
 
 
 
 
@app.route('/upbot', methods=['POST'])
def upbot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    Finaldata=incoming_msg.splitlines()
    Finaldata = [i for i in Finaldata if i != '']
    
    for i in Finaldata:
        if i.split()[1]=='mobile':
            mobile=i.split()[1]
            
    if 'mobile'in incoming_msg:
        # for i in Finaldata:
        #     if "cover" in i:
        #         cover=i
        #         glass='None'
        #     elif "glass" in i:
        #         glass=i
        #         cover='None' 
        glass=list(filter(lambda x: "glass" in x, Finaldata))   
        glass = ' '.join(str(e) for e in glass)
        cover=list(filter(lambda x: "cover" in x, Finaldata)) 
        cover = ' '.join(str(e) for e in cover)
        if glass and cover is not None:
            new_user = Orderdetails(shopname=Finaldata[0],glass=glass,cover=cover,custome="None")  
        else:  
            new_user = Orderdetails(shopname=Finaldata[0],custome=Finaldata[1],cover="None",glass="None")    
        db.session.add(new_user)
        db.session.commit()
        quote="Your order saved SucessFully"
        msg.body(quote)
        responded = True
    else:
        quote="Please place order in format"
        msg.body(quote)
        responded = True 
    if not responded:
        msg.body('Please place order!')
        
    return str(resp)
    
    
@app.route('/newdisplay', methods=['GET'])
def newdisplay():
    # users = Orderdetails.query.all().order_by('-id').reverse()
    users=Orderdetails.query.order_by(Orderdetails.id.desc()).all()
    return render_template("newdisplay.html", data=users,len = len(users))
    

