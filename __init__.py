
import os
import secrets
from flask import session
from flask_babel import Babel
from flask_caching import Cache
from flask_limiter import Limiter
from flask_migrate import Migrate
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_limiter.util import get_remote_address
from flask import Flask, request, redirect, url_for


# Create a Flask application instance
app = Flask(__name__)


# SECURITY WARNING: keep the secret key used in production secret!
# Use a secure environment variable to store the secret key.
# You can use the 'secrets' module (available in Python 3.6+) to generate a secret key:
SECRET_KEY = "flask-insecure-c#y(k55srf&7q^i@mi+f*tw_%ll$^w@#cd1=fwa6&8tr^2qwv1"
secret_key = secrets.token_urlsafe(20)  # Generate a secure secret key


# Define the database path relative to the application directory
APP_DATABASE = os.path.join(os.path.dirname(__file__), "database")
DATABASE_PATH = os.path.join(APP_DATABASE, "Database.db")  # Database name can be change


# Flask-Limiter adds rate limiting to Flask applications (e.g limiting the number of request a client can send).
limiter = Limiter(
    app=app,
    headers_enabled=True,
    storage_uri="memory://",
    key_func=get_remote_address,
    default_limits=["3000 per hour"],
)


# Configure Flask application settings
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["BABEL_DEFAULT_LOCALE"] = "en_US"
app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"


