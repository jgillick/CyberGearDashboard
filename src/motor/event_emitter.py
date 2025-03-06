class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, listener):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)
        return listener

    def emit(self, event, *args, **kwargs):
        if event in self._listeners:
            for listener in self._listeners[event]:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    print(f"Error calling event handler: {e}")

    def remove_listener(self, event, listener):
        if event in self._listeners:
            self._listeners[event].remove(listener)
            if not self._listeners[event]:
                del self._listeners[event]
