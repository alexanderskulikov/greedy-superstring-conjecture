# TODO: replace with an efficient implementation later if needed
def overlap(first_string, second_string):
    for i in range(min(len(first_string), len(second_string)), 0, -1):
        if first_string[-i:] == second_string[0:i]:
            return i

    return 0


def prefix(first_string, second_string):
    return len(first_string) - overlap(first_string, second_string)


def suffix(first_string, second_string):
    return len(second_string) - overlap(first_string, second_string)
