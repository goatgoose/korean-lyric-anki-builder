from lyricsgenius import Genius
from gtts import gTTS


class AnkiBuilder:
    def __init__(self):
        self.genius = Genius("DhLgBRFiLg4HOiABUzSJvGjpTDgX6vwVSFvyV3P6igiKdAhNdvq0VbwnF8QEXxa0")

    @staticmethod
    def char_is_hangul(char):
        value = ord(char)

        # https://jrgraphix.net/research/unicode_blocks.php
        return 0x1100 <= value <= 0x11FF or 0x3130 <= value <= 0x318F or 0xAC00 <= value <= 0xD7AF

    @staticmethod
    def block_is_hangul(block):
        for char in block:
            if not AnkiBuilder.char_is_hangul(char):
                return False
        return True

    def get_hangul_lyrics(self, song_name, artist=""):
        song = self.genius.search_song(song_name, artist=artist)

        words = []
        for line in song.lyrics.split():
            line = line.strip()
            if line.startswith("["):
                continue

            for word in line.split(" "):
                if AnkiBuilder.block_is_hangul(word):
                    words.append(word)

        return words

    def build(self):
        pass


if __name__ == '__main__':
    builder = AnkiBuilder()
    print(builder.get_hangul_lyrics("hold me tight", artist="TWICE"))
