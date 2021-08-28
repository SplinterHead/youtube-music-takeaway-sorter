def progress_bar(current, total, bar_length=20):
    percent = float(current) * 100 / total
    arrow = "-" * int(percent / 100 * bar_length - 1) + ">"
    spaces = " " * (bar_length - len(arrow))

    print("Progress: [%s%s] %d / %d" % (arrow, spaces, current, total), end="\r")
