import matplotlib.pyplot as plt
import numpy as np
import csv

K = []
ALG1 = []
ALG2 = []
ALG3 = []


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
                first = False
                continue

            K.append(float(riga[0]))
            ALG1.append(int(riga[1]))
            ALG2.append(int(riga[2]))
            ALG3.append(int(riga[3]))


def plotInfluensed(filename, title):
    readfile(filename)

    plt.plot(K, ALG1, label='Algoritmo 1', color='blue', marker='o')
    plt.plot(K, ALG2, label='Algoritmo 2', color='green', marker='o')
    plt.plot(K, ALG3, label='Algoritmo 3', color='red', marker='o')

    plt.title(title)
    plt.xlabel("K")
    plt.ylabel("#Influensed")
    plt.legend()

    plt.savefig(f"Results/Plots/{title}.pdf", transparent=True, dpi='figure')
    plt.show()


def plotSeedSet(filename, title):
    readfile(filename)

    x = np.arange(len(K))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    offset = width * multiplier
    rects = ax.bar(x + offset, ALG1, width, label="Algoritmo 1")
    ax.bar_label(rects, padding=3)
    multiplier += 1
    offset = width * multiplier
    rects = ax.bar(x + offset, ALG2, width, label="Algoritmo 2")
    ax.bar_label(rects, padding=3)
    multiplier += 1
    offset = width * multiplier
    rects = ax.bar(x + offset, ALG3, width, label="Algoritmo 3")
    ax.bar_label(rects, padding=3)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Size Seed Set')
    ax.set_title(title)
    ax.set_xticks(x + width, K)
    ax.set_xlabel('K')
    ax.legend()

    plt.show()
    fig.savefig(f"Results/Plots/{title}.pdf", transparent=True, dpi='figure')


plotInfluensed("resultInfluensedCostRandom.csv", "Influenzati")
plotSeedSet("sizeSeedSetCostRandom.csv", "Size Seet Set")
