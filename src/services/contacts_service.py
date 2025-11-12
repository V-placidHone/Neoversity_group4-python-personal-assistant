# Handles CRUD operations for contacts:
#  - add(), update(), delete(), search()
#  - validates phone/email before saving


class ContactsService:
    def __init__(self, store):
        self.store = store  # expects .load() and .save()
