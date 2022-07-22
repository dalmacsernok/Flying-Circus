from flask import Flask, render_template, request, url_for, redirect, session, escape

import data

import data_handler

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\xec]/'

# 4. /test: TEST
# 1 kérdést mutat és a hozzá tartozó válaszokat.Összes kérdés megválaszolását követően: redirect to /result.
# Válaszok: radio buttonként, submit button.
# If the user is not logged in, opening the /test page will redirect to the / page!
# After submitting the last question: redirect to /result
# Refreshing the /test page: keeps the actual answer shown!! (nincs új POST request kérés)
#
# 5. /result: RESULT
# The number of correctly answered questions is displayed.
# User logged in: number of correctly answered questions is displayed.
# User NOT LOGGED IN: redirects to the / page!


@app.route('/')
def index():
    if 'username' not in session:
        session['username'] = None
    return render_template('index.html', username = session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email in data.users:
            if data_handler.verify_password(password, data.users[email]):
                session['username'] = email
                return redirect(url_for('index'))
        error = True
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/test')
def test():
    new_list = []
    for question, answers in data.questions.items():
        new_list.append({question: answers})
    if 'current' not in session:
        session['result'] = 0
        session['current'] = 0
    if session['current'] > len(new_list) - 1:
        return redirect(url_for('test_results'))
    return render_template('test.html', questions=new_list[session['current']])


@app.route('/step', methods=['POST'])
def step():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == 'True':
            session['result'] += 1
        session['current'] += 1
        return redirect(url_for('test'))


@app.route('/results')
def test_results():
    result = session['result']
    session.pop('result', None)
    session.pop('current', None)
    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

