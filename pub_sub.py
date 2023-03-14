PUBLISHERS  = []
SUBSCRIBERS = []
PUBLISHERS_COUNT  = 0
SUBSCRIBERS_COUNT = 0

class Publisher:
	def __init__(self, Id, name):
		self.id 		 = Id
		self.name		 = name
		self.subscribers = list()

	def __repr__(self):
		return f"Publisher:{self.name}"

	def add_subscriber(self, subscriber):
		self.subscribers.append(subscriber)

	def remove_subscriber(self, subscriber):
		self.subscribers.remove(subscriber)

	def notify_subscribers(self, message=None):
		for subscriber in self.subscribers:
			subscriber.alert(self, message)


class Subscriber:
	def __init__(self, Id, name):
		self.ID			   = Id
		self.name 		   = name
		self.subscriptions = list()

	def __repr__(self):
		return f"Subscriber:{self.name}"

	def subscribe(self, publisher):
		if publisher not in self.subscriptions:
			self.subscriptions.append(publisher)
			publisher.add_subscriber(self)
			print(f"{self.name} subscribed to {publisher}")
		else: print("Already subscribed!")

	def unsubscribe(self, publisher):
		if publisher in self.subscriptions:
			self.subscriptions.remove(publisher)
			publisher.remove_subscriber(self)
			print(f"{self.name} unsubscribed from {publisher}")
		else: print("Subscription not found!")

	def alert(self, sender, message):
		print(f"{self.name} : You have a notification from {sender}: {message}")


def create_publisher(name):
	global PUBLISHERS_COUNT
	PUBLISHERS.append( Publisher(PUBLISHERS_COUNT, name) )
	print(f"Publisher {name} created")
	PUBLISHERS_COUNT += 1

def create_subscriber(name):
	global SUBSCRIBERS_COUNT
	SUBSCRIBERS.append( Subscriber(SUBSCRIBERS_COUNT, name) )
	print(f"Subscriber {name} created")
	SUBSCRIBERS_COUNT += 1

if __name__ == "__main__":
	create_publisher("p1")
	create_publisher("p2")

	create_subscriber("s1")
	create_subscriber("s2")
	create_subscriber("s3")

	print()

	SUBSCRIBERS[0].subscribe( PUBLISHERS[0] )
	SUBSCRIBERS[1].subscribe( PUBLISHERS[0] )
	SUBSCRIBERS[1].subscribe( PUBLISHERS[1] )
	SUBSCRIBERS[2].subscribe( PUBLISHERS[1] )

	print()

	PUBLISHERS[0].notify_subscribers("YO1")
	PUBLISHERS[1].notify_subscribers("YO2")

	SUBSCRIBERS[2].unsubscribe( PUBLISHERS[1] )

	PUBLISHERS[1].notify_subscribers("YO3")