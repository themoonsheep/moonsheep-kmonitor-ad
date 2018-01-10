from django.db import models


# TODO: move to moonsheep
class MyIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True

        super().__init__(*args, **kwargs)


class MyCharField(models.CharField):
    """
    By default can be blank and null. Default length: 128
    """

    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 128

        super().__init__(*args, **kwargs)


class PercentField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        if 'decimal_places' not in kwargs:
            kwargs['decimal_places'] = 2
        if 'max_digits' not in kwargs:
            kwargs['max_digits'] = 3

        super().__init__(*args, **kwargs)


class AmountField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        if 'decimal_places' not in kwargs:
            kwargs['decimal_places'] = 2
        if 'max_digits' not in kwargs:
            kwargs['max_digits'] = 12

        super().__init__(*args, **kwargs)
