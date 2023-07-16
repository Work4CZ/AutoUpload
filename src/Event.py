class LabelError(Exception):
    pass


class Event:

    def __init__(self, label: str, data: dict):
        legal_labels = ("device_changes", )
        if label not in legal_labels:
            raise LabelError(f"The label can only be one of {legal_labels}")
        self.label = label
        self.data = data


pass
