# Handles CRUD for notes:
#  - add(), delete(), find(), find_by_tags(), edit()
#  - each note may include one or more tags


class NotesService:
    def __init__(self, store):
        self.store = store  # expects .load() and .save()
