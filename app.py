import logging
import persistence
from logging.handlers import RotatingFileHandler
from flask import Flask
import blueprints.posts
import blueprints.security
import blueprints.pages
import blueprints.users
import security
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_minify import Minify
from blueprints.pages import init_error_handlers
from custom_filters import safe_br
from persistence.repository.site_setting import SiteSettingRepository

csrf = CSRFProtect()
minify = Minify(html=True, js=True, cssless=True)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.jinja_env.globals['org_name'] = lambda: SiteSettingRepository.get_org_name()
    app.jinja_env.filters['safe_br'] = safe_br
    app.jinja_env.add_extension('jinja2.ext.do')

    persistence.init_app(app)
    security.init_app(app)
    csrf.init_app(app)
    minify.init_app(app)
    init_error_handlers(app)

    app.register_blueprint(blueprints.posts.bp, url_prefix='/posts')
    app.register_blueprint(blueprints.pages.bp, url_prefix='/')
    app.register_blueprint(blueprints.security.bp, url_prefix='/')
    app.register_blueprint(blueprints.users.bp, url_prefix='/users')

    handler = RotatingFileHandler('errors.log')
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", debug=True)

