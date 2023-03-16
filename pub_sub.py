import time

PUBLISHERS  = dict()
SUBSCRIBERS = dict()
PUBLISHERS_COUNT  = 0
SUBSCRIBERS_COUNT = 0

class Publisher:
	def __init__(self, Id, name, description, img_lnk):
		self.Id   = Id
		self.name = name
		self.description = description
		self.img_lnk = img_lnk
		self.subscribers = list()

	def __repr__(self):
		return f"Publisher {self.name}"

	def add_subscriber(self, subscriber):
		self.subscribers.append(subscriber)

	def remove_subscriber(self, subscriber):
		self.subscribers.remove(subscriber)

	def publish_message(self, message):
		message = message.replace(',', ';') #csv failsafe
		with open(f"{self.Id}.csv", 'a+') as database:
			database.write(f"{time.time()},{message}\n")
		self.notify_subscribers()

	def notify_subscribers(self):
		for subscriber in self.subscribers:
			subscriber.alert(self)


class Subscriber:
	def __init__(self, Id, IP):
		self.Id = Id
		self.IP = IP
		self.subscriptions = list()

	def __repr__(self):
		return f"Subscriber:{self.Id}"

	def subscribe(self, publisher):
		if publisher not in self.subscriptions:
			self.subscriptions.append(publisher)
			publisher.add_subscriber(self)
			print(f"{self.Id} subscribed to {publisher}")
		else: print("Already subscribed!")

	def unsubscribe(self, publisher):
		if publisher in self.subscriptions:
			self.subscriptions.remove(publisher)
			publisher.remove_subscriber(self)
			print(f"{self.name} unsubscribed from {publisher}")
		else: print("Subscription not found!")

	def alert(self, sender):
                print("ALERT RECIEVED")
                messages = ''
                with open(f"{sender.Id}.csv", 'r') as database:
                        messages += str( database.readline().strip().split(',') )

                print(f"{self.name} : Notifications from {sender}: {messages}")


def create_publisher(Id, name, description, img_lnk):
	global PUBLISHERS_COUNT
	PUBLISHERS[Id] = Publisher(Id, name, description, img_lnk)
	print(f"Publisher {name} created")
	PUBLISHERS_COUNT += 1


def create_subscriber(Id, IP):
	global SUBSCRIBERS_COUNT
	SUBSCRIBERS[Id] = Subscriber(Id, IP)
	print(f"Subscriber {Id} created")
	SUBSCRIBERS_COUNT += 1


def static_publishers():
	create_publisher(1101, "Slaypoint", "Roasting Channel")
	create_publisher(2743, "Computerphile", "Learn all about computers and computing world")
	create_publisher(3210, "CodeBullet", "Everything about AI,Games and coding")

if __name__ == "__main__":
	create_publisher(1, "p1", "Desc1", '')
	create_publisher(2, "p2", "Desc2", '')

	create_subscriber("s1", 1)
	create_subscriber("s2", 2)
	create_subscriber("s3", 3)

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
