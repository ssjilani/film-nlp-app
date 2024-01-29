## Project Diary

#### Day One:
Using beautiful soup script data was extracted from imsb. The extracted data was used to populated SQL tables, with the goal to allow users to access and interact with the data.

Batman (1989) film script was utilized for testing purposes. 

Furthermore, a flask app was intitizlized, which is deployed through dockerized containers along with postgresql services.

#### Day Two:
For the overall purpose of the project, which requires a substantial amount of data per character in order to train character specifc chatbots, imsb as a data source became less than ideal. It is lacking in consistency with the data availability, as it lacks sequel scripts which would be esential in gathering larger volumes of data per character and furthermore would limit the kinds of visulaizations being envisioned.

As an alternative to imsb, https://movies.fandom.com/ was found. It contains transcripts from thousand of films, and the data is quite well parsed, which would decrease the amoumnt of pre-processing required. 

The only caviat is that beautiful soup is not quite effective in extracting data from this website as it requires some user interaction. As an alternatve selenium is being used to extract the data as it has had uses in extracting data from dynamic websites using javascript.

Furthermore, the data is now going to focus on the MCU franchise of movies, as we can do our analysis effectively, which include character arcs within one film and character arcs over multiple films. Furthermore theres should be quite enough data to create our chatbots. 

The flask app and the dockers wer updated to reflect these changes, along with subtsntial upgrades to user experience when navigating the data.
