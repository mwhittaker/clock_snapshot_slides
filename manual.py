from collections import defaultdict
import itertools
import math
import matplotlib.pyplot as plt
import sys

def setlist(xs, key=lambda x: x):
    return list(sorted(set(xs), key=key))

def flatten(ls):
    return [x for l in ls for x in l]

def process(x):
    return x[0]

def timestamp(x):
    return x[1]

def plot(events, plotname, labels=None):
    labels = [] if labels is None else labels

    plt.figure()
    if len(events) == 0:
        plt.axis("off")
        plt.savefig(plotname, bbox_inches="tight")
        return

    # Gather the events into a sorted sequence of events keyed by process. For
    # example, the set of events
    #
    #     [(("a", 2),), (("a", 1), ("b", 5))]
    #
    # would be gathered into the following dictionary
    #
    #     {
    #         "a": [("a", 1), ("a", 2)],
    #         "b": [("b", 5)],
    #     }
    history = defaultdict(list)
    for event in events:
        for x in event:
            history[process(x)].append(x)

    for p in history:
        history[p] = setlist(history[p], key=timestamp)

    threads = list(sorted(history.keys()))
    num_threads = len(threads)
    max_timestamp = max(max(timestamp(x) for x in event) for event in history.values())

    # horizontal lines
    for i in range(max_timestamp):
        plt.plot([0, num_threads - 1], [i + 0.5, i + 0.5], "k--")

    # vertical lines
    for i in range(num_threads):
        plt.plot([i, i], [-0.5, max_timestamp + 0.5], "k")

    # thread labels
    for (i, p) in enumerate(threads):
        plt.text(
            i,
            max_timestamp + 3,
            "process ${}$".format(p),
            rotation="vertical",
            horizontalalignment="center"
        )

    # events and labels
    for (i, p) in enumerate(threads):
        for (j, x) in enumerate(history[p]):
            if i < (float(num_threads) / 2):
                plt.text(i - 0.1, timestamp(x), "${}_{}$".format(p, j), ha="center")
            else:
                plt.text(i + 0.1, timestamp(x), "${}_{}$".format(p, j), ha="center")
            plt.scatter([i], [timestamp(x)], c="k")

    # additional labels
    for (p, t, l) in labels:
        i = threads.index(p)
        if i < (float(num_threads) / 2):
            plt.text(i - 0.15, t, l, ha="right")
        else:
            plt.text(i + 0.15, t, l, ha="left")

    # edges
    for event in events:
        assert 1 <= len(event) <= 2
        if len(event) == 2:
            (p0, y0) = event[0]
            (p1, y1) = event[1]
            x0 = threads.index(p0)
            x1 = threads.index(p1)
            plt.plot([x0, x1], [y0, y1])

    plt.axis("off")
    plt.savefig(plotname, bbox_inches="tight")

def main():
    events = [
        (("b", 1), ("c", 2)),
        (("c", 3), ("a", 4)),
        (("b", 0), ("a", 5)),
    ]
    plot(events, "naive.pdf")

    events = {}
    events[1] = [
        (("a", 0), ("b", 1)),
        (("a", 0), ("c", 1)),
    ]
    events[2] = [
        (("b", 2), ("a", 6)),
        (("b", 2), ("c", 3)),
        (("c", 3), ("b", 4)),
        (("c", 4), ("a", 5)),
        (("c", 4), ("b", 5)),
    ]
    events[3] = [
        (("a", 5), ("c", 6)),
        (("b", 5), ("c", 6)),
        (("a", 6), ("b", 7)),
    ]
    events[4] = [
        (("b", 8),),
        (("b", 9), ("a", 10)),
        (("b", 9), ("c", 10)),
        (("c", 11),),
        (("c", 12), ("a", 13)),
        (("c", 12), ("b", 13)),
    ]

    labels = {}
    labels[1] = [
        ("a", 0, "$[]$"),
        ("b", 0, "$[0:a]$"),
        ("c", 0, "$[0:a]$"),
        ("b", 1, "$[]$"),
        ("c", 1, "$[]$"),
    ]
    labels[2] = [
        ("b", 2, "$[2:b]$"),
        ("c", 3, "$[2:b]$"),
        ("c", 4, "$[2:b, 4:c]$"),
        ("a", 5, "$[4:c]$"),
        ("b", 4, "$[2:b]$"),
        ("b", 5, "$[2:b, 4:c]$"),
        ("a", 6, "$[2:b, 4:c]$"),
    ]
    labels[3] = [
        ("c", 6, "$[2:b, 4:c]$"),
        ("b", 7, "$[2:b, 4:c]$"),
    ]
    labels[4] = [
        ("b", 8, "$[2:b, 4:c]$"),
        ("b", 9, "$[4:c]$"),
        ("a", 10, "$[4:c]$"),
        ("c", 10, "$[4:c]$"),
        ("c", 11, "$[4:c]$"),
        ("c", 12, "$[]$"),
        ("a", 13, "$[]$"),
        ("b", 13, "$[]$"),
    ]

    eventsn = lambda n: flatten(events[i] for i in range(1, n + 1))
    labelsn = lambda n: flatten(labels[i] for i in range(1, n + 1))

    plot(eventsn(1), "mutex1.pdf", labelsn(1))
    plot(eventsn(2), "mutex2.pdf", labelsn(2))
    plot(eventsn(3), "mutex3.pdf", labelsn(3))
    plot(eventsn(4), "mutex4.pdf", labelsn(4))

if __name__ == "__main__":
    main()
