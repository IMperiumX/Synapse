# TODO: Complementary OT in client side
# TODO: Improve the OT algorithm


class Operation:
    def apply(self, doc):
        raise NotImplementedError

    def transform(self, other):
        raise NotImplementedError


class Insert(Operation):
    """Inserts text at a given position."""

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos

    def apply(self, doc):
        return doc[: self.pos] + self.text + doc[self.pos :]

    def transform(self, other):
        if isinstance(other, Insert):
            if self.pos < other.pos:
                return self
            else:
                return Insert(self.text, self.pos + len(other.text))
        elif isinstance(other, Delete):
            if self.pos <= other.pos:
                return self
            elif self.pos >= other.pos + other.length:
                return Insert(self.text, self.pos - other.length)
            else:
                # XXX: Handle overlapping insert and delete
                self._transform_text(other)
        return self

    def _transform_text(self, other):
        if self.pos < other.pos:
            new_text = self.text
        elif self.pos >= other.pos + other.length:
            new_text = self.text
        else:
            new_text = (
                self.text[: other.pos - self.pos]
                + self.text[other.pos - self.pos + other.length :]
            )
        self.text = new_text


class Delete(Operation):
    """Deletes a range of text."""

    def __init__(self, length, pos):
        self.length = length
        self.pos = pos

    def apply(self, doc):
        return doc[: self.pos] + doc[self.pos + self.length :]

    def transform(self, other):
        if isinstance(other, Insert):
            if self.pos + self.length <= other.pos:
                return self
            elif self.pos >= other.pos:
                return Delete(self.length, self.pos + len(other.text))
            else:
                # Handle overlapping delete and insert (complex case)
                return Delete(self.length, other.pos)
        elif isinstance(other, Delete):
            if self.pos + self.length <= other.pos:
                return self
            elif self.pos >= other.pos + other.length:
                return Delete(self.length, self.pos - other.length)
            elif self.pos < other.pos:
                # Handle overlapping deletes (complex case)
                new_length = self.pos + self.length - other.pos
                return Delete(new_length, self.pos)
            elif self.pos + self.length > other.pos + other.length:
                new_length = other.pos + other.length - self.pos
                return Delete(new_length, self.pos)
            else:
                return None  # Simplified for this example
        return self
