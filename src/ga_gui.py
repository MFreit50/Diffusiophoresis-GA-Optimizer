import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        # Bind the mouse wheel event for vertical scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _on_mouse_wheel(self, event):
        """Scroll vertically when the mouse wheel is used."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class GA_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GA Progress")
        self.root.geometry("1400x800")  # Wider and taller window size

        self.scrollable_frame = ScrollableFrame(root)
        self.scrollable_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.figure = Figure(figsize=(12, 15), dpi=100)

        # Adjust spacing between subplots
        self.figure.subplots_adjust(hspace=0.4)  # Slightly increase vertical space between graphs

        # Create subplots with labels
        self.ax1 = self.figure.add_subplot(311)
        self.ax1.set_title("Best Fitness Over Generations")
        self.ax1.set_xlabel("Generations")
        self.ax1.set_ylabel("Best Fitness")

        self.ax2 = self.figure.add_subplot(312)
        self.ax2.set_title("Mutation Rate Over Generations")
        self.ax2.set_xlabel("Generations")
        self.ax2.set_ylabel("Mutation Rate")

        self.ax3 = self.figure.add_subplot(313)
        self.ax3.set_title("Unique Fitness Scores Over Generations")
        self.ax3.set_xlabel("Generations")
        self.ax3.set_ylabel("Unique Fitness Scores")

        self.line_best, = self.ax1.plot([], [], label="Best Fitness", color='blue')
        self.line_mutation, = self.ax2.plot([], [], label="Mutation Rate", color='green')
        self.line_unique, = self.ax3.plot([], [], label="Unique Fitness Scores", color='orange')

        self.generation_list = []
        self.best_fitness_list = []
        self.mutation_rate_list = []
        self.unique_fitness_list = []

        self.canvas = FigureCanvasTkAgg(self.figure, self.scrollable_frame.scrollable_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()

        self.console = ScrolledText(root, wrap=tk.WORD, width=40, height=40)
        self.console.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Horizontal scrollbar to control x-axis range, now placed at the bottom-left of the visible area
        self.h_scrollbar = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=self._on_scroll)
        self.h_scrollbar.place(x=10, rely=0.97, relwidth=0.7)  # Positioned to the bottom-left

        self.max_generations_to_display = 100
        self.display_start = 0
        self.total_generations = 0

        self.auto_scroll = True  # Automatically follow new data unless manually scrolled
        self._init_hover()

    def _on_scroll(self, value):
        """Handle horizontal scrollbar interaction."""
        scroll_value = int(float(value))
        self.display_start = scroll_value
        self.auto_scroll = False  # Disable auto-follow when manually scrolling
        self.update_plots()

    def update_plots(self):
        """Update the visible range of the plots according to the scrollbar value."""
        if self.auto_scroll:
            self.display_start = max(0, self.total_generations - self.max_generations_to_display)

        x_min = max(0, self.display_start)
        x_max = x_min + self.max_generations_to_display

        display_generations = self.generation_list[x_min:x_max]

        self.line_best.set_data(display_generations, self.best_fitness_list[x_min:x_max])
        self.line_mutation.set_data(display_generations, self.mutation_rate_list[x_min:x_max])
        self.line_unique.set_data(display_generations, self.unique_fitness_list[x_min:x_max])

        # Adjust x-axis limits to fit the selected range
        self.ax1.set_xlim(x_min, x_max)
        self.ax2.set_xlim(x_min, x_max)
        self.ax3.set_xlim(x_min, x_max)

        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()

        self.canvas.draw()

    def _init_hover(self):
        """Initialize hover annotations for each plot."""
        self.annotations = [None, None, None]
        self.annotations[0] = self.ax1.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                                                bbox=dict(boxstyle="round", fc="w"),
                                                arrowprops=dict(arrowstyle="->"))
        self.annotations[1] = self.ax2.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                                                bbox=dict(boxstyle="round", fc="w"),
                                                arrowprops=dict(arrowstyle="->"))
        self.annotations[2] = self.ax3.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                                                bbox=dict(boxstyle="round", fc="w"),
                                                arrowprops=dict(arrowstyle="->"))
        
        for annotation in self.annotations:
            annotation.set_visible(False)
        
        self.canvas.mpl_connect("motion_notify_event", self._on_hover)

    def _on_hover(self, event):
        """Display hover annotations for the nearest data point."""
        visible = False
        for i, (ax, line, data_list) in enumerate([(self.ax1, self.line_best, self.best_fitness_list),
                                                   (self.ax2, self.line_mutation, self.mutation_rate_list),
                                                   (self.ax3, self.line_unique, self.unique_fitness_list)]):
            if event.inaxes == ax:
                xdata = self.generation_list
                ydata = data_list
                if xdata:
                    dist = [(abs(event.xdata - x), i) for i, x in enumerate(xdata)]
                    closest_idx = min(dist, key=lambda d: d[0])[1]
                    x, y = xdata[closest_idx], ydata[closest_idx]
                    self.annotations[i].xy = (x, y)
                    self.annotations[i].set_text(f"({x}, {y:.3f})")
                    self.annotations[i].set_visible(True)
                    visible = True
                    break
        if not visible:
            for annotation in self.annotations:
                annotation.set_visible(False)
        self.canvas.draw_idle()

    def update(self, data):
        generation = data['generation']
        best_fitness = data['best_fitness']
        mutation_rate = data['mutation_rate']
        unique_fitness_results = data['unique_fitness_scores']

        self.generation_list.append(generation)
        self.best_fitness_list.append(best_fitness)
        self.mutation_rate_list.append(mutation_rate)
        self.unique_fitness_list.append(unique_fitness_results)

        self.total_generations = len(self.generation_list)

        # Update the scrollbar maximum to match the total generations
        self.h_scrollbar.config(to=max(0, self.total_generations - self.max_generations_to_display))

        if self.auto_scroll:
            self.display_start = max(0, self.total_generations - self.max_generations_to_display)

        self.update_plots()

        self.console.insert(tk.END, f'\nGeneration {generation}\n')
        self.console.insert(tk.END, f'Best Fitness: {best_fitness}\n')
        self.console.insert(tk.END, f'Mutation Rate: {mutation_rate:.3f}\n')
        self.console.insert(tk.END, f'Unique Fitness Scores: {unique_fitness_results}\n')
        self.console.yview(tk.END)  # Auto scroll to the latest entry