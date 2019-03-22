from apicheck.core.dict_helpers import search

from typing import Callable, List, Any
import sys
import random

from faker import Faker


faker = Faker()


def generator(field: dict) -> Callable[[None], Any]:
    def _str():
        minimum = 10
        maximum = 200
        if "maxLength" in field:
            maximum = field["maxLength"]
        if "minLength" in field:
            minimum = field["minLength"]
        r = faker.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        return r

    def _obj():
        return {
            k: generator(v)()
            for k, v in field["properties"].items()
        }

    def _int():
        minimum = -sys.maxsize-1
        maximum = sys.maxsize
        if "minimum" in field:
            minimum = field["minimum"]
        if "maximum" in field:
            maximum = field["maximum"]
        if "exclusiveMinimum" in field:
            minimum = minimum+1
        if "exclusiveMaximum" in field:
            maximum = maximum-1
        r = random.randint(minimum, maximum)
        if "multipleOf" in field:
            rem = r % field["multipleOf"]
            r = r - rem
        return r

    def _list():
        minimum = 1
        if "minItems" in field:
            minimum = field["minItems"]
        maximum = minimum + 9
        if "maxItems" in field:
            maximum = field["maxItems"]
        size = random.randint(minimum, maximum)
        item_type = field["items"]
        gen = generator(item_type)
        if "uniqueItems" in field and field["uniqueItems"]:
            for _ in range(1000):
                res = [gen() for _ in range(size)]
                if len(res) == len(set(res)):
                    return res
            raise ValueError("Cannot generate unique list with this parameters")
        return [gen() for _ in range(size)]
    
    def _bool():
        n = random.randint(1, 10)
        return n % 2 == 0

    field_type = field["type"]
    if field_type == "string":
        return _str
    elif field_type == "integer":
        return _int
    elif field_type == "object":
        return _obj
    elif field_type == "array":
        return _list
    elif field_type == "boolean":
        return _bool
    else:
        return lambda: None


def test_string_field():
    field = {
        "type": "string",
        "example": "fieldname"
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    res = gen()

    assert isinstance(res, str)
    assert res != ""

    res2 = gen()

    assert isinstance(res2, str)
    assert res2 != ""

    assert res != res2


def test_string_boundaries():
    field = {
        "type": "string",
        "minLength": 2,
        "maxLength": 10,
        "example": "fieldname"
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    gen = generator(field)
    for _ in range(1000):
        res = gen()
        assert len(res) >= 2
        assert len(res) <= 10


def test_integer_field():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "example": 123
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    res = gen()

    assert isinstance(res, int)

    res2 = gen()

    assert isinstance(res, int)

    assert res != res2


def test_integer_boundaries():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "minimum": 0,
        "maximum": 10,
        "example": 123
    }

    gen = generator(field)
    for _ in range(1000):
        res = gen()
        assert res >= 0
        assert res <= 10


def test_integer_exclusive_boundaries():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "minimum": 0,
        "maximum": 10,
        "exclusiveMinimum": True,
        "exclusiveMaximum": True,
        "example": 123
    }

    gen = generator(field)
    for _ in range(1000):
        res = gen()
        assert res > 0
        assert res < 10


def test_integer_multiple_of():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "multipleOf": 10,
        "example": 123
    }

    gen = generator(field)
    for _ in range(1000):
        res = gen()
        assert res % 10 == 0


def test_array_field():
    field = {
        "type": "array",
        "items": {
            "type": "integer",
            "example": 123
        }
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    res = gen()

    assert isinstance(res, List)
    assert len(res) <= 10

    res2 = gen()

    assert isinstance(res2, List)
    assert len(res2) <= 10

    assert res != res2


def test_array_boundaries():
    field = {
        "type": "array",
        "maxItems": 9,
        "minItems": 2,
        "items": {
            "type": "integer",
            "example": 123
        }
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    for _ in range(1000):
        res = gen()
        assert isinstance(res, List)
        assert len(res) <= 9
        assert len(res) >= 2


def test_array_unique():
    field = {
        "type": "array",
        "uniqueItems": True,
        "minItems": 10,
        "items": {
            "type": "integer",
            "minimum": 1,
            "maximum": 40,
            "example": 123
        }
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    for _ in range(1000):
        res = gen()
        assert isinstance(res, List)
        len(res) == len(set(res))


def test_object_field():
    field = {
        "type": "object",
        "description": "An object for describing a "
        "single error that occurred "
        "during the processing of a "
        "request.\n",
        "properties": {
            "reason": {
                "type": "string",
                "description": "What happened to "
                "cause this error. In "
                "most cases, this can "
                "be fixed immediately "
                "by changing the data "
                "you sent in the "
                "request, but in some "
                "cases you will be "
                "instructed to [open "
                "a Support Ticket]("
                "#operation/createTicket) or perform some other action before you can complete the request successfully.\n",
                "example": "fieldname must be a "
                "valid value"
            }
        }
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    res = gen()

    assert isinstance(res, dict)
    assert len(res.keys()) > 0
    assert "reason" in res

    value = res["reason"]

    assert isinstance(value, str)


def test_compund_item():
    compound_item = {
        "type": "object",
        "properties": {
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "description": "An object for describing a "
                        "single error that occurred "
                        "during the processing of a "
                        "request.\n",
                        "properties": {
                            "reason": {
                                "type": "string",
                                "description": "What happened to "
                                "cause this error. In "
                                "most cases, this can "
                                "be fixed immediately "
                                "by changing the data "
                                "you sent in the "
                                "request, but in some "
                                "cases you will be "
                                "instructed to [open "
                                "a Support Ticket]("
                                "#operation/createTicket) or perform some other action before you can complete the request successfully.\n",
                                "example": "fieldname must be a "
                                "valid value"
                            },
                            "field": {
                                "type": "string",
                                "description": "The field in the "
                                "request that caused "
                                "this error. This may "
                                "be a path, separated "
                                "by periods in the "
                                "case of nested "
                                "fields. In some "
                                "cases this may come "
                                "back as \"null\" if "
                                "the error is not "
                                "specific to any "
                                "single element of "
                                "the request.\n",
                                "example": "fieldname"
                            }
                        }
                    }
                }
        }
    }

    gen = generator(compound_item)

    assert isinstance(gen, Callable)

    res = gen()

    assert isinstance(res, dict)
    assert "errors" in res

    error_list = res["errors"]
    assert isinstance(error_list, List)
    assert len(error_list) <= 10

    for item in error_list:
        assert "reason" in item
        assert isinstance(item["reason"], str)
        assert "field" in item
        assert isinstance(item["field"], str)


def test_boolean_field():
    field = {
        "type": "boolean"
    }

    gen = generator(field)

    assert isinstance(gen, Callable)

    res = gen()

    assert isinstance(res, bool)

    res2 = [gen() for _ in range(1000)]
    assert any(res2)
    not_res2 = [not x for x in res2]
    assert any(not_res2)
