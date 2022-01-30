---
title: Actors matching
emoji: 🎬
colorFrom: yellow
colorTo: orange
sdk: gradio
app_file: app.py
pinned: true
---

# Actors matching demo

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

## Next steps

- Better image dataset (ie: identify and clean-up errors where multiple people where queried in the Bing Search)
- Larger dataset and more balanced dataset (to reduce the bias toward white male actors)
- Provide a way of looping through multiple people in a picture in the Gradio app
- Currently, I find the best matching actor using the average embedding for the actor. I plan to then do a second pass to find the closest matching picture(s) of this specific actor for a better user experience. 
- Deeper analysis of which embedding dimensions are necessary. Might want to reweight them.

## Credits

Author: Nicolas Beuchat (nicolas.beuchat@gmail.com)

Thanks to the following open-source projects:

- [dlib](https://github.com/davisking/dlib) by [Davis King](https://github.com/davisking) ([@nulhom](https://twitter.com/nulhom))
- [face_recognition](https://github.com/ageitgey/face_recognition) by [Adam Geitgey](https://github.com/ageitgey)
- [annoy](https://github.com/spotify/annoy) by Spotify 

Example images used in the Gradio app (most under [Creative Commons Attribution license](https://en.wikipedia.org/wiki/en:Creative_Commons)):

- [RB Ginsburg](https://www.flickr.com/photos/tradlands/25602059686) - CC
- [Frederik Douglass](https://commons.wikimedia.org/wiki/File:Frederick_Douglass_1856_sq.jpg) - CC
- [Leonardo da Vinci](https://commons.wikimedia.org/wiki/File:Leonardo_da_Vinci._Photograph_by_E._Desmaisons_after_a_print_Wellcome_V0027541EL.jpg) - CC
- [Hannibal Barca](https://en.wikipedia.org/wiki/Hannibal#/media/File:Mommsen_p265.jpg) - Public domain
- [Joan of Arc](https://de.wikipedia.org/wiki/Jeanne_d%E2%80%99Arc#/media/Datei:Joan_of_Arc_miniature_graded.jpg) - Public domain