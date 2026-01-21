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

        # Info window (left panel)
        self.info_frame = Frame(self.root, width=400, height=800, bg="lightgrey")
        self.info_frame.place(x=0, y=0)

        # -------------------------
        # MODE SWITCH BAR
        # -------------------------
        self.mode = StringVar(value="inspector")

        self.top_bar = Frame(self.info_frame, bg="lightgrey")
        self.top_bar.place(x=0, y=0, width=400, height=50)

        self.btn_inspector = Button(
            self.top_bar,
            text="Inspector",
            command=self.show_inspector
        )
        self.btn_inspector.place(x=20, y=10, width=170, height=30)

        self.btn_summon = Button(
            self.top_bar,
            text="Summon",
            command=self.show_summon
        )
        self.btn_summon.place(x=210, y=10, width=170, height=30)

        # -------------------------
        # CONTENT AREA (pages)
        # -------------------------
        self.content = Frame(self.info_frame, bg="lightgrey")
        self.content.place(x=0, y=50, width=400, height=750)

        # Inspector page
        self.inspector_page = Frame(self.content, bg="lightgrey")
        Label(
            self.inspector_page,
            text="Inspector mode",
            bg="lightgrey",
            font=("Arial", 16, "bold")
        ).place(x=20, y=20)

        Label(
            self.inspector_page,
            text="(later: click a block to see its info)",
            bg="lightgrey",
            font=("Arial", 11)
        ).place(x=20, y=60)

        Label(
            self.inspector_page,
            text="Gravity",
            bg="lightgrey",
            font=("Arial", 14)
        ).place(x=20, y=120)
        gravity_entry = Entry(
            self.inspector_page,
            width=10
        )
        gravity_entry.place(x=120, y=120)
        gravity_entry.insert(0, "9.81")  # default value (m/s^2)
        def update_gravity():
            try:
                g = float(gravity_entry.get())
                import simcore
                # physics core expects pixels/s^2; scale from m/s^2
                simcore.set_gravity(g * 100.0)
            except ValueError:
                pass  # ignore invalid input
        gravity_entry.bind("<Return>", lambda event: update_gravity())


        # Summon page
        self.summon_page = Frame(self.content, bg="lightgrey")
        Label(
            self.summon_page,
            text="Summon mode",
            bg="lightgrey",
            font=("Arial", 16, "bold")
        ).place(x=20, y=20)

        # Your summon button goes inside summon_page now
        self.summon_button = Button(
            self.summon_page,
            text="Summon Block",
            command=on_summon
        )
        self.summon_button.place(x=150, y=80)

        # start in inspector mode
        self.show_inspector()

    # -------------------------
    # PAGE SWITCHING
    # -------------------------
    def _hide_pages(self):
        self.inspector_page.place_forget()
        self.summon_page.place_forget()

    def _update_button_states(self):
        if self.mode.get() == "inspector":
            self.btn_inspector.config(relief=SUNKEN, state=DISABLED)
            self.btn_summon.config(relief=RAISED, state=NORMAL)
        else:
            self.btn_inspector.config(relief=RAISED, state=NORMAL)
            self.btn_summon.config(relief=SUNKEN, state=DISABLED)

    def show_inspector(self):
        self.mode.set("inspector")
        self._hide_pages()
        self.inspector_page.place(x=0, y=0, width=400, height=750)
        self._update_button_states()

    def show_summon(self):
        self.mode.set("summon")
        self._hide_pages()
        self.summon_page.place(x=0, y=0, width=400, height=750)
        self._update_button_states()

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
