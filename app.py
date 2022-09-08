
from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse

 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopname=db.Column(db.String(20), unique=False, nullable=False)
    Orderone = db.Column(db.String(20), unique=False, nullable=False)
    ornumber =db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.String(20), unique=False, nullable=False)

 
@app.route("/new")
def home_view():
        return "<h1>Welcome to Geeks for Geeks</h1>"


 
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
        db.session.add(new_user)
        db.session.commit()
        quote="Your order saved SucessFully"
        msg.body(quote)
        responded = True
    if not responded:
        msg.body('Please place order!')
    return str(resp)
