class Cell:
    def __init__(self, data):
        self.data = data
        self.col = None
        self.row = None
        
    def __len__(self):
        return len(str(self.data))

    def render(self):
        return format(str(self.data), f"{self.align}{self.width}")

    def render_divider(self):
        return (
            (":" if self.align in "^" else " ") +
            ("-" * self.width) +
            (":"  if self.align in "^>" else " ")
        )
    @property
    def align(self):
        return self.col.align

    @property
    def width(self):
        return self.col.width


class Slice:
    def __init__(self, cells):
        self.cells = cells
    
    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)


class Col(Slice):
    def __init__(self, cells, align):
        super().__init__(cells)
        for cell in cells:
            cell.col = self
        if align not in "<^>":
            raise ValueError(f"Invalid alignment token: {align}")
        self.align = align
        self.width = max(len(cell) for cell in self.cells)


class Row(Slice):
    def __init__(self, cells):
        super().__init__(cells)
        for cell in cells:
            cell.row = self

    def render(self):
        rendered_cells = (cell.render() for cell in self.cells)
        return "| " + (" | ".join(rendered_cells)) + " |"

    def __str__(self):
        return self.render()


class Header(Row):
    def __init__(self, cells):
        super().__init__(cells)

    def render(self):
        header = super().render()
        divider = self.render_divider()
        return "\n".join((header, divider))

    def render_divider(self):
        rendered_divider_cells = (cell.render_divider() for cell in self.cells)
        return "|" + ("|".join(rendered_divider_cells)) + "|"


def render(rows, aligns = None):
    cells_by_row = [[Cell(cell) for cell in row] for row in rows]
    cells_by_col = list(zip(*cells_by_row))
    num_of_cols = len(cells_by_col)
    if aligns is None:
        aligns = "<" * num_of_cols
    if len(aligns) != num_of_cols:
        raise ValueError(f"Incorrect number of alignment tokens: expected {num_of_cols}, got {len(aligns)}")
    header = Header(cells_by_row[0])
    rows = [Row(cells) for cells in cells_by_row[1:]]
    rows.insert(0, header)    
    cols = [Col(cells, align) for cells, align in zip(cells_by_col, aligns)]

    rendered = "\n".join([str(row) for row in rows])
    return rendered

if __name__ == "__main__":
    print(render([["First","2nd","tired"],[1,2,3],[4,5,6],[7,8,9]]))
    print()
    print(render([["First","2nd","tired"],[1,2,3],[4,5,6],[7,8,9]], "<^>"))
