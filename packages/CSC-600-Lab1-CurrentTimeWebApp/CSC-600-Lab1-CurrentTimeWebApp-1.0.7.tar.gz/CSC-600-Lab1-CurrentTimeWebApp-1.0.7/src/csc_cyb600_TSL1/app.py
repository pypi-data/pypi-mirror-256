from flask import Flask
import datetime

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def get_current_time():
        current_time = datetime.datetime.now().strftime("%m/%d/%Y  %H:%M:%S")
        return f"Current Time: {current_time}"

    return app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True)
#Finshed