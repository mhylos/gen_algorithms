import customtkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
from gen_algorithm import genetic_algorithm, generate_population
import statistics

WIDTH = 800
HEIGHT = 700

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry(f"{WIDTH}x{HEIGHT}")
app.grid_rowconfigure(0, weight=3)
app.grid_rowconfigure(1, weight=10)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=5)
app.title("Algoritmos genéticos - Mochila")
title_font = customtkinter.CTkFont(size=20, weight="bold")
section_font = customtkinter.CTkFont(size=17, weight="bold")

# Defaults
best_percentage = 30
random_percentage = 20


def change_best_percentage(label: customtkinter.CTkLabel, slider: customtkinter.CTkSlider):
    global best_percentage
    value = slider.get()
    if random_percentage + value > 100:
        slider.set(best_percentage)
        return
    best_percentage = value
    label.configure(text=f"{int(best_percentage)} %")


def change_random_percentage(label: customtkinter.CTkLabel, slider: customtkinter.CTkSlider):
    global random_percentage
    value = slider.get()
    if best_percentage + value > 100:
        slider.set(random_percentage)
        return
    random_percentage = value
    label.configure(text=f"{int(random_percentage)} %")


def change_mutation_rate(label: customtkinter.CTkLabel, slider: customtkinter.CTkSlider):
    label.configure(text=f"{int(slider.get())} %")


options_frame = customtkinter.CTkFrame(app)
stats_frame = customtkinter.CTkFrame(app)
results_frame = customtkinter.CTkFrame(app, width=400, height=400)

options_title = customtkinter.CTkLabel(
    options_frame, text="Opciones", fg_color="transparent", font=title_font)
options_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Tamaño de la población
population_label = customtkinter.CTkLabel(
    options_frame, text="Tamaño de la población: ", fg_color="transparent")
population_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
population_input = customtkinter.CTkEntry(
    options_frame, width=50)
population_input.insert(0, 50)
population_input.grid(row=1, column=1, padx=10, sticky="w")

# Número de generaciones
generations_label = customtkinter.CTkLabel(
    options_frame, text="Número de generaciones: ", fg_color="transparent")
generations_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
generations_input = customtkinter.CTkEntry(
    options_frame, width=50)
generations_input.insert(0, 100)
generations_input.grid(row=2, column=1, padx=10, sticky="w")

# Seleccion

# Mejores
best_selection_label = customtkinter.CTkLabel(
    options_frame, text="Selección de mejores", fg_color="transparent")
best_selection_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
selection_best_value_label = customtkinter.CTkLabel(
    options_frame, text=f"{int(best_percentage)} %", fg_color="transparent", width=40)
selection_best_value_label.grid(row=4, column=1, padx=10, sticky="w")
selection_best_slider = customtkinter.CTkSlider(
    options_frame, from_=0, to=100)
selection_best_slider.set(best_percentage)
selection_best_slider.grid(row=4, column=0, padx=10, sticky="w")

# Aleatoria
random_selection_label = customtkinter.CTkLabel(
    options_frame, text="Selección aleatoria", fg_color="transparent")
random_selection_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
selection_random_value_label = customtkinter.CTkLabel(
    options_frame, text=f"{int(random_percentage)} %", fg_color="transparent", width=40)
selection_random_value_label.grid(
    row=6, column=1, padx=10, sticky="w")
selection_random_slider = customtkinter.CTkSlider(
    options_frame, from_=0, to=100)
selection_random_slider.set(random_percentage)
selection_random_slider.grid(row=6, column=0, padx=10, sticky="w")

selection_best_slider.bind("<ButtonRelease-1>", lambda e: change_best_percentage(
    selection_best_value_label, selection_best_slider))
selection_random_slider.bind("<ButtonRelease-1>", lambda e: change_random_percentage(
    selection_random_value_label, selection_random_slider))

# Mutación
mutation_label = customtkinter.CTkLabel(
    options_frame, text="Probabilidad de mutación", fg_color="transparent")
mutation_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
mutation_value_label = customtkinter.CTkLabel(
    options_frame, text=f"{10} %", fg_color="transparent", width=40)
mutation_value_label.grid(row=8, column=1, padx=10, sticky="w")
mutation_slider = customtkinter.CTkSlider(
    options_frame, from_=0, to=100)
mutation_slider.set(10)
mutation_slider.grid(row=8, column=0, padx=10, sticky="w")

mutation_slider.bind("<ButtonRelease-1>", lambda e: change_mutation_rate(
    mutation_value_label, mutation_slider)
)


