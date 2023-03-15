import datetime

PUBLISHERS  = dict()
SUBSCRIBERS = []
PUBLISHERS_COUNT  = 0
SUBSCRIBERS_COUNT = 0

class Publisher:
	def __init__(self, Id, name, description):
		self.Id   = Id
		self.name = name
		self.description = description
		self.subscribers = list()

	def __repr__(self):
		return f"Publisher {self.name}"

	def add_subscriber(self, subscriber):
		self.subscribers.append(subscriber)

	def remove_subscriber(self, subscriber):
		self.subscribers.remove(subscriber)

	def publish_message(self, message):
		message = message.replace(',', ';')#csv failsafe
		today = datetime.date.today()
		date  = f"{today.day}-{today.month}-{today.year}"
		with open(f"{self.Id}.csv", 'a+') as database:
			database.write(f"{date},{self.name},{message}\n")
		self.notify_subscribers()

	def notify_subscribers(self):
		for subscriber in self.subscribers:
			subscriber.alert(self)


class Subscriber:
	def __init__(self, Id, name):
		self.Id   = Id
		self.name = name
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

	def alert(self, sender):
		messages = ''
		with open(f"{sender.Id}.csv", 'r') as database:
			messages += str( database.readline().strip().split(',') )

		print(f"{self.name} : Notifications from {sender}: {messages}")


def create_publisher(Id, name, description):
	global PUBLISHERS_COUNT
	PUBLISHERS[Id] = Publisher(Id, name, description)
	print(f"Publisher {name} created")
	PUBLISHERS_COUNT += 1


def create_subscriber(name):
	global SUBSCRIBERS_COUNT
	SUBSCRIBERS.append( Subscriber(SUBSCRIBERS_COUNT, name) )
	print(f"Subscriber {name} created")
	SUBSCRIBERS_COUNT += 1


def static_publishers():
	create_publisher(1101, "Slaypoint", "Roasting Channel")
	create_publisher(2743, "Computerphile", "Learn all about computers and computing world")
	create_publisher(3210, "CodeBullet", "Everything about AI,Games and coding")

if __name__ == "__main__":
	create_publisher(1, "p1", "Desc1")
	create_publisher(2, "p2", "Desc2")

	create_subscriber("s1")
	create_subscriber("s2")
	create_subscriber("s3")

	print()

	SUBSCRIBERS[0].subscribe( PUBLISHERS[1] )
	SUBSCRIBERS[1].subscribe( PUBLISHERS[1] )
	SUBSCRIBERS[1].subscribe( PUBLISHERS[2] )
	SUBSCRIBERS[2].subscribe( PUBLISHERS[2] )

	print()

	PUBLISHERS[1].publish_message("YO1")
	PUBLISHERS[2].publish_message("YO2")

	SUBSCRIBERS[2].unsubscribe( PUBLISHERS[1] )

	PUBLISHERS[2].publish_message("YO3")
