import itertools
from heapq import *


class Queue:
    queue = []

    def empty(self):
        return len(self.queue) == 0

    def dequeue(self):
        return self.queue.pop()

    def size(self):
        return len(self.queue)

    def enqueue(self, item):
        self.queue.insert(0, item)


class PriorityQueue:
    pq = []  # list of entries arranged in a heap
    entry_finder = {}  # mapping of tasks to entries
    REMOVED = '<removed-task>'  # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    def empty(self):
        for entry in self.entry_finder:
            if entry != self.REMOVED:
                return False
        return True

    def queue(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def dequeue(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, task
        raise KeyError('pop from an empty priority queue')