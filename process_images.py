import face_recognition
import requests
import pandas as pd
from io import BytesIO
from tqdm import tqdm
from time import time


def get_image(url: str):
    response = requests.get(url)
    response.raise_for_status()
    img_file_object = BytesIO(response.content)
    return face_recognition.load_image_file(img_file_object)

def get_embeddings(url: str):
    try:
        image = get_image(url)
        embeddings = face_recognition.face_encodings(image, num_jitters=2, model="large")
        return list(embeddings[0])
    except Exception as e:
        print(e)

def process_all_images(input_file, output_file):
    df = pd.read_csv(input_file)[["nconst","contentUrl","resultPosition"]]
    
    try:
        df_emb = pd.read_csv(output_file)
        df = df[~df["contentUrl"].isin(df_emb["contentUrl"])]
    except: 
        # file does not exists yet
        df_emb = pd.DataFrame(columns=list(df.columns) + ["embeddings"])

    print(f"Start processing of {df.shape[0]} images")
    df = df.sort_values("resultPosition", ascending=True)
    #df = df.sample(frac=1) # shuffle so you get some images for everybody while it's running
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        embeddings = get_embeddings(row["contentUrl"])
        new_row = row.copy()
        new_row["embeddings"] = embeddings
        new_row = new_row[["nconst", "contentUrl", "embeddings"]]
        df_emb = df_emb.append(new_row, ignore_index=True)

        if i % 5 == 0:
            df_emb.to_csv(output_file, index=False)

    df_emb.to_csv(output_file, index=False)
    return df_emb

def build_annoy_index():
    pass

if __name__ == "__main__":
    output_file = "data/actors_embeddings.csv"
    df_embeddings = process_all_images(input_file="data/actors_images.csv", output_file=output_file)