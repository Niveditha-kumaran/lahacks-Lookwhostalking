# lahacks-Lookwhostalking
## Inspiration
As students, an elevator pitch is a very import aspect in interacting with professionals and making a first impression. An elevator pitch needs a coherent flow. People are often used to practising speeches in front of a mirror or with a friend, or maybe even recording their audio clips to judge it later. But the need to render complete and meaningful pitch is paramount which leads in creating a webapp that facilitates a data-driven approach to improving your pitch and making it widely available, especially to non-native English speakers in low-income areas.



## What it does
Once opening the webapp, you can record your pitch for a set amount of time(say 30 seconds). Once done, the audio file is analyzed using emotional and sentiment analysis to provide quality feedback such as sentiment and emotion scores as well the exact text recorded which gives you the feedback needed to know where to polish your pitch



## How we built it
We used Google Cloud's Speech-To-Text API to get text data, upon which we performed sentiment analysis over the text data. We also built a Naive Bayes classifier from scratch to provide emotional quotient of the text and a word pacer to calculate speech. We go through all these outputs in Python and display on a frontend built from Flask and HTML.



## Challenges we ran into
The biggest challenge we ran into was creating a front end. Being the first time developing a scalable front end, we faced technical issues with flask and javascript. An unresolved issue is making Python detect an in-built mic of an earphone for better video quality. Another issue was the compatibility of the audio file format with the Google API which was handled with multiple libraries and conversions.



## Accomplishments that we're proud of
We are proud of our naive Bayes classifier for being able to classify emotions perfectly and the successful integration of the audio input to the APIs and finally, to the NLP algorithm



## What we learned
We learnt a lot of integrating GCP Apis. We also learnt how to code on flask and integrate a html to python file for the first time.



## What's next for Look Who's Talking
Next step would be to provide feedback with better visualization in terms of pace, emotion and sentiment to come up with better recommendations for the user to augment their pitch with the vocabulary and emotion necessary.



## Built With
- speechapi
- cloud-speech-to-text
- python
-gcp
-cloud-natural-language
-naive-bayes
