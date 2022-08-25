"""An example component that uses the matcher to store span groups."""

from typing import Any, Dict, List

import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc


@spacy.registry.misc("example.movie_matches.v1")
def movie_matches() -> List[List[Dict[str, Any]]]:
    """The match rules for use in the MovieMatcher component."""
    movie_matches = [
        [
            {"LOWER": {"IN": ["film", "films", "movie", "movies", "cinema"]}},
        ]
    ]
    return movie_matches


@Language.factory(
    "example.movie_matcher.v1",
    default_config={
        "matches": {
            "@misc": "example.movie_matches.v1",
        },
        "span_key": "movie",
    },
)
def create_movie_matcher_component(
    nlp: Language, name: str, matches: List[List[Dict[str, Any]]], span_key: str
) -> "MovieMatcher":
    """Factory for creating the movie_matcher.

    Args:
        nlp (Language): Pipeline (passed)
        name (str): Component name (passed)
        matches (List[List[Dict[str, Any]]]): A list of movie match rules.
        span_key (str): Span key to store the matches on.

    Returns:
        MovieMatcher: The MovieMatcher component.
    """
    return MovieMatcher(nlp, matches, span_key)


class MovieMatcher:
    """The MovieMatcher is an example component that uses the matcher
    to extract movie related words from texts.
    """

    def __init__(
        self, nlp: Language, matches: List[List[Dict[str, Any]]], span_key: str
    ):
        """Initialize the MovieMatcher.

        Args:
            nlp (Language): Pipeline (passed)
            matches (List[List[Dict[str, Any]]]): A list of movie match rules.
            span_key (str): Span key to store the matches on.
        """
        self.matcher = Matcher(nlp.vocab, validate=True)
        self.matcher.add("movie_matches", matches)
        self.span_key = span_key

    def __call__(self, doc: Doc) -> Doc:
        """Runs the matcher on an input doc, adding the movie spans to the
        doc.spans[span_key] span group.

        Args:
            doc (Doc): The doc to run the matcher on.

        Returns:
            Doc: The output doc, with movie spans on the doc.spans[span_key] span group.
        """
        spans = []
        for match_id, start, end in self.matcher(doc):
            # We don't use the string_id, but if you have multiple
            # match rules it can be helpful to refer to them by the string id
            string_id = doc.vocab.strings[match_id]  # noqa: see above
            spans.append(doc[start:end])
        doc.spans[self.span_key] = spans
        return doc
