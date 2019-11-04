from typing import *
import random

from faker import Faker

from apicheck.core.generator import *

fake = Faker()


def str_processor(minimum: int, maximum: int) -> MaybeCallable[str]:
    def _generate() -> MaybeValue[str]:
        r = fake.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        return r

    if maximum < minimum:
        return fail(AbsentValue("Incorrect maxLength or minLength"))
    return _generate


def object_processor(
        properties: Optional[Properties],
        strategies: List[Strategy]
        ) -> MaybeCallable[AsDefined]:
    def _object_gen_proc(properties: Properties) -> MaybeCallable[AsDefined]:
        def _proc() -> AsDefined:
            return {
                name: next(generator)
                for name, generator
                in property_builder
            }

        property_builder = [
            (name, generator(definition, strategies))
            for name, definition
            in properties.items()
        ]
        return _proc

    if not properties:
        return fail(
            AbsentValue("Can't gen a property-less object without policy")
        )
    return _object_gen_proc(properties)


def int_processor(
        minimum: int,
        maximum: int,
        multiple_of: int
        ) -> MaybeCallable[int]:
    def _generate_simple(min_val: int, max_val: int) -> Callable[[], int]:
        return lambda: random.randint(min_val, max_val)

    def _generate_multiple_of(
            min_val: int,
            max_val: int,
            multiple: int
            ) -> MaybeCallable[int]:
        def _gen() -> int:
            r = random.randint(0, m-1)
            return m_init + r * multiple

        m_s = max_val // multiple
        m_i = min_val // multiple
        m = m_s - m_i
        if m <= 0:
            return fail(
                AbsentValue("No multiple exists within the requested range")
            )
        m_init = multiple + ((m_s - m) * multiple)
        return _gen

    if maximum < minimum:
        return fail(AbsentValue("Invalid Maximum or Minimum"))
    elif multiple_of:
        return _generate_multiple_of(minimum, maximum, multiple_of)
    else:
        return _generate_simple(minimum, maximum)


def list_processor(
        strategies: List[Strategy],
        element_definition: Definition,
        minimum: int,
        maximum: int,
        must_be_unique: bool
        ) -> MaybeCallable[List[Any]]:
    def _must_be_unique() -> MaybeValue[List[Any]]:
        raise NotImplementedError()

    def gen() -> MaybeValue[List[Any]]:
        size = random.randint(minimum, maximum)
        item_gen = generator(element_definition, strategies)
        return [next(item_gen) for _ in range(size)]

    if must_be_unique:
        return _must_be_unique
    else:
        return gen
