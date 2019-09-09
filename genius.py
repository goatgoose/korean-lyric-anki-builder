import lyricsgenius
genius = lyricsgenius.Genius("DhLgBRFiLg4HOiABUzSJvGjpTDgX6vwVSFvyV3P6igiKdAhNdvq0VbwnF8QEXxa0")
song = genius.search_song("likey", artist="TWICE")

print(song.lyrics)
song.save_lyrics(verbose=False)
