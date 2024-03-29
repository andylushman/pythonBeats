from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException
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
        artists = [{"id": row[0], "name": row[1], "location": row[2]} for row in data_reader]
        return artists


@app.post("/artists")
def create_artist(artist: Artist):
    with open(artists_file, 'a', newline="") as csvfile:
        data_writer = csv.writer(csvfile)
        initial_uuid = uuid.uuid1()
        four_digit_id = int(str(initial_uuid.int)[:4])
        artist_key = four_digit_id
        data_writer.writerow([artist_key, artist.name, artist.location])


@app.get("/items/{item_id}")
def read_item(item_id: str, q: Optional[str] = None):
    with open(artists_file, 'r') as csvfile:
        data_reader = csv.reader(csvfile)
        artists = [element for element in data_reader if element[0] == item_id]
        if not artists:
            raise HTTPException(status_code=404, detail="Item not found")
        artist = artists[0]

        return {"key": artist[0], "name": artist[1], "location": artist[2]}
