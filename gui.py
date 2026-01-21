from tkinter import *

class GUI:
    def __init__(self, on_summon):
        self.root = Tk()
        self.root.geometry("1200x800")

        # Simulation window
        self.canvas_width = 800
        self.canvas_height = 800
        self.canvas = Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white"
        )
        self.canvas.place(x=401, y=0)

        # store canvas rectangles by block id
        self.block_rects = {}

        # Info window
        self.info_frame = Frame(self.root, width=400, height=800, bg="lightgrey")
        self.info_frame.place(x=0, y=0)

        # Button summons a REAL C++ block
        self.summon_button = Button(
            self.info_frame,
            text="Summon Block",
            command=on_summon
        )
        self.summon_button.place(x=150, y=50)

    def render(self, blocks):
        """
        blocks: list of dicts:
        {
            "id": int,
            "x": float,
            "y": float,
            "width": float,
            "height": float
        }
        """
        for b in blocks:
            bid = b["id"]

            x1 = b["x"]
            y1 = b["y"]
            x2 = x1 + b["width"]
            y2 = y1 + b["height"]

            if bid not in self.block_rects:
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="blue"
                )
                self.block_rects[bid] = rect_id
            else:
                self.canvas.coords(
                    self.block_rects[bid],
                    x1, y1, x2, y2
                )
