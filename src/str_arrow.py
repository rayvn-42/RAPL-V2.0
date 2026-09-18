def str_arrow(text, pos_start, pos_end):
    lines = text.split('\n')

    line = lines[pos_start.ln] if pos_start.ln < len(lines) else text

    return_str = f"\n\t{line}\n\t"

    start_col = pos_start.col
    end_col = pos_end.col

    if end_col <= start_col:
        end_col = start_col + 1

    for i in range(max(len(line), end_col)):
        if start_col <= i < end_col:
            return_str += '^'
        else:
            return_str += ' '


    return return_str