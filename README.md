## film-nlp-flask-app (WIP)

#### Check project_diary.md for work progress


#### Description:
This docker containerized app extracts data from film scripts using webscraping tools and stores the data in a SQL database. Users can freely view the dialogue data from their favorite characters and run specialized search queries seamlessly through an intuitive search bar.

Additional features will be added (agenda):
- dynamic visualizations for character dialogue analysis
- character arc timelines through sentiment analysis across films
- character based chatbots
- additional features will be added...

#### Prerequisite:
- Have Docker insalled

#### Start App:
- to start the app run: `docker-compose up --build` 
- access app in browser using `https:localhost:8000`

- `docker-compose down` to bring down the container

All data collected from https://imsdb.com/ or https://movies.fandom.com/ and is only used for educational purposes. 


#### Files overview:
- mcu_web_scraping.py scrapes dialogue from transcripts from a substantial amount of movies from the MCU franchise. All transcript links are saved in urls. Running the script outputs the csv file used to populate the SQL tables used in the Flask app.
