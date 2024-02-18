import datetime
class Alarm:
    def __repr__(self):
        return f"Alarm: {self.message} Severity: {self.severity} Timestamp: {self.timestamp}"

    def __str__(self):
        return f"Alarm: {self.message} Severity: {self.severity} Timestamp: {self.timestamp}"

    def __init__(self, message, severity=1):
        self.message = message
        self.severity = severity
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
