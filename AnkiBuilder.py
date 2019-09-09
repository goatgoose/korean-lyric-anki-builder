from lyricsgenius import Genius
from gtts import gTTS
from googletrans import Translator
import genanki


class AnkiBuilder:
    def __init__(self, deck_name, deck_id):
        self.deck_name = deck_name
        self.deck_id = deck_id

        self.genius = Genius("DhLgBRFiLg4HOiABUzSJvGjpTDgX6vwVSFvyV3P6igiKdAhNdvq0VbwnF8QEXxa0")
        self.translator = Translator()

        self.songs = []
        self.translated = {}

        self.model = genanki.Model(
            1313562696, "lyrics-model",
            fields=[
                {"name": "Term"},
                {"name": "Translation"}
            ],
            templates=[
                {
                    "name": "term card",
                    "qfmt": "{{Term}}",
                    "afmt": "{{FrontSide}}<hr id='answer'>{{Translation}}"
                }
            ]
        )

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

    @staticmethod
    def get_hangul_blocks(song):
        lines = []
        for line in song.lyrics.split("\n"):
            blocks_in_line = []

            line = line.strip()
            if line.startswith("["):
                continue

            for word in line.split(" "):
                if AnkiBuilder.block_is_hangul(word) and word:
                    blocks_in_line.append(word)
            if len(blocks_in_line) > 0:
                lines.append(blocks_in_line)

        return lines

    def add_song(self, song):
        self.songs.append(song)

    def translate(self, term):
        if term not in self.translated:
            self.translated[term] = self.translator.translate(term).text

    def build(self):
        hangul = []
        for song in self.songs:
            hangul.append(self.get_hangul_blocks(song))

        for song in hangul:
            for line in song:
                phrase = " ".join(line)
                self.translate(phrase)

                for block in line:
                    self.translate(block)

        deck = genanki.Deck(self.deck_id, self.deck_name)
        for term in self.translated:
            deck.add_note(genanki.Note(
                model=self.model,
                fields=[term, self.translated[term]]
            ))

        genanki.Package(deck).write_to_file("decks/" + self.deck_name + ".apkg")


if __name__ == '__main__':
    builder = AnkiBuilder("Likey", 1768730765)
    builder.add_song(builder.genius.search_song("likey", artist="TWICE"))
    builder.build()
