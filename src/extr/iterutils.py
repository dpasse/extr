def flatten(items) -> list:
    flat_list = []
    for sublist in items:
        for item in sublist:
            flat_list.append(item)

    return flat_list
