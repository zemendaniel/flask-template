from flask import redirect, url_for, render_template, request, g, flash, abort, send_file
from blueprints.pages import bp
from security.decorators import is_fully_authenticated, is_admin
from blueprints.pages.forms import SetOrgNameForm, SetFaviconForm, SetWelcomeTextForm
from persistence.repository.site_setting import SiteSettingRepository
from io import BytesIO
from blueprints import flash_form_errors


@bp.route('/')
def home():
    return render_template('pages/home.html', welcome_text=SiteSettingRepository.get_welcome_text())


@bp.route('/set-favicon', methods=['POST'])
def set_favicon():
    form = SetFaviconForm()
    if form.validate_on_submit():
        SiteSettingRepository.set_favicon(form.icon.data)
        flash("The favicon was set successfully", 'success')
    elif form.errors:
        flash_form_errors(form)

    return redirect(url_for('pages.site_settings'))


@bp.route('/set-welcome-text', methods=['POST'])
def set_welcome_text():
    form = SetWelcomeTextForm()
    if form.validate_on_submit():
        SiteSettingRepository.set_welcome_text(form.text.data)
        flash("The welcome text was set successfully", 'success')
    elif form.errors:
        flash_form_errors(form)

    return redirect(url_for('pages.site_settings'))


@bp.route('/set-org-name', methods=['POST'])
def set_org_name():
    form = SetOrgNameForm()
    if form.validate_on_submit():
        SiteSettingRepository.set_org_name(form.name.data.strip())
        flash("The organization name was set successfully", 'success')
    elif form.errors:
        flash_form_errors(form)

    return redirect(url_for('pages.site_settings'))


@bp.route('/site-settings')
@is_fully_authenticated
@is_admin
def site_settings():
    org_form = SetOrgNameForm()
    icon_form = SetFaviconForm()
    welcome_form = SetWelcomeTextForm()

    org_form.name.data = SiteSettingRepository.get_org_name()
    welcome_form.text.data = SiteSettingRepository.get_welcome_text()

    return render_template('pages/site-settings.html', org_form=org_form, icon_form=icon_form,
                           favicon_exits=bool(SiteSettingRepository.find_by_key('favicon')), welcome_form=welcome_form)


@bp.route('/delete-favicon', methods=['POST'])
@is_fully_authenticated
@is_admin
def delete_favicon():
    icon = SiteSettingRepository.find_by_key('favicon') or abort(404)
    SiteSettingRepository.delete(icon)
    flash("The favicon was deleted successfully", 'success')
    return redirect(url_for('pages.site_settings'))


@bp.route('/favicon.ico')
def favicon():
    icon = SiteSettingRepository.get_favicon() or abort(404)

    return send_file(BytesIO(icon), mimetype='application/octet-stream', as_attachment=False, download_name='favicon.ico')


@bp.route('/errors')
@is_fully_authenticated
@is_admin
def errors():
    if request.args.get('delete'):
        with open('errors.log', 'w') as f:
            f.write('')
        return redirect(url_for('pages.errors'))

    try:
        with open('errors.log', 'r') as f:
            errors_text = f.read().replace('\n', '<br>')
    except FileNotFoundError:
        errors_text = ""

    return render_template("errors/errors.html", errors=errors_text)


# @bp.route("/about")
# def about():
#     return render_template("pages/about.html")
