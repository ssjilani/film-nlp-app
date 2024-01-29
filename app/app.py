from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import secrets
from app.models.script_db import db 

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = secrets.token_hex(16)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@script_db/script_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
        
    #### routes

    @app.route('/')
    def hub():
        return render_template('hub.html')
    
    @app.route('/script-data')
    def data_view():
        return render_template('view_script.html')
    
    @app.route('/get_script_data')
    def get_script_data():
        current_page = int(request.args.get('page', 1))
        items_per_page = 100

        offset = (current_page - 1) * items_per_page
        
        sql_query = text(f"""SELECT * FROM script_data
                            LIMIT {items_per_page} OFFSET {offset}
                        """)

        with app.app_context():
            result = db.session.execute(sql_query)
            data = result.fetchall()

        data_dict_list = []
        for row in data:
            data_dict = {'line_id': row[0], 'character_name': row[1], 'dialogue': row[2], 'character_line_number': row[3],
                         'film': row[4], 'url': row[5], 'franchise': row[6]}
            data_dict_list.append(data_dict)

        return jsonify(data_dict_list)
    
    @app.route('/search')
    def search_data():
        search_term = request.args.get('search', '')
        current_page = int(request.args.get('page', 1))
        items_per_page = 100
        offset = (current_page - 1) * items_per_page

        # Use ILIKE for case-insensitive search
        sql_query = text(f"""SELECT * FROM script_data
                            WHERE lower(character_name) LIKE :search_term
                            OR lower(film) LIKE :search_term
                            OR lower(dialogue) LIKE :search_term
                            LIMIT {items_per_page} OFFSET {offset}
                        """)

        with app.app_context():
            result = db.session.execute(sql_query, {'search_term': f"%{search_term.lower()}%"})
            data = result.fetchall()

        data_dict_list = []
        for row in data:
            data_dict = {'line_id': row[0], 'character_name': row[1], 'dialogue': row[2], 'character_line_number': row[3],
                        'film': row[4], 'url': row[5], 'franchise': row[6]}
            data_dict_list.append(data_dict)

        return jsonify(data_dict_list)

        
    
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
               'film' : data[4],
               'url' : data[5],
               'franchise' : data[6]
               }
        return jsonify(dic)
        

    return app
    

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)