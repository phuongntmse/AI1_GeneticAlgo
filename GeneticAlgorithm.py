import math
import random
import time
from tkinter import *


# --------------1. DEFINED MAIN CLASSES-----------------
class X:
    def __init__(self):
        self.value = random.random()
        self.f = float(1 / calculate_f(self.value))


def init_xs(number_population):
    return [X() for i in range(number_population)]


def calculate_f(x):
    return float(a * x * x + b * x + c)  # min if x =1/2, f=1/(1+y)


def crossover(f_xs):
    offspring = []

    for i in range(nb_Crossover):

        parent1 = random.choice(f_xs)
        parent2 = random.choice(f_xs)

        x_binary = '{0:08b}'.format(int(parent1.value * (2 ** nBit)))
        y_binary = '{0:08b}'.format(int(parent2.value * (2 ** nBit)))
        child1 = X()
        child2 = X()

        split = random.randint(0, nBit - 1)
        new_x1 = x_binary[0:split] + y_binary[split:nBit]
        new_x2 = y_binary[0:split] + x_binary[split:nBit]

        child1.value = int(new_x1, 2) / (2 ** nBit)
        child1.f = 1 / calculate_f(child1.value)

        child2.value = float(int(new_x2, 2) / (2 ** nBit))
        child2.f = float(1 / calculate_f(child2.value))

        # check if being refused
        if (not is_refused_fx(child1)) & (not is_refused_fx(child2)):

            offspring.append(child1)
            offspring.append(child2)
        else:
            continue  # crossover(Xs)

    f_xs.extend(offspring)  # total number = nb_Crossover(new child) + old pop

    return f_xs


def is_refused_fx(child):
    if 0.0 < 1.0 / child.f < 1.0:
        return False
    else:
        return True


def mutation(f_xs):
    r = random.random()

    if r < mutation_Rate:

        pick = random.choice(f_xs)

        x_binary = list('{0:08b}'.format(int(pick.value * (2 ** nBit))))

        j = random.randint(0, nBit - 1)
        if x_binary[j] == '1':
            x_binary[j] = '0'
        else:
            x_binary[j] = '1'
        x_str = "".join(x_binary)
        child = X()
        child.value = int(x_str, 2) / (2 ** nBit)
        child.f = float(1 / calculate_f(child.value))
        # check if being refused
        if not is_refused_fx(child):
            pick.value = child.value
            pick.f = child.f
        else:
            pass

    return f_xs


def get_probability_list(l_xs):
    fitness_list = []
    for x in l_xs:
        fitness_list.append(x.f)

    total_fit = float(sum(fitness_list))
    relative_fitness = [(f / total_fit) for f in fitness_list]
    probabilities = [sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))]
    return probabilities


def roulette_wheel_pop(l_xs, probabilities, number_population):
    next_generation = []
    for n in range(number_population):
        r = random.random()
        for i in range(len(probabilities)):
            if r <= probabilities[i]:
                next_generation.append(l_xs[i])
                break
    return next_generation


def convergence(l_xs):
    return max(x.f for x in l_xs)


def is_converging(fx_list):
    n = len(fx_list)
    sum_coverging.append((fx_list[n - 1] - fx_list[n - 2]) ** 2)
    if math.sqrt(sum(sum_coverging)) / len(fx_list) <= 0.00001:
        return True
    else:
        return False


def calculate_x(f):
    c1 = c - f
    delta = (b ** 2) - (4 * a * c1)
    if delta < 0:
        return 0.0000001
    ans1 = (-b - math.sqrt(delta)) / (2 * a)
    ans2 = (-b + math.sqrt(delta)) / (2 * a)

    if 0 <= ans1 <= 1:
        ans = ans1
    elif 0 <= ans2 <= 1:
        ans = ans2
    else:
        return 0.0000001
    return ans


# -------------- 2. MAIN FUNCTION-----------------


def startprocess():
    configtostart()
    # Run algorithm
    global xs
    fx_list = []
    flag = True
    sum_coverging.append(0.0)
    while flag:

        xs = crossover(xs)  # pop = n+k
        xs = mutation(xs)  # pop = n+k
        probabilities = get_probability_list(xs)
        xs = roulette_wheel_pop(xs, probabilities, nb_pop)  # pop = n
        fx = convergence(xs)
        fx_list.append(fx)
        print("FX: " + str(1.0 / fx))
        if len(fx_list) > min_loops:
            if is_converging(fx_list):
                flag = not (rs_coverging(fx, len(fx_list)))
            elif len(fx_list) >= max_loop:
                flag = not (export_result(fx_list))
        else:
            # first_sum += fx
            n = len(fx_list)
            if n > 1:
                sum_coverging.append((fx_list[n - 1] - fx_list[n - 2]) ** 2)
    # Enable config side
    startbutton["state"] = "normal"
    entrya["state"] = "normal"
    entryb["state"] = "normal"
    entryc["state"] = "normal"
    epopulation["state"] = "normal"
    ecrossrate["state"] = "normal"
    emutation["state"] = "normal"
    emaxloop["state"] = "normal"


# -------------- 3. GUI-----------------

def export_result(fx_list):
    av_fx = sum(fx_list) / len(fx_list)
    min_val = X()
    min_val.value = calculate_x(1.0 / av_fx)
    min_val.f = av_fx
    is_refuse = is_refused_fx(min_val)
    global result
    t_end = time.time()
    result.insert(END, "Time: " + str(t_end - t_start) + "\n")
    result.insert(END, "Number of loops: " + str(len(fx_list)) + "\n")
    result.insert(END, "Min f(x): " + str(1.0 / min_val.f) + "\n")
    if is_refuse:
        result.insert(END, "Can not find value of x\n")
        result.insert(END, "-----------------------\n")
        root.update()
        rs = False
    else:
        result.insert(END, "x: " + '{:.10f}'.format(min_val.value) + "\n")
        rs = True
    result.insert(END, "-----------------------\n")
    root.update()
    return rs


