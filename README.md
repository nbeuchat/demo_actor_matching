# Actor matching demo

Who should play Hannibal (the Carthaginian, not the cannibal) if HBO ever adapts his story? How about you? Who should be your actor?
This application lets you input an image and see the top three actors that more closely resemble the image based on facial features.

Try it out on HugginFace _[Coming Soon]_


## Data

The data comes from two sources:

1. I built a list of relevant actors that have been in popular movies across their careers. The datasets that I used to build can be found on the [IMDB datasets page](https://datasets.imdbws.com/) (see instructions [here](https://www.imdb.com/interfaces/))
2. I then found 20 images of each actor using Microsoft Bing Search API using queries such as *"Brad Pitt, actor or actress"*

Note that due to API limits, I only took images from 1,000 actors. 

## Application

The application is built with Gradio and deployed on HuggingFace Space. In the background, it uses:

1. The [`face_recognition` library](https://github.com/ageitgey/face_recognition) to extract the location of faces in the image and compute an embedding of these faces
2. Spotify's `annoy` library to efficiently search the closest actors based on the face embedding and a small database of actors' faces embeddings. 
3. Show you the best matches!

This is meant to be a fun and tiny application. There are known issues and biases. 

## Known biases and limitations

There are a few issues with the dataset and models used:

- The dataset of actors is limited to a couple thousands actors and actresses and it is therefore not representative of the richness of professionals out there
- The subset of actors and actresses selected is based on an aggregated metrics that considers all movies and shows in which the person was listed as an actor/actress. It is the weighted sum of the number of IMDb votes for this movie/show, weighted by the average IMDb score. This is obviously only a rough indicator of popularity but provided me with a quick way of getting a dataset with actors that people may know.
- Given the above, the database sampling will have several biases that are intrinsic to (a) the IMDb database and user base itself which is biased towards western/American movies, (b) the movie industry itself with a dominance of white male actors
- The pictures of actors and actresses was done through a simple Bing Search and not manually verified, there are several mistakes. For example, Graham Greene has a mix of pictures from Graham Greene, the canadian actor, and Graham Greene, the writer. You may get surprising results from time to time! Let me know if you find mistakes

