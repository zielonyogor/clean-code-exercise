from pathlib import Path
# from abc import ABC, abstractmethod


# class Everything(ABC):
#     @abstractmethod
#     def send(self, x):
#         pass

#     @abstractmethod
#     def save(self, x):
#         pass

#     @abstractmethod
#     def refund(self, x):
#         pass


class Thing:
    def send(self, x):
        print("EMAIL " + x)

    def save(self, x):
        with Path("orders.txt").open("a", encoding="utf-8") as f:
            f.write(x + "\n")

    def refund(self, x):
        raise NotImplementedError("Not supported")


counter = 0
total = 0


def doIt(s, action, verbose, send, save):
    global counter, total
    try:
        if action == 2:
            x = f"REPORT|{counter}|{total:.2f}"
            if verbose:
                print(x)
            return x
        if action != 1:
            return "UNKNOWN"
        a = s.split("|")
        n, e, t = a[0], a[1], a[2]
        b = a[3].split(",")
        z = 0
        detail = ""
        for q in b:
            c = q.split(":")
            if c[0] == "BOOK":
                p = 40
            elif c[0] == "PEN":
                p = 5
            elif c[0] == "BAG":
                p = 80
            else:
                p = 0
            z += p * int(c[1])
            detail += c[0] + "x" + c[1] + ";"
        if t == "VIP":
            z *= 0.9
        elif t == "STUDENT":
            z *= 0.95
        if a[4] == "SAVE10":
            z *= 0.9
        if z < 100:
            z += 12
        z *= 1.23
        x = f"ORDER|{n}|{detail}|{z:.2f}"
        counter += 1
        total += z
        obj = Thing()
        if save:
            obj.save(x)
        if send:
            obj.send(e + "|" + x)
        if verbose:
            print(x)
        return x
    except Exception:
        return "ERROR"


if __name__ == "__main__":
    doIt("Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10", 1, True, True, True)
    doIt("Bob|bob@example.test|REGULAR|BAG:2|NONE", 1, True, True, True)
    doIt("", 2, True, False, False)
