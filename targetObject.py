class coordinates:
    def __init__(self, name = None, lt_x = None, lt_y = None, rb_x = None, rb_y = None):
        self.name = name
        self.lt_x = lt_x
        self.lt_y = lt_y
        self.rb_x = rb_x
        self.rb_y = rb_y

class person(coordinates):
    def __init__(self, name, lt_x, lt_y, rb_x, rb_y, sit = false):
        super(person, self).__init__(name, lt_x, lt_y, rb_x, rb_y)
        self.sit = sit
class seat(coordinates):
    def __init__(self, name, lt_x, lt_y, rb_x, rb_y):
        super(seat, self).__init__(name, lt_x, lt_y, rb_x, rb_y)