# Estadisticas
stats_title = customtkinter.CTkLabel(
    stats_frame, text="Estadísticas", fg_color="transparent", font=title_font)
stats_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Generación actual
current_generation_label = customtkinter.CTkLabel(
    stats_frame, text="Generación actual: ", fg_color="transparent")
current_generation_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
current_generation_value_label = customtkinter.CTkLabel(
    stats_frame, text="0", fg_color="transparent")
current_generation_value_label.grid(row=1, column=1, padx=10, sticky="w")

# Coeficiente de variación
coefvar_label = customtkinter.CTkLabel(
    stats_frame, text="Coeficiente de variación: ", fg_color="transparent")
coefvar_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
coefvar_value_label = customtkinter.CTkLabel(
    stats_frame, text="0", fg_color="transparent")
coefvar_value_label.grid(row=2, column=1, padx=10, sticky="w")


# Media
mean_label = customtkinter.CTkLabel(
    stats_frame, text="Media: ", fg_color="transparent")
mean_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
mean_value_label = customtkinter.CTkLabel(
    stats_frame, text="0", fg_color="transparent")
mean_value_label.grid(row=3, column=1, padx=10, sticky="w")

# Mejor
best_label = customtkinter.CTkLabel(
    stats_frame, text="Mejor: ", fg_color="transparent")
best_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
best_value_label = customtkinter.CTkLabel(
    stats_frame, text="0", fg_color="transparent")
best_value_label.grid(row=4, column=1, padx=10, sticky="w")


# Boton Generar
ms_per_generation = 300
stop = False


def create_generations():
    for widget in results_frame.winfo_children():
        widget.destroy()
    global population_size, generations, best_percentage, random_percentage, mutation_rate, ms_per_generation, stop
    stop = False
    population_size = int(population_input.get())
    generations = int(generations_input.get())
    best_percentage = selection_best_slider.get()
    random_percentage = selection_random_slider.get()
    mutation_rate = mutation_slider.get()

    population = generate_population(population_size)

    x_values = []
    y_values = []
    graph = Figure(figsize=(4, 4), dpi=100)
    graph.suptitle("Valor de la mejor mochila por generación", fontsize=12)
    plot = graph.add_subplot(111)
    plot.set_xlabel("Generación")
    plot.set_ylabel("Valor de la mochila")
    canvas = FigureCanvasTkAgg(graph, master=results_frame)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=10)

    def update_graph(i):
        nonlocal population
        population = genetic_algorithm(
            population, best_percentage / 100, random_percentage / 100, mutation_rate)

        best_bp = max(population, key=lambda x: x.get_value())
        mean = int(statistics.mean([bp.get_value() for bp in population]))
        std = int(statistics.stdev([bp.get_value() for bp in population]))
        coefvar = f'{std / mean * 100:.2f} %'

        coefvar_value_label.configure(text=coefvar)
        mean_value_label.configure(text=str(mean))
        best_value_label.configure(text=str(best_bp.get_value()))

        print(
            f'Generacion {i}:\n\nMejor:\n{best_bp}')
        print(f'Poblacion: \n' + '\n'.join([str(bp)
              for bp in population]) + '\n\n\n')
        x_values.append(i)
        y_values.append(best_bp.get_value())
        current_generation_value_label.configure(text=str(i + 1))

        plot.clear()
        plot.plot(x_values, y_values)
        canvas.draw()

        if stop:
            print("Parado")
            return

        if i < generations - 1:
            results_frame.after(ms_per_generation, update_graph, i + 1)

    results_frame.after(ms_per_generation, update_graph, 0)


generate_button = customtkinter.CTkButton(
    options_frame, text="Generar", command=create_generations)
generate_button.grid(row=9, column=0, columnspan=2,
                     padx=10, pady=20, sticky="nsew", ipadx=10, ipady=10)

# Acelerar el proceso


def acceleration():
    global ms_per_generation
    ms_per_generation = ms_per_generation // 2


acceleration_button = customtkinter.CTkButton(
    options_frame, text="Acelerar la generación", command=acceleration, fg_color="yellow3", hover_color="yellow", text_color="black")

acceleration_button.grid(row=10, column=0, columnspan=2,
                         padx=10, pady=20, sticky="nsew", ipadx=10, ipady=10)

options_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
stats_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Parar


def stop_generation():
    global stop
    stop = True


stop_button = customtkinter.CTkButton(
    options_frame, text="Parar generación", command=stop_generation, fg_color="darkred", hover_color="red")
stop_button.grid(row=11, column=0, columnspan=2,
                 padx=10, pady=20, sticky="nsew", ipadx=10, ipady=10)


app.mainloop()
