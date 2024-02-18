from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from spacy.tokens import Doc

from vnerrant.components.alignment import Alignment
from vnerrant.components.classifier import BaseClassifer
from vnerrant.components.merger import BaseMerger
from vnerrant.constants import (
    MAPPING_TYPE_ERROR,
    MERGING_ALL_EQUAL,
    MERGING_ALL_MERGE,
    MERGING_ALL_SPLIT,
    MERGING_RULES,
    Operator,
    SeparatorTypes,
)
from vnerrant.model.edit import Edit


class Annotator:
    """
    Annotator class for automatic annotation of parallel text with ERRANT edits.
    """

    def __init__(
        self,
        lang: str,
        nlp: Any = None,
        merger: BaseMerger = None,
        classifier: BaseClassifer = None,
    ):
        """
        Initialise the annotator with a language id, spacy processing object,
        merging module, and classifier module.
        :param lang: A string language id: e.g. "en"
        :param nlp: A spacy processing object for the language
        :param merger: A merging module for the language
        :param classifier: A classifier module for the language
        """
        self.lang = lang
        self.nlp = nlp

        self.merger = (
            self._import_module(merger, "merger") if merger is None else merger
        )
        self.classifier = (
            self._import_module(classifier, "classifier")
            if classifier is None
            else classifier
        )

    def _import_module(self, module, module_type):
        """
        Import a module from the components directory.
        :param module: A module object
        :param module_type: A string module type
        :return: A module object
        """
        base_path = Path(__file__).resolve().parent
        module_name = f"vnerrant.components.{self.lang}.{module_type}"
        module_path = base_path / "components" / self.lang / f"{module_type}.py"

        if module_path.exists():
            Module = importlib.import_module(module_name).__getattribute__(
                module_type.capitalize(),
            )
            return Module()
        else:
            raise ValueError(f"No {module_type} available for language: {self.lang}")

    @staticmethod
    def normalised_text(text: str, **kwargs) -> str:
        """
        Normalise a text string.
        :param text: A text string
        :return: A normalised text string
        """
        if kwargs.get("lowercase"):
            text = text.lower()

        # Remove new lines and tabs
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        return text

    def preprocess_by_rule(self, text: str, **kwargs) -> Doc | str:
        text = self.normalised_text(text, **kwargs)

        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_space]
        return doc, " ".join(tokens)

    def parse(self, text: str, tokenise: bool = False) -> Doc:
        """
        Parse a text string with spacy.
        :param text: A text string
        :param tokenise: A flag to tokenise the text string
        :return: A spacy Doc object
        """
        if tokenise:
            text = self.nlp(text)
        else:
            text = Doc(self.nlp.vocab, text.split())
            # self.nlp.tagger(text)
            # self.nlp.parser(text)
            text = self.nlp(text)
        return text

    def align(self, orig: str, cor: str, lev: bool = False) -> Alignment:
        """
        Align an original and corrected text string.
        :param orig: An original text string
        :param cor: A corrected text string
        :param lev: A flag to use levenshtein alignment
        :return: An Alignment object
        """
        return Alignment(orig, cor, lev)

    def merge(self, alignment: Alignment, merging: str = MERGING_RULES) -> list[Edit]:
        """
        Merge an alignment into a list of edits.
        :param alignment: An Alignment object
        :param merging: A string merging strategy
        :return: A list of Edit objects
        """
        # rules: Rule-based merging
        if merging == MERGING_RULES:
            edits = self.merger.get_all_rule_merge_edits(
                alignment.orig,
                alignment.cor,
                alignment.align_seq,
            )
        # all-split: Don't merge anything
        elif merging == MERGING_ALL_SPLIT:
            edits = self.merger.get_all_split_edits(
                alignment.orig,
                alignment.cor,
                alignment.align_seq,
            )
        # all-merge: Merge all adjacent non-match ops
        elif merging == MERGING_ALL_MERGE:
            edits = self.merger.get_all_merge_edits(
                alignment.orig,
                alignment.cor,
                alignment.align_seq,
            )
        # all-equal: Merge all edits of the same operation type
        elif merging == MERGING_ALL_EQUAL:
            edits = self.merger.get_all_equal_edits(
                alignment.orig,
                alignment.cor,
                alignment.align_seq,
            )
        # Unknown
        else:
            raise Exception(
                "Unknown merging strategy. Choose from: "
                "rules, all-split, all-merge, all-equal.",
            )
        return edits

    def classify(self, edit: Edit) -> Edit:
        """
        Classify an edit with the classifier.
        :param edit: An Edit object
        :return: An Edit object
        """
        return self.classifier.classify(edit)

    def annotate(
        self,
        orig: Doc,
        cor: Doc,
        lev: bool = False,
        merging: str = "rules",
    ) -> list[Edit]:
        """
        Annotate a pair of original and corrected spacy Doc objects.
        :param orig: An original spacy Doc object
        :param cor: A corrected spacy Doc object
        :param lev: A flag to use levenshtein alignment
        :param merging: A string merging strategy
        :return: A list of Edit objects
        """
        alignment = self.align(orig, cor, lev)
        edits = self.merge(alignment, merging)
        for edit in edits:
            edit = self.classify(edit)
        return edits

    def annotate_with_pre_and_post_processing(
        self,
        orig: str,
        cor: str,
        lev: bool = False,
        merging: str = "rules",
    ) -> list[Edit]:
        """
        Annotate a pair of original and corrected text strings with pre-processing and post-processing.
        :param orig: An original text string
        :param cor: A corrected text string
        :param lev: A flag to use levenshtein alignment
        :param merging: A string merging strategy
        :return: A list of Edit objects
        """

        doc_orig, normalized_orig = self.preprocess_by_rule(orig)
        doc_corr, normalized_corr = self.preprocess_by_rule(cor)

        processed_text = self.parse(normalized_orig)
        corrected_text = self.parse(normalized_corr)
        alignment = self.align(processed_text, corrected_text, lev)
        edits = self.merge(alignment, merging)
        for edit in edits:
            edit = self.classify(edit)
            start_token = edit.o_start
            end_token = edit.o_end

            count_idx = 0
            add_space = 0
            for token in doc_orig:
                if token.is_space:
                    add_space += 1
                    continue
                else:
                    if count_idx == start_token:
                        break
                    else:
                        count_idx += 1

            orig_tokens = doc_orig[start_token + add_space : end_token + add_space]
            edit.o_toks.start_char = orig_tokens.start_char
            edit.o_toks.end_char = orig_tokens.end_char

        edits = self.postprocess_by_rule(orig, edits)
        return edits

    def postprocess_by_rule(
        self,
        orig: str,
        edits: list[Edit] | Edit,
    ) -> list[Edit]:
        """
        Postprocess a list of edits.
        :param orig: An original text string
        :param edits: A list of Edit objects
        :return: A list of Edit objects
        """

        if isinstance(edits, Edit):
            edits = [edits]

        for edit in edits:
            operator = edit.type[0]
            type_error = edit.type[2:]
            type_error = MAPPING_TYPE_ERROR[type_error]

            edit.type = operator + SeparatorTypes.COLON + type_error

            if operator == Operator.MISSING:
                if edit.o_toks.start_char == 0:
                    edit.o_toks.end_char = edit.o_toks.start_char
                    edit.c_str = edit.c_str + " "
                else:
                    edit.o_toks.end_char = edit.o_toks.start_char - 1
                if "PUNC" in type_error and edit.o_toks.start_char != len(orig):
                    edit.o_toks.start_char = edit.o_toks.start_char - 1
                elif "PUNC" in type_error and edit.o_toks.start_char == len(
                    orig,
                ):
                    edit.o_toks.end_char = edit.o_toks.start_char
            elif operator == Operator.UNNECESSARY:
                if "PUNC" not in type_error:
                    edit.o_toks.end_char = edit.o_toks.end_char + 1
        return edits

    def import_edit(
        self,
        orig: str,
        cor: str,
        edit: list,
        min: bool = True,
        old_cat: bool = False,
    ) -> Edit:
        """
        Import an edit from an external source.
        :param orig: An original text string
        :param cor: A corrected text string
        :param edit: An edit list of the form: [o_start, o_end, c_start, c_end]
        :param min: A flag to minimise the edit
        :param old_cat: A flag to use the old error type classification
        :return: An Edit object
        """
        # Undefined error type
        if len(edit) == 4:
            edit_obj = Edit(orig, cor, edit)
        # Existing error type
        elif len(edit) == 5:
            edit_obj = Edit(orig, cor, edit[:4], edit[4])
        # Unknown edit format
        else:
            raise Exception(
                "Edit not of the form: " "[o_start, o_end, c_start, c_end, (cat)]",
            )
        # Minimise edit
        if min:
            edit_obj = edit_obj.minimise()
        # Classify edit
        if not old_cat:
            edit_obj = self.classify(edit_obj)
        return edit_obj
