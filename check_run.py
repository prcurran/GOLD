import os


if __name__ == "__main__":
    targets = ['akt1', 'ampc', 'cp3a4', 'cxcr4', 'gcr', 'hivpr', 'hivrt', 'kif11']

    for t in targets:
        for r in ["vanilla", "vanilla_scale_10", "hotspot_50_scale_10"]:
            path = f"/local/pcurran/diverse/{t}/gold_results/{r}/bestranking.lst"
            if os.path.exists(path):
                print(t, r)
