from textual.app import App, ComposeResult
from textual.widgets import Header

from textual_plotext import PlotextPlot

from main import get_robots

def get_positions(robots, step):
    x_max = 101
    y_max = 103
    positions = []
    for position in [x.step(step, x_max, y_max) for x in robots]:
        positions.append(position)
    return positions



class ScatterApp(App[None]):
    BINDINGS = [
        ("d", "increment()", "increment"),
        ("a", "decrement()", "decrement"),
        ("c", "increment_101()", "increment_101"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("input") as f:
            lines = [line.strip() for line in f.readlines()]
        self.step = 0
        self.robots = get_robots(lines)
        self.plot = PlotextPlot(name="robots")
    def compose(self) -> ComposeResult:
        yield Header()
        yield self.plot

    def action_increment(self):
        self.step += 1
        plt = self.plot.plt
        y = get_positions(self.robots, self.step)
        plt.clear_data()
        plt.scatter([x.x for x in y], [x.y for x in y])
        self.title = f'step {self.step}'
        self.plot.refresh()

    def action_increment_101(self):
        self.step += 101
        plt = self.plot.plt
        y = get_positions(self.robots, self.step)
        plt.clear_data()
        plt.scatter([x.x for x in y], [x.y for x in y])
        self.title = f'step {self.step}'
        self.plot.refresh()

    def action_decrement(self):
        self.step -= 1
        plt = self.plot.plt
        y = get_positions(self.robots, self.step)
        plt.clear_data()
        plt.scatter([x.x for x in y], [x.y for x in y])
        self.title = f'step {self.step}'
        self.plot.refresh()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt
        y = get_positions(self.robots, self.step)
        plt.scatter([x.x for x in y], [x.y for x in y])
if __name__ == "__main__":
    ScatterApp().run()