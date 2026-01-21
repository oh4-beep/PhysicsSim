import time
from gui import GUI
import simcore

TARGET_FPS = 60
FRAME_MS = int(1000 / TARGET_FPS)

def main():
    world = simcore.GameControl()

    def summon_block():
        # spawn near the top, random-ish x if you want later
        world.add_block(100, 50)

    gui = GUI(on_summon=summon_block)

    last = time.perf_counter()

    def tick():
        nonlocal last
        now = time.perf_counter()
        dt = now - last
        last = now

        if dt > 0.05:
            dt = 0.05

        world.update(dt)

        blocks = world.get_blocks()
        gui.render(blocks)

        gui.root.after(FRAME_MS, tick)

    tick()
    gui.root.mainloop()

if __name__ == "__main__":
    main()
