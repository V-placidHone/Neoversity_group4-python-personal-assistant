# Defines the Contact class and additional (auxiliary) classes:
#  - attributes: name, phone, email, address, birthday
#  - helper methods: __str__(), to_dict(), from_dict()


class Field:
    """Base class for all record fields (e.g., Name, Phone, Birthday)."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Address:
    def __init__(self):
        pass


class Birthday:
    def __init__(self):
        pass


class Address:
    def __init__(self):
        pass


class Email:
    def __init__(self):
        pass


class Phone:
    def __init__(self):
        pass


class Name:
    def __init__(self):
        pass


class Contact:
    def __init__(self):
        pass
