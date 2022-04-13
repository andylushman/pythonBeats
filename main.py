from typing import Optional
from fastapi import FastAPI
import csv
from pydantic import BaseModel

app = FastAPI()

artists_file = 'artists.csv'


class Artist(BaseModel):
    name: str
    location: Optional[str] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/artists")
def read_artists():
    with open(artists_file, 'r') as csvfile:
        data_reader = csv.reader(csvfile)
        artists = [{"name": row[0], "location": row[1]} for row in data_reader]
        return artists


@app.post("/artists")
def create_artist(artist: Artist):
    with open(artists_file, 'a', newline="") as csvfile:
        data_writer = csv.writer(csvfile)
        data_writer.writerow([artist.name, artist.location])


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
