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
