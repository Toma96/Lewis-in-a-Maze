from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import netgraph
from random import *
from sqlite3 import *
matplotlib.use("TkAgg")

BUTTON_FONT = ("Chiller", 32, "italic")
CURSOR = "hand2"
INSTR_LABEL = "Lewis is confronted by a series of odd mazes. For each maze upon him," \
              " he gets the respective map.\n\n The maze is solved only after each room" \
              " is visited EXACTLY once. \n\n Additionally, some paths are" \
              " marked as the ones that absolutely need to be crossed. \nSome mazes won't be solvable" \
              " and for these, you have to state so by pressing the button 'Unsolvable'. \nHowever, " \
              "beware because pressing the button when the maze is solvable will result " \
              "in losing time.\n\n" \
              "Lewis, who just happens to be a professional Formula 1 driver as well, \nwants" \
              " to solve as many mazes as possible in the given time, and collect as many points as he can. "
DIFFS_LABEL = "Difficulties go as follows: \n\n" \
              "EASY: \t4-5 rooms\t\tPoints x1\n\n" \
              "MEDIUM: \t6-7 rooms\t\tPoints x2\n\n" \
              "HARD: \t8-9 rooms\t\tPoints x3"


class MainApp(Tk):

    def __init__(self, *args, **kwargs):

        super(MainApp, self).__init__(*args, **kwargs)

        Tk.wm_title(self, "Lewis in a maze")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.points = 0
        self.connector = connect("Highscores.db")
        self.cursor = self.connector.cursor()

        for F in (MainMenuPage, HighscoresPage, InstructionsPage,
                  SelectDiffPage, CustomGraphPage, GamePage, SaveToHighscoresPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenuPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainMenuPage(Frame):

    def __init__(self, parent, controller):
        # super(MainMenuPage, self).__init__(parent)
        Frame.__init__(self, parent)

        title_label = Label(self, text="Lewis in a maze", font=("Chiller", 128, "bold", "italic"))
        title_label.pack(pady=15, padx=15)

        button_play = Button(self, text="Play", font=BUTTON_FONT, width=10, bg="green",
                             cursor=CURSOR, command=lambda: controller.show_frame(SelectDiffPage))
        button_play.pack(padx=15, pady=15)

        button_highs = Button(self, text="Highscores", font=BUTTON_FONT, width=10, bg="black", fg="white",
                              cursor=CURSOR, command=lambda: controller.show_frame(HighscoresPage))
        button_highs.pack(padx=15, pady=15)

        button_instr = Button(self, text="Instructions", font=BUTTON_FONT, width=10, bg="cyan",
                              cursor=CURSOR, command=lambda: controller.show_frame(InstructionsPage))
        button_instr.pack(padx=15, pady=15)

        # button_custom = Button(self, text="My graphs", font=BUTTON_FONT, width=10, bg="blue",
        #                         cursor=CURSOR, command=lambda: controller.show_frame(CustomGraphPage))
        # button_custom.pack(padx=15, pady=15)

        button_quit = Button(self, text="Quit", font=BUTTON_FONT, width=10, bg="white",
                             cursor=CURSOR, command=parent.quit)
        button_quit.pack(padx=15, pady=15)


class HighscoresPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        title_label = Label(self, text="Hall of Fame", font=("Chiller", 128, "bold", "italic"))
        title_label.grid(row=0, column=0, columnspan=3)

        rank_label = Label(self, text="Rank", font=('Chiller', 64, "bold", "italic"))
        rank_label.grid(row=1, column=0)
        name_label = Label(self, text="Name", font=('Chiller', 64, "bold", "italic"))
        name_label.grid(row=1, column=1)
        points_label = Label(self, text="Points", font=('Chiller', 64, "bold", "italic"))
        points_label.grid(row=1, column=2)

        self.score_labels = [Label(self, text="", font=('Arial', 16)) for _i in range(30)]
        for i, label in enumerate(self.score_labels):
            label.grid(row=i//3 + 2, column=i%3)

        self.button_back = Button(self, text="Back", font=BUTTON_FONT, width=10, bg="white", cursor=CURSOR)

        self.update_scores()

    def update_scores(self):
        query = "SELECT * FROM Highscores ORDER BY Points DESC LIMIT 10"
        table = self.controller.cursor.execute(query)
        rank = 1
        index = 0
        for entry in table:
            self.score_labels[index].config(text=str(rank))
            index += 1
            self.score_labels[index].config(text=entry[1])
            index += 1
            self.score_labels[index].config(text=str(entry[2]))
            index += 1

            rank += 1

        self.button_back.config(command=lambda: self.controller.show_frame(MainMenuPage))
        self.button_back.grid(row=rank+1, column=1)


class InstructionsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        title_label = Label(self, text="Lewis in a maze", font=("Chiller", 128, "bold", "italic"))
        title_label.pack(pady=15, padx=15)

        instr_label = Label(self, text=INSTR_LABEL, font=('Arial', 16))
        instr_label.pack(pady=15, padx=15)

        diffs_label = Label(self, text=DIFFS_LABEL, font=('Arial', 16))
        diffs_label.pack(pady=15, padx=15)

        button_back = Button(self, text="Back", font=BUTTON_FONT, width=10, bg="white", cursor=CURSOR, command=lambda: controller.show_frame(MainMenuPage))
        button_back.pack(padx=15, pady=10)


class SelectDiffPage(Frame):

    def __init__(self, parent, controller):
        # super(SelectDiffPage, self).__init__(parent)
        Frame.__init__(self, parent)
        self.controller = controller

        label_diff = Label(self, text="Select difficulty:", font=("Chiller", 128, "bold", "italic"))
        label_diff.pack(padx=15, pady=15)

        button_easy = Button(self, text="Easy", font=BUTTON_FONT, width=10, bg="green", cursor=CURSOR, command=lambda diff="easy": self.pick_diff(diff))
        button_easy.pack(padx=15, pady=15)

        button_medium = Button(self, text="Medium", font=BUTTON_FONT, width=10, bg="cyan", cursor=CURSOR, command=lambda diff="medium": self.pick_diff(diff))
        button_medium.pack(padx=15, pady=15)

        button_hard = Button(self, text="Hard", font=BUTTON_FONT, width=10, bg="black", fg="white", cursor=CURSOR, command=lambda diff="hard": self.pick_diff(diff))
        button_hard.pack(padx=15, pady=15)

        button_back = Button(self, text="Back", font=BUTTON_FONT, width=10, bg="white", cursor=CURSOR, command=lambda: controller.show_frame(MainMenuPage))
        button_back.pack(padx=15, pady=100)

    def pick_diff(self, diff):
        self.controller.frames[GamePage].difficulty = diff
        self.controller.show_frame(GamePage)


class CustomGraphPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        button_draw = Button(self, text="Draw", font=BUTTON_FONT, width=10, cursor=CURSOR, command=self.create_graph)
        button_draw.pack(padx=15, pady=15)

        button_back = Button(self, text="Back", font=BUTTON_FONT, width=10, cursor=CURSOR, command=lambda: controller.show_frame(MainMenuPage))
        button_back.pack(padx=15, pady=15)

    def create_graph(self):
        plt.ion()
        fig, ax = plt.subplots(1, 1)
        ax.set(xlim=[-2, 2], ylim=[-2, 2])

        total_nodes = randint(4, 5)
        graph = np.array(
            [[0 if random() < 0.3 or j <= i else 1 for i in range(total_nodes)] for j in range(total_nodes)])
        print(graph)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        plot_instance = netgraph.InteractivelyConstructDestroyGraph(graph)

        print(plot_instance.edge_list)
        print(plot_instance.node_edge_artists)

        mainloop()


class GamePage(Frame):

    def __init__(self, parent, controller):
        super(GamePage, self).__init__(parent)

        self.plot_instance = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.button_start = Button(self, text="Start", bg="green", font=BUTTON_FONT, width=10, cursor=CURSOR, command=self.play)
        self.button_start.grid(column=0, row=0, columnspan=2)

        self.button_back = Button(self, text="Back", font=BUTTON_FONT, bg="white", width=10, cursor=CURSOR, command=lambda: controller.show_frame(SelectDiffPage))
        self.button_back.grid(column=0, row=1, columnspan=2, pady=50)
        self.button_undo = Button(self, text="Undo (z)", font=BUTTON_FONT, bg="white", cursor=CURSOR)
        self.button_help = Button(self, text="Help (h)", font=BUTTON_FONT, bg="green", cursor=CURSOR)

        self.time_label = Label(self, text="", font=('Arial', 16))
        self.points_label = Label(self, text="", font=('Arial', 16))

        self.time = 0

        self.difficulty = None

        self.fig, ax = plt.subplots(1, 1)
        ax.set(xlim=[-2, 2], ylim=[-2, 2])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.controller = controller

    def play(self):

        self.button_start.grid_forget()
        self.button_back.grid_forget()
        self.time_label.grid(row=0, column=0)
        self.points_label.grid(row=0, column=1)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=3, columnspan=2, sticky="nsew")
        self.time = 90 if self.difficulty == "hard" else 60
        self.update_clock()

        if self.difficulty == "easy":
            total_nodes = randint(4, 5)
        elif self.difficulty == "medium":
            total_nodes = randint(6, 7)
        else:
            total_nodes = randint(8, 9)

        graph = create_graph(total_nodes, self.difficulty)
        self.plot_instance = netgraph.PlayableGraph(graph)

        self.fig.canvas.mpl_connect('button_press_event', self._on_press)

        self.button_undo.grid(column=0, row=2, sticky="nsew")
        self.button_undo.config(command=self.plot_instance.undo)

        self.button_help.grid(column=1, row=1, sticky="nsew")
        self.button_help.config(command=self.click_help)

        self.reset_button = Button(self, text="Reset (r)", font=BUTTON_FONT, bg="black", fg="white", cursor=CURSOR, width=10, command=self.plot_instance.deselect_all_artists)
        self.reset_button.grid(column=0, row=1, sticky="nsew")

        self.unsolvable_button = Button(self, text="Unsolvable (t)", font=BUTTON_FONT, cursor=CURSOR, width=10,
                                    bg="blue", command=self.pressUnsolvable)
        self.unsolvable_button.grid(column=1, row=2, sticky="nsew")

        self.points_label.config(text="Current points: 0")

        self.controller.bind('r', lambda event: self.plot_instance.deselect_all_artists())
        self.controller.bind('t', lambda event: self.pressUnsolvable())
        self.controller.bind('z', lambda event: self.plot_instance.undo())
        self.controller.bind('h', lambda event: self.click_help())

    def nextGraph(self):
        self.plot_instance.deleteGraph()
        if self.difficulty == "easy":
            total_nodes = randint(4, 5)
        elif self.difficulty == "medium":
            total_nodes = randint(6, 7)
        else:
            total_nodes = randint(8, 9)
        graph = create_graph(total_nodes, self.difficulty)
        self.plot_instance = netgraph.PlayableGraph(graph)

        self.fig.canvas.mpl_connect('button_press_event', self._on_press)
        self.reset_button.config(command=self.plot_instance.deselect_all_artists)
        self.unsolvable_button.config(command=self.pressUnsolvable)
        self.button_undo.config(command=self.plot_instance.undo)
        self.button_help.config(command=self.click_help)

        # self.button_next.config(text="Done", command=lambda: self.controller.show_frame(SaveToHighscoresPage))
        # self.button_next.pack(padx=15, pady=10)

    def _on_press(self, event):
        if self.plot_instance.isSolved():
            self.controller.points += self.plot_instance.no_vertices
            self.points_label.config(text="Current points: {0}".format(self.controller.points))
            if self.difficulty == "medium":
                self.time += 3
            elif self.difficulty == "hard":
                self.time += 5
            self.nextGraph()

    def pressUnsolvable(self):
        if not self.plot_instance.hamiltonian_paths:
            self.controller.points += 2
            self.points_label.config(text="Current points: {0}".format(self.controller.points))
            self.nextGraph()
        else:
            messagebox.showwarning("Fail!", "Given maze is solvable! Time penalty -2!")
            self.time -= 2

    def update_clock(self):
        self.time -= 1
        if self.time > 0:
            self.time_label.config(text=self.time)
            self.after(1000, self.update_clock)
        else:
            self.clear_window()
            if self.difficulty == "medium":
                self.controller.points *= 2
            elif self.difficulty == "hard":
                self.controller.points *= 3
            self.controller.frames[SaveToHighscoresPage].update_points()
            self.controller.show_frame(SaveToHighscoresPage)

    def clear_window(self):
        self.time_label.config(text="")
        self.points_label.config(text="")
        self.controller.unbind('z')
        self.controller.unbind('r')
        self.controller.unbind('t')
        self.controller.unbind('h')
        self.plot_instance.deleteGraph()
        self.unsolvable_button.grid_forget()
        self.reset_button.grid_forget()
        self.button_undo.grid_forget()
        self.button_help.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
        self.button_start.grid(column=0, row=0, columnspan=2)
        self.button_back.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    def click_help(self):
        self.controller.points = 0
        self.points_label.config(text="Current points: 0")
        hamiltons = self.plot_instance.hamiltonian_paths
        visited = self.plot_instance.visited
        for path in hamiltons:
            if visited == path[:len(visited)]:
                messagebox.showinfo("Information", "You're on the right track!")
                return
        messagebox.showwarning("Warning", "Current path can't be right! Try undoing/resetting.")


class SaveToHighscoresPage(Frame):

    def __init__(self, parent, controller):
        super(SaveToHighscoresPage, self).__init__(parent)

        self.controller = controller
        self.points = self.controller.points

        self.feedback_label = Label(self, text="Time's up! Your score is: " + str(controller.points), font=('Arial', 32))
        self.feedback_label.pack(padx=15, pady=30)

        self.entry = Entry(self, width=30)
        self.entry.pack(padx=15, pady=30)

        self.save_button = Button(self, text="Save to highscores", width=15, bg='green', cursor=CURSOR, font=BUTTON_FONT, command=self.insert_to_highscores)
        self.save_button.pack(padx=15, pady=15)

        self.cancel_button = Button(self, text="Cancel", width=15, bg='white', cursor=CURSOR, font=BUTTON_FONT, command=self.cancel)
        self.cancel_button.pack(padx=15, pady=15)

    def update_points(self):
        self.points = self.controller.points
        self.feedback_label.config(text="Time's up! Your score is: " + str(self.controller.points))

    def insert_to_highscores(self):
        name = self.entry.get()
        if name:
            insert = "INSERT INTO Highscores (Ime, Points) VALUES ('{0}',{1})".format(name, self.points)
            self.controller.cursor.execute(insert)
            self.controller.connector.commit()
            self.controller.frames[HighscoresPage].update_scores()
            self.controller.points = 0
            self.controller.show_frame(MainMenuPage)
        else:
            messagebox.showwarning("Warning!", "Please input a name!")

    def cancel(self):
        self.controller.points = 0
        self.controller.show_frame(MainMenuPage)


def create_graph(total_nodes, diff):
    if diff == "easy":
        graph = np.array([[0 if random() < 0.4 or j <= i else 1 for i in range(total_nodes)] for j in range(total_nodes)])
    else:
        graph = np.array([[0 if random() < 0.7 or j <= i else 1 for i in range(total_nodes)] for j in range(total_nodes)])
    index = 0
    for row in graph:
        if np.all(np.zeros(total_nodes) == row):
            allowed_values = list(range(0, total_nodes))
            allowed_values.remove(index)
            ran = choice(allowed_values)
            row[ran:ran + 1] = 1
        index += 1
    for i in range(total_nodes):
        for j in range(total_nodes):
            if graph[i][j] == 1 and graph[j][i] == 1:
                graph[i][j] = 0
    return graph

  
if __name__=='__main__':
    app = MainApp()
    app.mainloop()
