from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
CURRENT_SURVEY_KEY = 'current_survey'
app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
       
    return render_template('which_survey.html', surveys=surveys)

@app.route('/', methods=["POST"])
def set_survey():
    survey_id = request.form['survey']
    survey = surveys[survey_id]
    session[CURRENT_SURVEY_KEY] = survey_id
    return render_template('home.html', survey=survey)

@app.route('/begin', methods = ["POST"])
def start_survey():
    session["responses"] = []
    return redirect('questions/0')

@app.route('/questions/<int:q_id>')
def get_question(q_id):
    survey_code = session.get(CURRENT_SURVEY_KEY)
    survey = surveys[survey_code]
    responses =session.get('responses')
    if responses is None:
        return redirect('/')
    
    if len(responses) == len(survey.questions):
        return redirect('/thankyou')


    if q_id != len(responses):
        flash(f'Invalid question id: {q_id}.')
        return redirect (f'/questions/{len(responses)}')
           
    return render_template(
        'questions.html', question=survey.questions[q_id])
        


@app.route('/answer', methods=["POST"])
def get_answer():
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]
    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(survey.questions) == len(responses):
        return redirect('/thankyou')
    else:
        return redirect('/questions/'+str(len(responses)))
    
@app.route('/thankyou')
def thank_you_page():
    return render_template('thank_you.html')