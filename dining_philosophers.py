"""
Operating Systems - Assignment 3
Topic   : Dining Philosophers Problem (using Semaphores)
Name    : Shalika Bharti
Roll No : 204BCSE026

PROBLEM
-------
N philosophers sit around a round table. Between every two philosophers
there is ONE fork (so there are N forks in total).
A philosopher keeps doing:  THINK -> get HUNGRY -> pick 2 forks -> EAT -> put forks down.
A philosopher needs BOTH the left and the right fork to eat.

The danger: if every philosopher picks up his LEFT fork at the same time,
everyone waits forever for the RIGHT fork  -->  DEADLOCK.

SOLUTION USED (simple and easy to explain)
------------------------------------------
1. Each fork is a binary semaphore (value 1 = free, 0 = in use).
2. A "room" (waiter) counting semaphore with value N-1.
   At most N-1 philosophers are allowed to try picking up forks at the
   same time. With only N-1 people competing for N forks, at least one
   of them always gets both forks, so deadlock can never happen.

HOW TO RUN
----------
    python dining_philosophers.py                 (asks for input)
    python dining_philosophers.py -n 5 -m 3       (5 philosophers, 3 meals each)
"""

import argparse
import random
import threading
import time

# ------------------------------------------------------------------
# Shared data (filled in main)
# ------------------------------------------------------------------
forks = []          # one semaphore per fork
room = None         # waiter semaphore, allows only N-1 philosophers in
print_lock = threading.Lock()   # so that lines printed by threads don't mix
start_time = 0.0

meals_eaten = []    # meals eaten by each philosopher
total_wait = []     # total time each philosopher spent HUNGRY (waiting for forks)
state = []          # current state of each philosopher (for printing)


def log(message):
    """Print a message with the time since start. Only one thread prints at a time."""
    with print_lock:
        elapsed = time.time() - start_time
        print(f"[{elapsed:6.2f}s] {message}")


def show_table():
    """Print the current state of all philosophers in one line."""
    with print_lock:
        print("          Table: " + " | ".join(f"P{i}:{s}" for i, s in enumerate(state)))


def philosopher(pid, n, meals):
    """Code run by each philosopher thread."""
    left = pid              # fork on the left
    right = (pid + 1) % n   # fork on the right

    for meal in range(1, meals + 1):
        # ---------------- THINKING ----------------
        state[pid] = "THINKING"
        log(f"Philosopher {pid} is THINKING")
        time.sleep(random.uniform(0.2, 0.6))

        # ---------------- HUNGRY ------------------
        state[pid] = "HUNGRY"
        log(f"Philosopher {pid} is HUNGRY (wants fork {left} and fork {right})")
        wait_start = time.time()

        room.acquire()                      # wait(room)  -> enter the dining room
        forks[left].acquire()               # wait(left fork)
        log(f"Philosopher {pid} picked up LEFT fork {left}")
        forks[right].acquire()              # wait(right fork)
        log(f"Philosopher {pid} picked up RIGHT fork {right}")

        waited = time.time() - wait_start
        total_wait[pid] += waited

        # ---------------- EATING ------------------
        state[pid] = "EATING"
        meals_eaten[pid] += 1
        log(f"Philosopher {pid} is EATING  (meal {meal}/{meals}, waited {waited:.2f}s)")
        show_table()
        time.sleep(random.uniform(0.2, 0.5))

        # ---------------- PUT FORKS DOWN ----------
        forks[right].release()              # signal(right fork)
        forks[left].release()               # signal(left fork)
        room.release()                      # signal(room) -> leave the room
        log(f"Philosopher {pid} put down forks {left} and {right}")

    state[pid] = "DONE"
    log(f"Philosopher {pid} has FINISHED all {meals} meals")


def read_input():
    """Read number of philosophers and meals from command line, or ask the user."""
    parser = argparse.ArgumentParser(description="Dining Philosophers using semaphores")
    parser.add_argument("-n", "--philosophers", type=int, help="number of philosophers (>= 2)")
    parser.add_argument("-m", "--meals", type=int, help="meals each philosopher eats (>= 1)")
    args = parser.parse_args()

    n = args.philosophers
    meals = args.meals

    # If not given on command line, ask in the terminal
    while n is None or n < 2:
        try:
            n = int(input("Enter number of philosophers (>= 2): "))
        except ValueError:
            n = None
        if n is None or n < 2:
            print("  Please enter a whole number of at least 2.")
            n = None

    while meals is None or meals < 1:
        try:
            meals = int(input("Enter number of meals per philosopher (>= 1): "))
        except ValueError:
            meals = None
        if meals is None or meals < 1:
            print("  Please enter a whole number of at least 1.")
            meals = None

    return n, meals


def main():
    global forks, room, start_time, meals_eaten, total_wait, state

    n, meals = read_input()

    # Create semaphores
    forks = [threading.Semaphore(1) for _ in range(n)]   # each fork free at start
    room = threading.Semaphore(n - 1)                    # only N-1 may sit to eat

    meals_eaten = [0] * n
    total_wait = [0.0] * n
    state = ["THINKING"] * n

    print("=" * 60)
    print(" DINING PHILOSOPHERS PROBLEM (Semaphores + Waiter)")
    print("=" * 60)
    print(f" Philosophers : {n}")
    print(f" Forks        : {n}")
    print(f" Meals each   : {meals}")
    print(f" Room limit   : {n - 1} philosophers at a time (prevents deadlock)")
    print("=" * 60)

    start_time = time.time()

    # Create and start one thread per philosopher
    threads = []
    for pid in range(n):
        t = threading.Thread(target=philosopher, args=(pid, n, meals))
        threads.append(t)
        t.start()

    # Wait for all philosophers to finish
    for t in threads:
        t.join()

    total_time = time.time() - start_time

    # ---------------- SUMMARY ----------------
    print()
    print("=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    print(f" {'Philosopher':<12}{'Meals Eaten':<14}{'Total Wait (s)':<16}{'Avg Wait (s)'}")
    for pid in range(n):
        avg = total_wait[pid] / meals_eaten[pid]
        print(f" P{pid:<11}{meals_eaten[pid]:<14}{total_wait[pid]:<16.2f}{avg:.2f}")
    print("-" * 60)
    print(f" Total meals eaten : {sum(meals_eaten)} (expected {n * meals})")
    print(f" Average wait time : {sum(total_wait) / (n * meals):.2f} s per meal")
    print(f" Total run time    : {total_time:.2f} s")
    print(" Result            : All philosophers finished all meals. NO DEADLOCK.")
    print("=" * 60)


if __name__ == "__main__":
    main()