from flask import Flask, render_template, redirect, request, session # import all flask tools this project needs
import random, datetime
app = Flask(__name__) # create instance of Flask
app.secret_key = "lucky's charming pot of gold" # secret key is needed to modify session

@app.route('/') # default loading page
def main_page():
    if 'your_gold' not in session: # create session gold if it doesn't exist
        session['your_gold'] = 0
        session['activity_log'] = []
        session['moves'] = 0
    #if session['moves'] < 15 and session['your_gold'] < 200:
    elif session['moves'] >= 15 and session['your_gold'] < 200:
        session['game_over'] = "You lost."
    elif session['moves'] < 15 and session['your_gold'] >= 200:
        session['game_over'] = "You win!"
    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process_money():
    session['moves'] += 1 # increase moves
    current_destination = request.form['destination']
    amounts = { # dictionary holds range for golds in each building
        'Farm': random.randint(10,20), # returns random golds for Farm
        'Cave': random.randint(5,10), # [returns random golds for Cave
        'House': random.randint(2,5), #[ returns random golds for House
        'Casino': random.randint(-50,50) # [returns random golds for Casino
    }
    # generate a random number in the range as defined above
    found_gold = amounts[current_destination] # get random gold based on location
    session['your_gold'] += found_gold # add (or subtract!) the amount found to the overall pot

    now = datetime.datetime.now() # get current date
    date_string = now.strftime("%Y/%m/%d %I:%M %p") # format date to readable form
    activity_data = { # web page will use this data to populate the activity log
        'location': current_destination,
        'class': None,
        'amount': found_gold,
        'timestamp': date_string
    }
    if found_gold >= 0: # determine whether the log entry will be red or green
        activity_data['class'] = 'gain'
    else:
        activity_data['class'] = 'loss'
    session['activity_log'].insert(0,activity_data) # put the newest activity at the front of the line
    session.modified = True # makes session['activity'] log persistent 
    return redirect('/') # send data back to / without re-posting the form data
@app.route('/reset') # clears session to start over
def reset_game():
    session.clear()
    return redirect('/')
if __name__ == '__main__': # ensure this code is being run directly and not from another module
    app.run(debug = True, port = 8000) # run app in debug mode on port 8000