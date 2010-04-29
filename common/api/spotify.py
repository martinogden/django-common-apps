import spotimeta

def artist_link(artist):
  spotify = spotimeta.search_artist(artist.name)
  if spotify['total_results'] > 0:
    for a in spotify['result']:
      if a['name'] == artist.name:
        artist.spotify_link = a['href']