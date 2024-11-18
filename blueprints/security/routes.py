from urllib.parse import urlsplit
from flask import g, redirect, url_for, session, flash, request, render_template
from blueprints import flash_form_errors
from blueprints.security import bp, generate_login_token
from blueprints.security.forms import LoginForm
from persistence.repository.user import UserRepository



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('pages.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserRepository.find_by_name(form.name.data.strip())
        if user is not None and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            if request.args.get('redirect') is not None and urlsplit(request.args.get('redirect')).netloc == '':
                response = redirect(request.args.get('redirect'))
            else:
                response = redirect(url_for('pages.home'))

            if form.stay_logged_in.data:
                token = generate_login_token(user.id)

                response.set_cookie('login_token', token, max_age=2592000, secure=True, httponly=True)

            return response

        elif user is None:
            flash('Incorrect username', 'error')
        elif not user.check_password(form.password.data):
            flash("Incorrect password", 'error')
    elif form.errors:
        flash_form_errors(form)

    return render_template('security/login.html', form=form)


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    response = redirect(url_for('pages.home'))
    response.set_cookie('login_token', '', expires=0)
    flash('Logout successful', 'success')
    return response
