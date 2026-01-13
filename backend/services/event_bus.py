subscribers = []

def subscribe(fn):
    subscribers.append(fn)

def publish(event):
    for fn in subscribers:
        fn(event)
