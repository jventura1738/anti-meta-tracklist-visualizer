import os
import random
import string
import subprocess
import sys
import time

LINE_LENGTH = 47  # for my terminal

def file_to_lines(filename: str) -> list:
    """Given a file name, return lines"""
    lines = list()
    with open(filename, "r") as file_in:
        lines = [[char for char in line.rstrip()]
                  for line in file_in]
    return lines

def visualize(lines: list, converge_mode: int = 0) -> None:
    """Visualizes the decoding on the lines.
    Args:
        lines (list(list(str)): the lines of the file as list
    Returns:
        Nothing, writes to terminal.

    Converge modes:
        random (0): randomly converges to decoded text
        # I'll do these in the future:
        top down (1): converges one line at a time
        bottom up (2): converges one line at a time reverse
        towards middle (3): converges top->middle<-bottom
    """
    def _get_random_chars(n: int = 1) -> str:
        char_pool = string.ascii_letters + string.digits + " .@-.,:\""
        return [char for char in random.choices(char_pool, k=n)]

    def _initial_state() -> list:
        return [_get_random_chars(len(line))
                for line in lines]

    def _get_threshold() -> list:
        threshold = list()
        for line in lines:
            threshold.append([random.randint(0,20) for _ in line])
        return threshold

    def _write_array(array) -> None:
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'

        for line in array:
            colored_line = []
            for char in line:
                if random.random() < 0.1:  # 10% chance of being red
                    colored_line.append(RED + BOLD + char + END)
                else:
                    colored_line.append(char)
            print(''.join(colored_line))

    random.seed(0)
    encoded = _initial_state()
    threshold = _get_threshold()

    run_simulation = True
    start_time = time.time()
    duration = 13 # 10s

    while run_simulation:
        os.system("clear")  # cls for windows
        for i, line in enumerate(encoded):
            for j, char in enumerate(line):
                if char != lines[i][j]:
                    encoded[i][j] = _get_random_chars()[0]
                else:
                    if threshold[i][j] > 0:
                        threshold[i][j] -= 1
                        encoded[i][j] = _get_random_chars()[0]

        _write_array(encoded)
        time.sleep(1/1000)
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            run_simulation = False

    os.system("clear")
    subprocess.call(['zsh', '-i', '-c', 'colorcat tracklist'])


if __name__ == "__main__":
    lines = file_to_lines("tracklist2")
    print(lines)
    visualize(lines)