# Configure media files for file uploads
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024 #10MB
app.config["ALLOWED_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".pdf"]
app.config["UPLOAD_FOLDER"] = os.path.abspath(os.path.join("my_demo_app", "static", "media"))


# Configure Flask-Caching
app.config["CACHE_TYPE"] = "simple"  # You can use 'simple', 'redis', 'memcached'
app.config["CACHE_DEFAULT_TIMEOUT"] = (
    300  # Cache timeout in seconds (e.g., 300 seconds = 5 minutes)
)


# Initialize database, babel, cache, CSRF protection, and migration management instances
babel = Babel(app)
cache = Cache(app)
cache.init_app(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)  # Protect against Cross-Site Request Forgery (CSRF) attacks
migrate = Migrate(app, db)  # Database migration with Flask-Migrate


# Configure Flask-Session for database-backed sessions
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_TYPE"] = "sqlalchemy"  # Use SQLAlchemy backend
app.config["SESSION_SQLALCHEMY"] = db  # Reference SQLAlchemy instance
app.config["SESSION_SQLALCHEMY_TABLE"] = "user_sessions"  # Use the Session model
app.config["SESSION_PERMANENT"] = False  # Set to True for persistent sessions
app.config["SESSION_USE_SIGNER"] = True  # Use a secret key for signing

Session(app)  # Initialize Flask-Session extension


# Flask_Asset for minifying js & css code for faster page loading
assets = Environment(app)


# Creating an instance of the Bundle
js = Bundle(
    # "js/script.js",
    # filters="jsmin",
    # output="gen/packed.js",
)


bootjs = Bundle(
    # filters="jsmin",
    # output="gen/packed.js",
)


css = Bundle(
    "css/base_main.css",
    filters="cssmin",
    output="gen/packed.css",
)


# Flask asset registration
assets.register("main_js", js)
assets.register("base_main_", css)
assets.register("bootstrap_js", bootjs)


@app.before_request
def app_middleware():
    # This middleware function performs several actions before each request:

    '''
    # Skip Processing for Dynamic Routes:
    # We check if the path starts with a slash (/) to handle potential invalid paths.

    # We use a generator expression and any to determine if any character after the first slash in the path (request.path[1:]) is non-alphanumeric. This identifies dynamic routes that likely use tokens or IDs.

    # If the path is identified as dynamic, the function returns None, effectively skipping URL processing for that route.

    # Canonicalization and Trailing Slash Removal:
    # If the path isn't a dynamic route, the middleware applies URL canonicalization (lowercase URLs) and trailing slash removal for static routes.

    # Benefits:
    # This approach avoids modifying URLs generated using secrets.token_urlsafe(), ensuring your dynamic routes maintain their integrity.

    # It keeps URL processing logic in a separate, reusable function for better organization.
    '''
    try:
        # Check for valid request path format (starts with a slash)
        if not request.path.startswith("/"):
            raise ValueError("Invalid request path format")

        # Skip processing for dynamic routes (non-alphanumeric characters)
        if any(not char.isalnum() for char in request.path[1:]):
            return None

        # URL Canonicalization: Redirect URLs with uppercase letters to lowercase
        if request.path != request.path.lower():
            return redirect(request.path.lower())

        # Remove trailing slashes except for root URL
        if request.path != "/" and request.path.endswith("/"):
            return redirect(request.path.rstrip("/"))

    except ValueError as e:
        app.logger.error(f"Middleware error: {e}, Request Path: {request.path}")
        session["error_message"] = (
            f"Middleware error: {e}, Request Path: {request.path}"
        )
        return redirect(url_for("errors_.value_error"))

    # No need to modify the URL for non-dynamic routes
    return None


@app.after_request
def app_security_headers_middleware(response):
    # This middleware function sets the X-Frame-Options header to "DENY" to prevent clickjacking attacks.

    # Security Headers: Sets essential security headers to mitigate potential vulnerabilities:

    # Referrer-Policy: Limits referrer information leaks.

    # X-Content-Type-Options: Prevents MIME-sniffing.

    # Content-Security-Policy (Basic implementation): Provides a starting point for restricting resource loading.

    '''Content-Security-Policy (CSP) Header
    The Content-Security-Policy (CSP) header is a security feature that helps prevent various types of attacks, such as Cross-Site Scripting (XSS) and data injection attacks. It allows web developers to control which resources (e.g., scripts, stylesheets, fonts, images) the browser is allowed to load for a specific web page.
    '''

    # X-Frame-Options: # Prevent clickjacking

    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # You can set response.headers to "no-referrer" to prevent any information leaking from your site.

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Content-Security-Policy"] = (
        "default-src 'self';"
        "script-src 'self' static/js/;"
        "style-src 'self' static/css/ https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css;"
        "font-src 'self' static/fonts;"
        "img-src 'self' static/media/ static/icons;"
    )
    response.headers["X-Frame-Options"] = "DENY"  # Prevent clickjacking

    # When executed the code below in a browser's console, it attempts to create an iframe pointing to http://127.0.0.1:5000/. However, because you've set the X-Frame-Options header to DENY, the browser will refuse to load your web page within an iframe, regardless of where it's hosted.

    '''var iframe = document.createElement('iframe');
    iframe.src = 'http://127.0.0.1:5000/';
    document.body.appendChild(iframe);'''

    return response
    

def flask_db_init():
    # This function creates and initiates the `db migration` folder if it does not exist.
    migrations_folder = os.path.join(os.getcwd(), 'migrations')
    if not os.path.exists(migrations_folder):
        os.system("flask db init")


# Import and register blueprint containing application routes
from my_demo_app.views.routes import view
from my_demo_app.search.routes import search_
from my_demo_app.errors.routes import errors_
from my_demo_app.uploads.routes import file_upload_
from my_demo_app.media_utils.utils import img_utils
from my_demo_app.admin.routes import admin_controller
from my_demo_app.authentication.routes import authent_
from my_demo_app.account_settings.routes import account_
from my_demo_app.caching.cache_constant import app_cache


app.register_blueprint(view, url_prefix="/")
app.register_blueprint(search_, url_prefix="/")
app.register_blueprint(errors_, url_prefix="/")
app.register_blueprint(authent_, url_prefix="/")
app.register_blueprint(account_, url_prefix="/")
app.register_blueprint(img_utils, url_prefix="/")
app.register_blueprint(app_cache, url_prefix="/")
app.register_blueprint(file_upload_, url_prefix="/")
app.register_blueprint(admin_controller, url_prefix="/")
