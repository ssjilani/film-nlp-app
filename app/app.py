from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import secrets
from app.models.script_db import db 
from web_scraping import extract_script_data


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = secrets.token_hex(16)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@script_db/script_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    def populate_data(url):
        film_title = url.split('/')[-1]
        film_title = film_title.split('.')[0]

        with app.app_context():
            script_ = extract_script_data(url)

            for i in range(len(script_)):
                line_id = f'{film_title}-{i + 1}'
                character_name = script_[i][0]
                dialogue = script_[i][1]
                character_line_number = int(script_[i][2])

                query = text(
                    """
                    INSERT INTO script_data (line_id, character_name, dialogue, character_line_number, film)
                    VALUES (:line_id, :character_name, :dialogue, :character_line_number, :film);
                    """
                )

                db.session.execute(
                    query,
                    {
                        'line_id': line_id,
                        'character_name': character_name,
                        'dialogue': dialogue,
                        'character_line_number': character_line_number,
                        'film': film_title
                    }
                )

            db.session.commit()




    @app.route('/')
    def hub():

        sql_query = text(f"""SELECT count(*) FROM script_data
                         """)
        with app.app_context():
            result = db.session.execute(sql_query)

            count = result.fetchone()[0]

        if count > 0:
            pass
        else:
            populate_data("https://imsdb.com/scripts/Batman.html")

        return render_template('hub.html')
    
    @app.route('/script-data')
    def data_view():

        sql_query = text(f"""SELECT * FROM script_data
                         """)

        with app.app_context():
            result = db.session.execute(sql_query)
            data = result.fetchall()

        return render_template('view_script.html', data=data)
    
    
    @app.route('/detail-view/<line_id>')
    def detail_view(line_id):

        sql_query = text(f"""SELECT * FROM script_data
                            WHERE line_id = '{line_id}'
                         """)

        with app.app_context():
            result = db.session.execute(sql_query)
            data = result.fetchone()


        dic = {'line_id' : data[0],
               'character_name' : data[1],
               'dialogue' : data[2],
               'character_line_number' : data[3],
               'film' : data[4]
               }
        return jsonify(dic)
        

    return app
    

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)