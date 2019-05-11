from ukrainian_data_adt import UkrainianData


if __name__ == "__main__":
    # Run this code to see example of usage
    mig = UkrainianData("338a8ccf-8b77-476b-b138-9bb5b7550584")
    print(mig.get_value('м. Севастополь***', 'Число прибулих 2010'))
    print(mig.get_row("м. Севастополь***"))
    print(mig.get_column("Число прибулих 2010"))
    print(UkrainianData.correlation_index(list(mig.get_column("Число прибулих 2010").values()),
                                          list(mig.get_column("Число прибулих 2012").values())))
    print(mig.row_names)
    print(mig.column_names)

    """
    with open("example_map.html", "w") as f:
        f.write(mig.get_map("Число прибулих", 2010))
    """