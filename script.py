from pathlib import Path
import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("account", type=str)
    return parser.parse_args()


def main():
    args = get_args()

    path_in = Path.cwd() / "data" / "transactions.csv"
    df = pd.read_csv(path_in)

    for dest in [False, True]:
        df_copy = df.copy()

        account_col = "source_name" if not dest else "destination_name"
        map_cols = {
            "date": "date",
            "description": "notes",
            "category": "category",
            "amount": "amount",
        }
        map_cols[("destination_name" if not dest else "source_name")] = "payee"

        df_copy = df_copy[df_copy[account_col] == args.account]
        df_copy = df_copy[list(map_cols.keys())]
        df_copy = df_copy.rename(columns=map_cols)
        df_copy["date"] = df_copy["date"].apply(lambda s: str(s).split("T")[0])

        path_out = Path.cwd() / "results" / f"{args.account.replace(" ", "").lower()}-{"inflow" if dest else "outflow"}.csv"
        path_out.parent.mkdir(exist_ok=True)
        df_copy.to_csv(str(path_out), index=False)


if __name__ == "__main__":
    main()
