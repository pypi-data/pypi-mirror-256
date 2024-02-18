from __future__ import annotations


def noop_edit(id: int = 0) -> str:
    """
    Create a noop edit string.
    :param id: The id number of the annotation.
    :return: A noop edit string.
    """
    return "A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||" + str(id)


def convert_edits_to_dict(edits: list[str]) -> dict:
    """
    Convert a list of edit strings to a dictionary of edits.
    :param edits: A list of edit strings.
    :return: A dictionary of edits.
    """
    edit_dict = {}
    for edit in edits:
        edit = edit.split("|||")
        span = edit[0][2:].split()  # [2:] ignore the leading "A "
        start = int(span[0])
        end = int(span[1])
        cat = edit[1]
        cor = edit[2]
        id = edit[-1]
        # Save the useful info as a list
        proc_edit = [start, end, cat, cor]
        # Save the proc_edit inside the edit_dict using coder id
        if id in edit_dict.keys():
            edit_dict[id].append(proc_edit)
        else:
            edit_dict[id] = [proc_edit]
    return edit_dict


def convert_m2_to_edits(sent: str) -> list:
    """
    Convert an m2 string to a list of edit strings.
    :param sent: An m2 string.
    :return: A list of edit strings.
    """
    out_edits = []
    # Get the edit lines from an m2 block.
    edits = sent.split("\n")[1:]
    # Loop through the edits
    for edit in edits:
        # Preprocessing
        edit = edit[2:].split("|||")  # Ignore "A " then split.
        span = edit[0].split()
        start = int(span[0])
        end = int(span[1])
        cat = edit[1]
        cor = edit[2]
        coder = int(edit[-1])
        out_edit = [start, end, cat, cor, coder]
        out_edits.append(out_edit)
    return out_edits


def get_corrected_text_and_edits(
    orig_text: str,
    edits: list[str],
) -> tuple[str, list[str]]:
    """
    Apply the edits to the original text to generate the corrected text.
    :param orig_text: The original text string.
    :param edits: A list of edit strings.
    :return: The corrected text and a list of edit strings.
    """
    # Copy orig_text; we will apply edits to it to make cor
    corr_text = orig_text.split()
    new_edits = []
    offset = 0
    # Sort the edits by offsets before processing them
    edits = sorted(edits, key=lambda e: (e[0], e[1]))
    # Loop through edits: [o_start, o_end, cat, cor_str]
    for edit in edits:
        o_start = edit[0]
        o_end = edit[1]
        cat = edit[2]
        cor_toks = edit[3].split()
        # Detection edits
        if cat in {"Um", "UNK"}:
            # Save the pseudo correction
            det_toks = cor_toks[:]
            # But temporarily overwrite it to be the same as orig
            cor_toks = orig_text.split()[o_start:o_end]
        # Apply the edits
        corr_text[o_start + offset : o_end + offset] = cor_toks
        # Get the cor token start and end offsets in cor
        c_start = o_start + offset
        c_end = c_start + len(cor_toks)
        # Keep track of how this affects orig edit offsets
        offset = offset - (o_end - o_start) + len(cor_toks)
        # Detection edits: Restore the pseudo correction
        if cat in {"Um", "UNK"}:
            cor_toks = det_toks
        # Update the edit with cor span and save
        new_edit = [o_start, o_end, c_start, c_end, cat, " ".join(cor_toks)]
        new_edits.append(new_edit)
    return " ".join(corr_text), new_edits


class Edit:
    """
    An object representing an edit.
    """

    def __init__(self, orig: str, cor: str, edit: list, type="NA"):
        """
        Initialise the edit object with the orig and cor token spans and
        the error type. If the error type is not known, it is set to "NA".
        :param orig: The original text string parsed by spacy.
        :param cor: The corrected text string parsed by spacy.
        :param edit: A token span edit list: [o_start, o_end, c_start, c_end].
        :param type: The error type string, if known.
        """
        # Orig offsets, spacy tokens and string
        self.o_start = edit[0]
        self.o_end = edit[1]
        self.o_toks = orig[self.o_start : self.o_end]
        self.o_str = self.o_toks.text if self.o_toks else ""
        # Cor offsets, spacy tokens and string
        self.c_start = edit[2]
        self.c_end = edit[3]
        self.c_toks = cor[self.c_start : self.c_end]
        self.c_str = self.c_toks.text if self.c_toks else ""
        # Error type
        self.type = type

    # Minimise the edit; e.g. [a b -> a c] = [b -> c]
    def minimise(self):
        """
        Minimise the edit by removing common tokens from the start and end of
        the edit spans. This is done by adjusting the start and end offsets
        and removing tokens from the token spans.
        :return: The minimised edit object.
        Examples:
            >>> e = Edit("a b c", "a d c", [0, 3, 0, 3])
            >>> print(e)
            Orig: [0, 3, 'a b c'], Cor: [0, 3, 'a d c'], Type: 'NA'
            >>> e.minimise()
            >>> print(e)
            Orig: [1, 2, 'b'], Cor: [1, 2, 'd'], Type: 'NA'
        """
        # While the first token is the same on both sides
        while (
            self.o_toks and self.c_toks and self.o_toks[0].text == self.c_toks[0].text
        ):
            # Remove that token from the span, and adjust the start offsets
            self.o_toks = self.o_toks[1:]
            self.c_toks = self.c_toks[1:]
            self.o_start += 1
            self.c_start += 1
        # Do the same for the last token
        while (
            self.o_toks and self.c_toks and self.o_toks[-1].text == self.c_toks[-1].text
        ):
            self.o_toks = self.o_toks[:-1]
            self.c_toks = self.c_toks[:-1]
            self.o_end -= 1
            self.c_end -= 1
        # Update the strings
        self.o_str = self.o_toks.text if self.o_toks else ""
        self.c_str = self.c_toks.text if self.c_toks else ""
        return self

    def to_m2(self, id=0):
        """
        Convert the edit to an m2 string. If the error type is "NA", it is
        converted to "UNK".
        :param id: The id number of the annotation.
        """
        span = " ".join(["A", str(self.o_start), str(self.o_end)])
        cor_toks_str = " ".join([tok.text for tok in self.c_toks])
        return "|||".join(
            [span, self.type, cor_toks_str, "REQUIRED", "-NONE-", str(id)],
        )

    # Edit object string representation
    def __str__(self):
        """
        Print the edit object in a readable format.
        """
        orig = "Orig: " + str([self.o_start, self.o_end, self.o_str])
        cor = "Cor: " + str([self.c_start, self.c_end, self.c_str])
        type = "Type: " + repr(self.type)
        return ", ".join([orig, cor, type])
