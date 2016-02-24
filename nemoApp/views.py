# imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from .forms import QueryForm
from nemoApp import app

@app.route('/')
@app.route('/home')
def index():
    """Searches the database for entries, then displays them."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid Username. Please try again."
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('query'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You are logged out')
    return render_template('logout.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    error = None
    ########### These would be replaced by DB entries ###############
    logger_type_choices = [('Mussel', 'Mussel'), \
                      ('Coral', 'Coral'), \
                      ('Sea Star', 'Sea Star')]
    country_name_choices = [('Canada', 'Canada'), \
                      ('USA', 'USA')]
    state_name_choices = [('Massachusetts', 'Massachusetts'), \
                      ('Oregon', 'Oregon')]
    location_name_choices = [('hopkins', 'Hopkins'), ('cattlepoint', 'Cattle Point')]
    zone_name_choices = [('Dummy1', 'Dummy1'), ('Dummy2', 'Dummy2')]
    sub_zone_name_choices = [('Dummy1', 'Dummy1'), ('Dummy2', 'Dummy2')]
    ##################################################################

    form = QueryForm(request.form)
    form.logger_type.choices = form.logger_type.choices  + logger_type_choices
    form.country_name.choices = form.country_name.choices + country_name_choices
    form.state_name.choices = state_name_choices
    form.location_name.choices = location_name_choices
    form.zone_name.choices = zone_name_choices
    form.sub_zone_name.choices = sub_zone_name_choices

    if request.method == 'GET':
        form.process()
    else:        
        if form.validate_on_submit():
            print("Query form submitted")
            flash("Query details. logger_type: '%s', country_name: '%s', \
                         state_name: '%s', location_name: '%s', \
                         Date From: '%s', Date To: '%s' " % \
                         (form.logger_type.data, form.country_name.data, \
                            form.state_name.data, form.location_name.data, \
                            form.date_pick_from.data.strftime('%m/%d/%Y'), 
                            form.date_pick_to.data.strftime('%m/%d/%Y')))
        else:
            error = 'Invalid Submission. All fields marked with * are compulsory'
    return render_template('query.html', title='Query', form=form, error=error)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# This function makes sure the server only runs if the script is executed directly
# from the Python interpreter and not used as an imported module.
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)