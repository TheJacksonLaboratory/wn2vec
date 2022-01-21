



from typing import DefaultDict


class SynonymMapper:

    def __init__(self, counter):
        if not isinstance(counter, DefaultDict):
            raise ValueError("Need to pass default dictionary with counts")
        # TODO --