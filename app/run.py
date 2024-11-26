from app import *

app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(other_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__':
    app.run(debug=True)
