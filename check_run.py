import os


if __name__ == "__main__":
    targets = ['akt1', 'ampc', 'cp3a4', 'cxcr4', 'gcr', 'hivpr', 'hivrt', 'kif11']

    for t in targets:
        path = f"/local/pcurran/diverse/{t}/gold_results/vanilla/bestranking.lst"
        if os.path.exists(path):
            print(t)
