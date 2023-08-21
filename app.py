from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    return render_template('home.html', survey = satisfaction_survey)

@app.route('/questions/<int:q_id>')
def get_question(q_id):
    if responses is None:
        return redirect('/')
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')


    if q_id != len(responses):
        flash(f'Invalid question id: {q_id}.')
        return redirect (f'/questions/{len(responses)}')
           
    return render_template(
        'questions.html', question=satisfaction_survey.questions[q_id])
        


@app.route('/answer', methods=["POST"])
def get_answer():
    answer = request.form['answer']
    responses.append(answer)
    if len(satisfaction_survey.questions) == len(responses):
        return redirect('/thankyou')
    else:
        return redirect('/questions/'+str(len(responses)))
    
@app.route('/thankyou')
def thank_you_page():
    return render_template('thank_you.html')