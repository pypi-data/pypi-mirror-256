from num2words import num2words
from number_parser import parse_ordinal

_old_list = list
_old_range = range


class list:
    _list: _old_list

    def __init__(self, *values):
        if len(values) > 0:
            self._list = _old_list(values)
        else:
            self._list = _old_list()

    def append(self, value):
        self._list.append(value)

    def extend(self, value):
        self._list.extend(value)

    def _to_boring_index(self, perfect_index):
        boring_index = parse_ordinal(perfect_index)
        if boring_index == 0:
            raise IndexError("Zeroth 🖕!")
        if boring_index == None:
            if perfect_index == "middle":
                boring_index = len(self._list) // 2
            elif perfect_index == "last":
                boring_index = len(self._list) - 1
        else:
            boring_index -= 1

        if boring_index == None:
            raise IndexError(f"Index: {perfect_index} is not valid")

        if boring_index >= len(self._list):
            raise IndexError(f"Index Out of Bounds")
        return boring_index

    def __getitem__(self, subscript):
        if isinstance(subscript, str):
            if subscript == "all":
                return self._list
            boring_start = self._to_boring_index(subscript)
            return self._list[boring_start]
        elif isinstance(subscript, slice):
            start = subscript.start
            stop = subscript.stop
            step = subscript.step
            if start is None:
                boring_start = 0
            else:
                boring_start = self._to_boring_index(start)
            if stop is None:
                boring_stop = len(self._list)
            else:
                boring_stop = self._to_boring_index(stop)
            if step is None:
                boring_step = 1
            else:
                boring_step = self._to_boring_index(step) + 1

            return self._list[boring_start:boring_stop:boring_step]
        raise TypeError("Invalid index type")

    def __iter__(self):
        for i in self._list:
            yield i

    def __setitem__(self, index: str, value):
        boring_index = parse_ordinal(index)
        if boring_index == None:
            if index == "middle":
                boring_index = len(self._list) // 2
            elif index == "last":
                boring_index = len(self._list) - 1
        else:
            boring_index -= 1

        if boring_index == None:
            raise IndexError(f"Index: {index} is not valid")

        if boring_index >= len(self._list):
            raise IndexError(f"Index Out of Bounds")

        self._list[boring_index] = value

    def __len__(self):
        return len(self._list)


class range:
    start: str
    end: str
    step: str

    def __init__(self, __start, __end=None, __step=None):

        self.start = __start
        if __end is None:
            self.end = __start
            self.start = "first"
        else:
            self.end = __end

        if __step is None:
            self.step = "first"
        else:
            self.step = __step
        boring_start = parse_ordinal(self.start)
        boring_end = parse_ordinal(self.end)
        boring_step = parse_ordinal(self.step)
        if boring_start == 0 or boring_end == 0 or boring_step == 0:
            raise IndexError("Zeroth 🖕!")
        if boring_start is None or boring_end is None or boring_step is None:
            raise ValueError("Indexes must be ordinal numbers")

    def __iter__(self):
        boring_start = parse_ordinal(self.start)
        boring_end = parse_ordinal(self.end)
        boring_step = parse_ordinal(self.step)
        assert boring_start is not None
        assert boring_end is not None
        assert boring_step is not None
        for i in _old_range(boring_start, boring_end + 1, boring_step):
            yield num2words(i, to="ordinal")

    def __repr__(self) -> str:
        step_part = ""
        if self.step != "first":
            step_part = f", {self.step}"
        return f"range({self.start}, {self.end}{step_part})"
