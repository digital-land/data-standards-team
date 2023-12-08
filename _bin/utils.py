def pythonic_keys(input_dict):
    new_dict = {}
    for key, value in input_dict.items():
        # Convert key to lowercase, replace spaces with underscores,
        # and remove brackets and their content
        new_key = (
            key.lower()
            .replace(" ", "-")
            .split(" (", 1)[0]
            .replace("(", "")
            .replace(")", "")
        )
        new_dict[new_key] = value
    return new_dict
