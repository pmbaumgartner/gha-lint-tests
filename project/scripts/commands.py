"""Any scripts that need to be run for this pipline can go here,
then they're usually called with arguments from the project.yml file
"""

from pathlib import Path

from subprocess import run

import spacy
import typer
from spacy.tokens import DocBin

import wasabi

app = typer.Typer()

msg = wasabi.Printer()


def _tsv_check(filename: Path):
    if filename.suffix != ".tsv":
        raise typer.BadParameter(".tsv file required")
    return filename


def _spacy_check(filename: Path):
    if filename.suffix != ".spacy":
        raise typer.BadParameter(".spacy file required")
    return filename


@app.command()
def convert(
    input_file: Path = typer.Argument(
        ..., help="The input file (.tsv) to convert from", callback=_tsv_check
    ),
    output_file: Path = typer.Argument(
        ..., help="The output file (.spacy) to convert to", callback=_spacy_check
    ),
):
    """Converts a data (.tsv) to the spaCy DocBin (.spacy) format.

    This is just an example to illustrate typer,
    your data will probably not be a TSV or classification problem.
    """
    input_lines = input_file.read_text().splitlines()

    nlp = spacy.blank("en")
    db = DocBin()
    for line in input_lines:
        text, label = line.split("\t")
        doc = nlp(text)
        positive = label == "1"
        doc.cats = {"POSITIVE": 1 if positive else 0, "NEGATIVE": 0 if positive else 1}
        db.add(doc)

    db.to_disk(output_file)


@app.command()
def git_lfs_installed():
    """Checks if Git LFS is installed.

    This is an example command and can be removed in a real project.
    It is here to illustrate the case where you have a typer script with
    multiple commands.
    """
    cmd = run(["git", "lfs", "-v"], capture_output=True)

    if cmd.returncode != 0:
        msg.fail("Git LFS Not Installed. See: https://git-lfs.github.com/")
    else:
        msg.good(f"Git LFS Installed!\n{cmd.stdout.decode()}")


if __name__ == "__main__":
    app()
