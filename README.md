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

1. The [`face_recognition` library](https://github.com/ageitgey/face_recognition) to compute an embedding of the image
2. Spotify's `annoy` library to efficiently search the closest actors based on the image embedding and a small database of actors' faces embeddings. 
3. Show you your best matches!

