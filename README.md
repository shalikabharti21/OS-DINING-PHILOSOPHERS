# Dining Philosophers Problem — OS Assignment 3

**Name:** Shalika Bharti
**Roll No:** 204BCSE026
**Topic (S.No. 3, Roll 21–30):** Dining Philosophers Problem
**Language:** Python 3 (no extra libraries needed)

---

## 1. Problem Formulation

- `N` philosophers sit around a round table, with **one fork between every two** of them (so `N` forks in total).
- Each philosopher repeatedly **THINKS → gets HUNGRY → picks up 2 forks → EATS → puts the forks down**.
- A philosopher needs **both** the left and the right fork to eat.

**The problem:** if all philosophers pick up their left fork at the same moment, each one waits forever for the right fork, which is held by a neighbour. This is a **deadlock** (circular wait).

## 2. Algorithm / Solution Logic

Synchronization is done with **semaphores**:

| Semaphore | Initial value | Purpose |
|-----------|---------------|---------|
| `forks[i]` (one per fork) | 1 | Binary semaphore: 1 = fork free, 0 = fork in use |
| `room` (the "waiter") | N − 1 | Lets at most N − 1 philosophers try to pick up forks at the same time |

**Why there is no deadlock:** with only N − 1 philosophers competing for N forks, at least one of them always gets both forks. That philosopher eats, puts the forks down, and the others can continue. This breaks the **circular wait** condition.

**Steps for each philosopher (thread):**
```
repeat for each meal:
    think()
    wait(room)          # enter room (max N-1 inside)
    wait(fork[left])    # pick left fork
    wait(fork[right])   # pick right fork
    eat()
    signal(fork[right]) # put right fork down
    signal(fork[left])  # put left fork down
    signal(room)        # leave room
```
In Python: `wait()` = `semaphore.acquire()` and `signal()` = `semaphore.release()`.
Left fork of philosopher `i` = `i`, right fork = `(i + 1) % N`.

## 3. How to Run

```bash
# Interactive: the program asks for input
python3 dining_philosophers.py

# With command-line arguments
python3 dining_philosophers.py -n 5 -m 3
```
| Option | Meaning |
|--------|---------|
| `-n`, `--philosophers` | Number of philosophers (at least 2) |
| `-m`, `--meals` | Number of meals each philosopher eats (at least 1) |

Invalid input (letters, 0, negative numbers) is rejected and asked again.

## 4. Output / Metrics Printed

- A time-stamped trace of every step: THINKING, HUNGRY, picked LEFT/RIGHT fork, EATING, put down forks.
- A **table line** showing the state of all philosophers each time someone starts eating.
- A **summary table**: meals eaten, total wait time and average wait time (time spent HUNGRY) per philosopher, plus total run time.

## 5. Sample Test Inputs

| Test | Command | Expected result |
|------|---------|-----------------|
| Standard case | `python3 dining_philosophers.py -n 5 -m 2` | 10 meals eaten, no deadlock |
| Small table | `python3 dining_philosophers.py -n 3 -m 1` | 3 meals eaten |
| Edge case (2 philosophers, 2 forks) | `python3 dining_philosophers.py -n 2 -m 3` | 6 meals eaten, they take turns |
| Large table | `python3 dining_philosophers.py -n 10 -m 3` | 30 meals eaten |

## 6. Sample Output

Full output for `-n 5 -m 2` is in [`sample_output.txt`](sample_output.txt). Summary part:

```
============================================================
 SUMMARY
============================================================
 Philosopher Meals Eaten   Total Wait (s)  Avg Wait (s)
 P0          2             0.33            0.17
 P1          2             0.05            0.03
 P2          2             0.36            0.18
 P3          2             0.01            0.00
 P4          2             0.77            0.39
------------------------------------------------------------
 Total meals eaten : 10 (expected 10)
 Average wait time : 0.15 s per meal
 Total run time    : 2.33 s
 Result            : All philosophers finished all meals. NO DEADLOCK.
============================================================
```
(Times change on every run because thinking and eating times are random.)

## 7. Key Concepts (for viva)

- **Semaphore:** an integer variable used for synchronization, changed only by `wait()` (decrement, block if 0) and `signal()` (increment, wake a waiting thread).
- **Deadlock conditions (Coffman):** mutual exclusion, hold and wait, no preemption, circular wait. This solution removes **circular wait**.
- **Starvation:** a philosopher waiting for a very long time while others keep eating.
- **Other solutions:** asymmetric pick-up (odd philosophers pick left first, even pick right first), or picking up both forks only if both are free (monitor solution).