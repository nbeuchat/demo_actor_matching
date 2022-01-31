import face_recognition
import json
import annoy
from typing import Tuple

EMBEDDING_DIMENSION = 128
ANNOY_INDEX_FILE = "models/actors_annoy_index.ann"
ANNOY_METADATA_FILE = "models/actors_annoy_metadata.json"
ANNOY_MAPPING_FILE = "models/actors_mapping.json"


def load_annoy_index(
    index_file=ANNOY_INDEX_FILE,
    metadata_file=ANNOY_METADATA_FILE,
    mapping_file=ANNOY_MAPPING_FILE,
) -> Tuple[annoy.AnnoyIndex, dict]:
    """Load annoy index and associated mapping file"""
    with open(metadata_file) as f:
        annoy_index_metadata = json.load(f)

    annoy_index = annoy.AnnoyIndex(f=EMBEDDING_DIMENSION, **annoy_index_metadata)
    annoy_index.load(index_file)

    with open(mapping_file) as f:
        mapping = json.load(f)
        mapping = {int(k): v for k, v in mapping.items()}
    return annoy_index, mapping


def analyze_image(
    image, annoy_index, n_matches: int = 1, num_jitters: int = 1, model: str = "large"
):
    """Extract face location, embeddings, and top n_matches matches"""
    face_locations = face_recognition.face_locations(
        image, number_of_times_to_upsample=1
    )
    if not face_locations:
        face_locations = face_recognition.face_locations(image, model="cnn")
    embeddings = face_recognition.face_encodings(
        image, num_jitters=num_jitters, model=model, known_face_locations=face_locations
    )
    matches = []
    distances = []
    for emb in embeddings:
        m, d = annoy_index.get_nns_by_vector(emb, n_matches, include_distances=True)
        matches.append(m)
        distances.append(d)
    return [
        dict(embeddings=e, matches=m, distances=d, face_locations=f)
        for e, m, d, f in zip(embeddings, matches, distances, face_locations)
    ]