def rs_coverging(fx, n_loops):
    min_val = X()
    min_val.value = calculate_x(1.0 / fx)
    min_val.f = fx
    is_refuse = is_refused_fx(min_val)
    global result
    t_end = time.time()
    result.insert(END, "Time: " + str(t_end - t_start) + "\n")
    result.insert(END, "Number of loops: " + str(n_loops) + "\n")
    result.insert(END, "Min f(x): " + str(1.0 / min_val.f) + "\n")
    if is_refuse:
        result.insert(END, "Can not find value of x\n")
        result.insert(END, "-----------------------\n")
        root.update()
        rs = False
    else:
        result.insert(END, "x: " + '{:.10f}'.format(min_val.value) + "\n")
        rs = True
    result.insert(END, "-----------------------\n")
    root.update()
    return rs


def configtostart():
    # Clear result information side
    global result
    result.delete('1.0', END)
    root.update()
    # get global value
    global a, b, c, nb_pop, rate_replacement, nb_Crossover, nBit, mutation_Rate, xs, max_loop
    global t_start
    t_start = time.time()
    a = float(entrya.get())
    b = float(entryb.get())
    c = float(entryc.get())
    nb_pop = int(epopulation.get())
    rate_replacement = float(ecrossrate.get())
    nb_Crossover = int(nb_pop * rate_replacement)
    mutation_Rate = float(emutation.get())
    max_loop = int(emaxloop.get())
    xs.clear()
    xs = init_xs(nb_pop)
    # Disable config side
    startbutton["state"] = "disabled"
    entrya["state"] = "disabled"
    entryb["state"] = "disabled"
    entryc["state"] = "disabled"
    epopulation["state"] = "disabled"
    ecrossrate["state"] = "disabled"
    emutation["state"] = "disabled"
    emaxloop["state"] = "disabled"


# declare global variable
a = 1.0
b = -1.0
c = 1.0
# multiple = 100
min_loops = 77  # vi chi thao thich :))
nb_pop = 100
rate_replacement = 0.75
nb_Crossover = int(rate_replacement * nb_pop)
nBit = 8
mutation_Rate = 0.01
xs = init_xs(nb_pop)
max_loop = 100000
t_start = time.time()
sum_coverging = []
# GUI
root = Tk()
root.geometry("700x450")
root.title("Genetic Algorithm")
frame = Frame(root, width=700, height=450)
frame.pack()
# Left side - Enter f(x), population, cross-over and mutation rate
leftframe = Frame(frame, width=300)
leftframe.pack(side=LEFT)
label = Label(leftframe, text="Enter f(x)")
label.pack()
fx_frame = Frame(leftframe)
fx_frame.pack()
entrya = Entry(fx_frame, width=6)
entrya.insert(0, '1')
entrya.grid(row=0)
lentrya = Label(fx_frame, text="x\u00b2 + ").grid(row=0, column=1)
entryb = Entry(fx_frame, width=6)
entryb.insert(0, '-1')
entryb.grid(row=0, column=2)
lentryb = Label(fx_frame, text="x + ").grid(row=0, column=3)
entryc = Entry(fx_frame, width=6)
entryc.insert(0, '1')
entryc.grid(row=0, column=4)
space = Label(leftframe, text="")
space.pack(padx=10, pady=10)
population_frame = Frame(leftframe)
population_frame.pack()
lpopulation = Label(population_frame, text="Size of population: ").grid(row=0)
epopulation = Entry(population_frame, width=10)
epopulation.insert(0, '100')
epopulation.grid(row=0, column=1)
space1 = Label(leftframe, text="")
space1.pack(padx=10, pady=10)
cross_frame = Frame(leftframe)
cross_frame.pack()
lcrossrate = Label(cross_frame, text="Crossover rate: ").grid(row=0)
ecrossrate = Entry(cross_frame, width=10)
ecrossrate.insert(0, '0.75')
ecrossrate.grid(row=0, column=1)
space2 = Label(leftframe, text="")
space2.pack(padx=10, pady=10)
mutation_frame = Frame(leftframe)
mutation_frame.pack()
lmutation = Label(mutation_frame, text="Mutation rate: ").grid(row=0)
emutation = Entry(mutation_frame, width=10)
emutation.insert(0, '0.01')
emutation.grid(row=0, column=1)
space3 = Label(leftframe, text="")
space3.pack(padx=10, pady=10)
maxloop_frame = Frame(leftframe)
maxloop_frame.pack()
lmaxloop = Label(maxloop_frame, text="Maximum number of loops: ").grid(row=0)
emaxloop = Entry(maxloop_frame, width=10)
emaxloop.insert(0, '100000')
emaxloop.grid(row=0, column=1)
space4 = Label(leftframe, text="")
space4.pack(padx=10, pady=10)
startbutton = Button(leftframe, text="Start", command=startprocess)
startbutton.pack()
# Right side - Result informations
rs_frame = Frame(frame, width=400)
rs_frame.grid_propagate(0)
rs_frame.pack(side=RIGHT)
rs_label = Label(rs_frame, text="Result")
rs_label.pack()
result = Text(rs_frame, width=30, wrap=NONE)
result.pack(padx=40)
scrollb = Scrollbar()
scrollb.place(in_=result, relx=1.0, relheight=1.0, bordermode="outside")
scrollb.configure(command=result.yview)
root.mainloop()
