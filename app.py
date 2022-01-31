import gradio as gr
from actors_matching.api import analyze_image, load_annoy_index
from pathlib import Path


annoy_index, actors_mapping = load_annoy_index()


def get_image_html(actor: dict):
    url = actor["url"]
    name = actor["name"]
    imdb_url = f"https://www.imdb.com/name/{actor['nconst']}/"
    return f"""
    <div style="position: relative; text-align: center; color: white;">
       <img src="{url}" alt="{name} matches the input image" style="height: 500px">
        <div style="padding: 0.2em; position: absolute; bottom: 16px; left: 16px; background-color: #aacccccc; font-size: 2em;">
            <p>{name}</p>
            <p style="font-size:0.5em"><a href={imdb_url} target="_blank">Click to see on IMDb</></p>
        </div>
    </div>
    """


def no_faces_found_html():
    return f"""<div>No faces found in the picture</div>"""


def get_best_matches(image, n_matches: int):
    return analyze_image(image, annoy_index=annoy_index, n_matches=n_matches)


def find_matching_actors(input_img, title, n_matches: int = 10):
    best_matches_list = get_best_matches(input_img, n_matches=n_matches)

    # TODO: allow looping through characters
    if best_matches_list:
        best_matches = best_matches_list[0]

        # TODO: Show how the initial image was parsed (ie: which person is displayed)

        # Build htmls to display the result
        output_htmls = []
        for match in best_matches["matches"]:
            actor = actors_mapping[match]
            output_htmls.append(get_image_html(actor))

        return output_htmls

    # No matches
    return [no_faces_found_html()]


iface = gr.Interface(
    find_matching_actors,
    title="Which actor or actress looks like you?",
    description="""Who is the best person to play a movie about you? Upload a picture and find out!
    Or maybe you'd like to know who would best interpret your favorite historical character? 
    Give it a shot or try one of the sample images below.\nPlease read below for more information on biases
    and limitations of the tool!""",
    article=Path("README.md").read_text(),
    inputs=[
        gr.inputs.Image(shape=None, label="Your image"),
        gr.inputs.Textbox(
            label="Who's that?", placeholder="Optional, you can leave this blank"
        ),
        # gr.inputs.Slider(minimum=1, maximum=10, step=1, default=5, label="Number of matches"),
    ],
    outputs=gr.outputs.Carousel(gr.outputs.HTML(), label="Matching actors & actresses"),
    examples=[
        ["images/example_rb_ginsburg.jpg", "RB Ginsburg in 1977"],
        [
            "images/example_hannibal_barca.jpg",
            "Hannibal (the one with the elephants...)",
        ],
        ["images/example_frederick_douglass.jpg", "Frederik Douglass"],
        ["images/example_leonardo_davinci.jpg", "Leonoardo da Vinci"],
        ["images/example_joan_of_arc.jpg", "Jeanne d'Arc"],
        ["images/example_sun_tzu.jpg", "Sun Tzu"],
    ],
)

iface.launch()
