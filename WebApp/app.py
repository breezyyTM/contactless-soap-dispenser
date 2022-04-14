################################ Flask Setup ################################
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/amountLeft')
def show_Remaining_Liquid():
    # Read the value of 'soapAmount'
    with open("../soapAmount.txt", "r") as f:
            soapAmount = f.read()
            soapAmount = int(soapAmount)
            
    return render_template("amountLeft.html", value = soapAmount)

    
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')

#############################################################################

