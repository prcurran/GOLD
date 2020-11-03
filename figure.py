import os
import numpy as np
import pandas as pd

from ccdc.descriptors import StatisticalDescriptors as sd
import operator
import seaborn as sns
import matplotlib.pyplot as plt


def reformat_results(fname, cols=["Score", "Ligand name", "activity"]):
    with open(fname, "r") as reader:
        lines = [l.strip("\n") for l in reader.readlines()]

    # headers
    header = lines[5]
    # ['Score', 'S(PLP)', 'S(hbond)', 'S(cho)', 'S(metal)', 'DE(clash)',
    # 'DE(tors)', 'intcor', 'time', 'File name', 'Ligand name']
    header = [b.strip() for b in [a for a in header.split("  ") if a != '' and a != '#']]

    #  data
    data = lines[7:]
    cat_data = list(zip(*[[a for a in entry.split(" ") if a != ''] for entry in data]))
    df = pd.DataFrame({h: cat_data[i] for i, h in enumerate(header)})

    # all decoys are from ZINC
    df["activity"] = np.array(list(map(lambda x: 'ZINC' not in x, list(df['Ligand name'])))).astype(int)
    df['Score'] = df['Score'].astype(float)
    df = df.sort_values(by=['Score'], ascending=False)
    return df[cols]


def roc_data(df, score_col="score", activity_col="activity"):
    rs = sd.RankStatistics(scores=list(zip(list(df[score_col]), list(df[activity_col]))),
                           activity_column=operator.itemgetter(1))

    # ROC
    tpr, fpr = rs.ROC()
    df["tpr"] = tpr
    df["fpr"] = fpr
    return df


def roc_plot(df, ax, title="plot", hue="scheme", hue_order=["plp", "hotspot"], palette='Set2'):
    """

    """
    # random
    sns.lineplot(x=[0, 1], y=[0, 1], color="grey", ax=ax)

    # docking rank
    vals = set(df[hue])
    # style lines
    d = {val: {"color": sns.color_palette(palette)[i], "linestyle": "-"} for i, val in enumerate(hue_order)}
    print(d)
    # group data (hue)
    lines = [ax.plot(grp.fpr, grp.tpr, label=n, **d[n])[0] for n, grp in df.groupby(hue)]

    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_xticks([0, 0.5, 1])
    ax.set_title(label=f"{title}",
                 fontdict={'fontsize':10})

    return lines


def enrichment(df):
    rs = sd.RankStatistics(scores=list(zip(list(df['Score']), list(df['actives']))),
                           activity_column=operator.itemgetter(1))

    metric_df = pd.DataFrame({"AUC": [rs.AUC()],
                             "EF1": [rs.EF(fraction=0.01)],
                             "EF5": [rs.EF(fraction=0.05)],
                             "EF10": [rs.EF(fraction=0.1)],
                             "BEDROC16": [rs.BEDROC(alpha=16.1)],
                             "BEDROC8": [rs.BEDROC(alpha=8)]
                             })
    return metric_df


def _asthetics(fig, axs, lines):
    """
    Extra formatting tasks

    :param `matplotlib.figure.Figure` fig: mpl figure
    :param list axs: list of  `matplotlib.axes.Axes`
    :param `matplotlib.lines.Line2D` lines: ROC lines
    :return:
    """
    # format axes
    axs[0][0].set_yticks([0, 0.5, 1])
    yticks = [-1, 0, 1, 2]

    # format legend
    fig.legend(lines,
               [f"{w}" for w in ['plp', 'hotspot']],
               (.83, .42),
               title="Scoring Scheme")
    # format canvas
    plt.subplots_adjust(left=0.1, right=0.8, top=0.86)


if __name__ == "__main__":

    base = "/local/pcurran/diverse"
    targets = ['akt1', 'ampc', 'cp3a4', 'cxcr4', 'gcr', 'hivpr', 'hivrt', 'kif11']
    # Plot the ROC and box plots
    sns.set_style('white')
    rows = 4
    cols = 2
    fig, axs = plt.subplots(nrows=rows, ncols=cols, figsize = (10, 20))

    for i in range(rows):
        for j in range(cols):
            n = (cols * i) + j
            t = targets[n]
            vanilla = f"/local/pcurran/diverse/{t}/gold_results/vanilla/bestranking.lst"
            rescored = f"/local/pcurran/diverse/{t}/gold_results/vanilla/rescored.csv"

            if os.path.exists(vanilla) and os.path.exists(rescored):
                df1 = reformat_results(vanilla)
                df1 = df1.rename(columns={"Score": "score", "Ligand name": "identifier"})
                df1 = roc_data(df1)
                df1["score_func"] = ["plp"] * len(df1)
                print(set(df1.activity))


                df2 = pd.read_csv(rescored, index_col=0)
                df2['score'] = df2['score'].astype(float)
                df2 = df2.sort_values(by=['score'], ascending=False)
                df2 = roc_data(df2)
                df2["score_func"] = ["hotspot"] * len(df2)

                df = pd.concat([df1, df2])

                print(df)

                lines = roc_plot(df=df, ax=axs[i][j], hue="score_func", title=t)

    _asthetics(fig, axs, lines)
    plt.show()

