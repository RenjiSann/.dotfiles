from MyClass import MyClass

MIN = 42
MID = 92
MAX = 142

# test default initialisation with constructor
def test_init():
    c = MyClass()

    assert c.i == MIN

#----------------------------------------------

# test Get function with default value
def test_get_default():
    c = MyClass()

    assert c.Get() == MIN
    assert c.i == MIN

# test Get function with basic value
def test_get_basic():
    c = MyClass()

    val = 69
    c.i = val
    assert c.Get() == val
    assert c.i == val

# test Get function with basic value
def test_get_max():
    c = MyClass()

    c.i = MAX
    assert c.Get() == MAX
    assert c.i == MAX

#----------------------------------------------

# test Set function with min value
def test_set_min():
    c = MyClass()

    assert c.Set(MIN) == MIN
    assert c.i == MIN

# test Set function with random value
def test_set_basic():
    c = MyClass()

    val = 69
    assert c.Set(val) == val
    assert c.i == val

# test Set function with max value
def test_set_max():
    c = MyClass()

    assert c.Set(MAX) == MAX
    assert c.i == MAX

# test Set function with invalid value below min
def test_set_invalid_below_default():
    c = MyClass()

    val = 12
    old = c.i
    assert c.Set(val) == old
    assert old == c.i

# test Set function with invalid value below min with non default value
def test_set_invalid_below():
    c = MyClass()
    c.i = 69

    val = 12
    old = c.i
    assert c.Set(val) == old
    assert old == c.i

# test Set function with invalid value over max
def test_set_invalid_over_default():
    c = MyClass()

    val = 199
    old = c.i
    assert c.Set(val) == old
    assert old == c.i

# test Set function with invalid value over max with non default value
def test_set_invalid_over():
    c = MyClass()
    c.i = 69

    val = 199
    old = c.i
    assert c.Set(val) == old
    assert old == c.i

#----------------------------------------------

# test Incr function with default value
def test_incr_default():
    c = MyClass()

    assert c.Incr() == MIN + 1
    assert c.i == MIN + 1

# test Incr function with basic value
def test_incr_basic():
    c = MyClass()
    c.i = 69

    old = c.i
    assert c.Incr() == old + 1
    assert c.i == old + 1

# test Incr function with max value
def test_incr_max_value():
    c = MyClass()
    c.i = MAX

    assert c.Incr() == MAX
    assert c.i == MAX

#----------------------------------------------

# test Decr function with default value
def test_decr_default():
    c = MyClass()

    assert c.Decr() == MIN
    assert c.i == MIN

# test Decr function with basic value
def test_decr_basic():
    c = MyClass()
    c.i = 69

    old = c.i
    assert c.Decr() == old - 1
    assert c.i == old - 1

# test Decr function with max value
def test_decr_max_value():
    c = MyClass()
    c.i = MAX

    assert c.Decr() == MAX - 1
    assert c.i == MAX - 1

#----------------------------------------------

# test Clear function with default value
def test_clear_default():
    c = MyClass()

    assert c.Clear() == MIN
    assert c.i == MIN

# test Clear function with basic value
def test_clear_basic():
    c = MyClass()
    c.i = 69

    assert c.Clear() == MIN
    assert c.i == MIN

# test Clear function with max value
def test_clear_max_value():
    c = MyClass()
    c.i = MAX

    assert c.Clear() == MIN
    assert c.i == MIN

#----------------------------------------------

# test Mid function with default value
def test_mid_default():
    c = MyClass()

    assert c.Mid() == MID
    assert c.i == MID

# test Mid function with basic value
def test_mid_basic():
    c = MyClass()
    c.i = 69

    assert c.Mid() == MID
    assert c.i == MID

# test Incr function with max value
def test_mid_max_value():
    c = MyClass()
    c.i = MAX

    assert c.Mid() == MID
    assert c.i == MID
