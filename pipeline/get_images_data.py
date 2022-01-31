import os
import requests
import pandas as pd
import os
import time

from datetime import datetime
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

BING_API_KEY = os.getenv("BING_API_KEY", None)


def get_actor_images(
    name: str, role: str = None, count: int = 50, api_key: str = BING_API_KEY
):
    """Get a list of actor images from the Bing Image Search API"""
    if api_key is None:
        raise ValueError("You must provide a Bing API key")

    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    query = f'"{name}"'
    if role:
        query = f"{query} ({role})"
    params = {
        "q": query,
        "count": count,
        "imageType": "Photo",
        "safeSearch": "Strict",
        "imageContent": "Face",
        "freshness": "Year",
    }
    response = requests.get(
        f"https://api.bing.microsoft.com/v7.0/images/search",
        headers=headers,
        params=params,
    )

    response.raise_for_status()
    return response.json()


def read_actors_list(
    max_actors: int = None, last_year_active: int = None, sort_by: str = None
):
    """Read and filter the list of actors"""

    df = pd.read_csv("data/imdb_actors.csv")
    if last_year_active:
        df = df[df["lastYear"] >= last_year_active]

    if sort_by:
        df = df.sort_values(sort_by, ascending=False)

    if max_actors:
        df = df.head(max_actors)

    return df


def store_all_actor_images_data(
    max_actors: int = None,
    images_per_actor: int = 10,
    last_year_active: int = None,
    output_file=None,
    max_api_calls_per_second: int = 3,
):
    """Get images data for each actor from the Bing Image Search API and store the results as csv"""

    df = read_actors_list(max_actors, last_year_active)
    df_im = None
    if output_file:
        try:
            df_im = pd.read_csv(output_file)
        except:
            # file does not exists yet
            pass

    # remove actors for which we already have images data
    if df_im is not None:
        df = df[~df["nconst"].isin(df_im["nconst"].unique())]

    print(f"Start retrieving images from Bing for {len(df)} actors")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            images_data = get_actor_images(
                name=row["primaryName"], count=images_per_actor
            )
        except Exception as e:
            print(e)
            continue

        df_im_tmp = pd.DataFrame(images_data["value"])
        df_im_tmp["nconst"] = row["nconst"]
        df_im_tmp["resultPosition"] = list(range(0, len(df_im_tmp)))

        if df_im is not None:
            df_im = pd.concat([df_im, df_im_tmp])
        else:
            df_im = df_im_tmp

        # Store progress
        df_im.to_csv(output_file, index=False)

        # Limit speed of requests to Bing Search (3 calls per seconds)
        time.sleep(1.0 / max_api_calls_per_second)


if __name__ == "__main__":
    store_all_actor_images_data(
        output_file="data/actors_images_new.csv",
        max_actors=2000,
        images_per_actor=20,
        last_year_active=datetime.now().year - 5,
        max_api_calls_per_second=100,
    )
