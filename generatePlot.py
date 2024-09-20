import matplotlib.pyplot as plt
import numpy as np
import csv

K = []
ALG1 = []
ALG2 = []
ALG3 = []
ALG4 = []


def readfile(filename):
    with open(f"Results/{filename}", mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        for riga in csv_reader:
            if first:
                K.clear()
                ALG1.clear()
                ALG2.clear()
                ALG3.clear()
                ALG4.clear()
                first = False
                continue

            K.append(float(riga[0]))
            ALG1.append(int(riga[1]))
            ALG2.append(int(riga[2]))
            ALG3.append(int(riga[3]))
            ALG4.append(int(riga[4]))
            
def readfiles(seedset_size_filename, influenced_filename):
    with open(f"Results/{seedset_size_filename}", mode='r') as seedset_file:
        with open(f"Results/{influenced_filename}", mode='r') as influenced_file:
            seedset_reader = csv.reader(seedset_file, delimiter=',')
            influenced_reader = csv.reader(influenced_file, delimiter=',')
            first = True
            for riga in zip(influenced_reader, seedset_reader):
                if first:
                    K.clear()
                    ALG1.clear()
                    ALG2.clear()
                    ALG3.clear()
                    ALG4.clear()
                    first = False
                    continue

                K.append(float(riga[0][0]))
                ALG1.append(round(float(riga[0][1])/float(riga[1][1]), 1))
                ALG2.append(round(float(riga[0][2])/float(riga[1][2]), 1))
                ALG3.append(round(float(riga[0][3])/float(riga[1][3]), 1))
                ALG4.append(round(float(riga[0][4])/float(riga[1][4]), 1))


def plotInfluenced(filename, title):
    readfile(filename)
    plt.clf()
    
    plt.plot(K, ALG1, label='Algoritmo 1', color='blue', marker='o')
    plt.plot(K, ALG2, label='Algoritmo 2', color='green', marker='o')
    plt.plot(K, ALG3, label='Algoritmo 3', color='red', marker='o')
    plt.plot(K, ALG4, label='Algoritmo 4', color='purple', marker='o')

    plt.title(title)
    plt.xlabel("K")
    plt.ylabel("#Influenced")
    plt.legend()

    # plt.show()
    plt.savefig(f"Results/Plots/{title}.pdf", transparent=True, dpi='figure')
    


def vertical_bars_plot(filename, title, single_file: bool = True):
    if single_file:
        readfile(filename)
    else:
        readfiles(filename, filename.replace("sizeSeedSet", "resultInfluenced"))

    x = list(range(len(K))) # the label locations
    x[1] += 0.2
    x[2] += 0.4
    
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    offset = width * multiplier
    rects = ax.bar(list(map(lambda tmp: tmp + offset, x)), ALG1, width, label="Algoritmo 1")
    ax.bar_label(rects, padding=3)
    
    multiplier += 1
    offset = width * multiplier
    rects = ax.bar(list(map(lambda tmp: tmp + offset, x)), ALG2, width, label="Algoritmo 2")
    ax.bar_label(rects, padding=3)
    
    multiplier += 1
    offset = width * multiplier
    rects = ax.bar(list(map(lambda tmp: tmp + offset, x)), ALG3, width, label="Algoritmo 3")
    ax.bar_label(rects, padding=3)
    
    multiplier += 1
    offset = width * multiplier
    rects = ax.bar(list(map(lambda tmp: tmp + offset, x)), ALG4, width, label="Algoritmo 4")
    ax.bar_label(rects, padding=3)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Size Seed Set')
    ax.set_title(title)
    ax.set_xticks(list(map(lambda tmp: tmp + width + 0.125, x)), K)
    ax.set_xlabel('K')
    ax.legend()

    # plt.show()
    fig.savefig(f"Results/Plots/{title}.pdf", transparent=True, dpi='figure')

# # Random
# vertical_bars_plot("resultInfluencedCostRandom.csv", "Influenced_Random")
# vertical_bars_plot("sizeSeedSetCostRandom.csv", "SeedSetSize_Random")

# # Degree
# vertical_bars_plot("resultInfluencedCostDegree.csv", "Influenced_Degree")
# vertical_bars_plot("sizeSeedSetCostDegree.csv", "SeedSetSize_Degree")

# # Constant
# vertical_bars_plot("resultInfluencedCostConst.csv", "Infleunced_Constant")
# vertical_bars_plot("sizeSeedSetCostConst.csv", "SeedSetSize_Constant")

# Ratios
vertical_bars_plot("sizeSeedSetCostConst.csv", "Constant_Ratio", False)
vertical_bars_plot("sizeSeedSetCostDegree.csv", "Degree_Ratio", False)
vertical_bars_plot("sizeSeedSetCostRandom.csv", "Random_Ratio", False)