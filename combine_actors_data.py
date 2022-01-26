import pandas as pd
from datetime import datetime
    

def process_actors_data(keep_alive: bool = True):
    current_year = datetime.now().year

    # Read actors data
    df = pd.read_csv("data/name.basics.tsv", sep="\t")
    df["birthYear"] = pd.to_numeric(df["birthYear"], errors="coerce")
    df["deathYear"] = pd.to_numeric(df["deathYear"], errors="coerce")

    # Prepare and cleanup actors data
    if keep_alive:
        df = df[df["deathYear"].isna()]
    df = df[df.knownForTitles.apply(lambda x: len(x)) > 0]
    df = df.dropna(subset=["primaryProfession"])
    df = df[df.primaryProfession.apply(lambda x: "actor" in x.split(","))]
    df = df[df.knownForTitles != "\\N"]
    df = df.dropna(subset=["birthYear"])
    #df["knownForTitles"] = df["knownForTitles"].apply(lambda x: x.split(","))

    #dfat = df[["nconst", "knownForTitles"]].explode("knownForTitles")
    #dfat.columns = ["nconst", "tconst"]
    dfat = pd.read_csv("data/title.principals.tsv.gz", sep="\t")
    dfat = dfat[dfat.category.isin(["actor", "self"])][["tconst", "nconst"]]

    
    # Get data for the movies/shows the actors were known for
    dftr = pd.read_csv("data/title.ratings.tsv", sep="\t")
    dftb = pd.read_csv("data/title.basics.tsv", sep="\t")
    dftb["startYear"] = pd.to_numeric(dftb["startYear"], errors="coerce")
    dftb["endYear"] = pd.to_numeric(dftb["endYear"], errors="coerce")

    # Estimate last year the show/movie was released (TV shows span several years and might still be active)
    dftb.loc[(dftb.titleType.isin(["tvSeries", "tvMiniSeries"]) & (dftb.endYear.isna())), "lastYear"] = current_year
    dftb["lastYear"] = dftb["lastYear"].fillna(dftb["startYear"])
    dftb = dftb.dropna(subset=["lastYear"])
    dftb = dftb[dftb.isAdult == 0]

    # Aggregate stats for all movies the actor was known for
    dft = pd.merge(dftb, dftr, how="inner", on="tconst")
    del dftb, dftr
    dfat = pd.merge(dfat, dft, how="inner", on="tconst")
    del dft
    dfat["totalRating"] = dfat.averageRating*dfat.numVotes
    dfat = dfat.groupby("nconst").agg({"averageRating": "mean", "totalRating": "sum", "numVotes": "sum", "tconst": "count", "startYear": "min", "lastYear": "max"})

    # Merge everything with actor data and cleanup
    df = df.drop(["deathYear", "knownForTitles", "primaryProfession"], axis=1)
    df = pd.merge(df, dfat, how="inner", on="nconst").sort_values("totalRating", ascending=False)
    df = df.dropna(subset=["birthYear", "startYear", "lastYear"])
    df[["birthYear", "startYear", "lastYear"]] = df[["birthYear", "startYear", "lastYear"]].astype(int)
    df = df.round(2)

    return df
    

if __name__ == "__main__":
    df = process_actors_data()
    df.to_csv("data/imdb_actors.csv", index=False)