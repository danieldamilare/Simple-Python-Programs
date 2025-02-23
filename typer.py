def lowest_common_substring(input_list):
    prefix = min(input_list, key=len)
    for i in range(len(prefix)):
        if not all(s[i] == prefix[i] for s in input_list):
            return prefix[:i]

    return prefix



