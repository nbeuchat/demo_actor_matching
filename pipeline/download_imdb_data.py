import os
import gzip
import shutil
from urllib.request import urlretrieve
from tqdm import tqdm


def download_large_file(url: str, output_file: str):
    if not os.path.exists(output_file):
        urlretrieve(url, output_file)


def unzip_file(input_file):
    output_file = os.path.splitext(input_file)[0]
    if not os.path.exists(output_file):
        with gzip.open(input_file, "rb") as f_in:
            # Input file has the format xxx.tsv.gz
            with open(output_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
    imdb_url = "https://datasets.imdbws.com"
    filenames = [
        "name.basics.tsv.gz",
        "title.basics.tsv.gz",
        "title.ratings.tsv.gz",
        "title.principals.tsv.gz",
    ]
    for filename in tqdm(filenames):
        url = f"{imdb_url}/{filename}"
        output_file = os.path.join("data", filename)
        download_large_file(url, output_file)
        unzip_file(output_file)
