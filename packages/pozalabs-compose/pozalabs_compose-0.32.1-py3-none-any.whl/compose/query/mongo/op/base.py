from __future__ import annotations

import abc
import functools
import operator
from collections.abc import Callable
from typing import Any, ClassVar

from .types import DictExpression, ListExpression


class Operator:
    @abc.abstractmethod
    def expression(self) -> Any:
        raise NotImplementedError

    def fmap(self, op: Callable[..., Operator]) -> Operator:
        return op(self.expression())


class ComparisonOperator(Operator):
    def __init__(self, field: str, value: Any | None = None):
        self.field = field
        self.value = value

    @abc.abstractmethod
    def expression(self) -> dict[str, Any]:
        raise NotImplementedError


class LogicalOperator(Operator):
    def __init__(self, *ops: Operator):
        self.ops = list(ops)

    @abc.abstractmethod
    def expression(self) -> dict[str, ListExpression]:
        raise NotImplementedError


class GeneralAggregationOperator(Operator):
    mongo_operator: ClassVar[str] = ""

    def __init__(self, *expressions: Any):
        self.expressions = list(expressions)

    def expression(self) -> DictExpression:
        return Evaluable({self.mongo_operator: self.expressions}).expression()


class Stage(Operator):
    @abc.abstractmethod
    def expression(self) -> DictExpression:
        raise NotImplementedError


class Merge(Operator):
    def __init__(self, *ops: Operator, initial: Any):
        self.ops = list(ops)
        self.initial = initial

    def expression(self) -> Any:
        return functools.reduce(operator.or_, [op.expression() for op in self.ops], self.initial)

    @classmethod
    def dict(cls, *ops: Operator) -> Merge:
        return cls(*ops, initial={})


class Flatten(Operator):
    def __init__(self, *ops: Operator | DictExpression | ListExpression):
        self.ops = list(ops)

    def expression(self) -> ListExpression:
        result = []
        for op in self.ops:
            exp = op.expression() if isinstance(op, Operator) else op

            match exp:
                case dict():
                    result.append(exp)
                case list():
                    for e in exp:
                        result.extend([e] if isinstance(e, dict) else Flatten(e).expression())
                case _:
                    raise ValueError(f"Expression must be dict or list, not {type(exp)} ({exp})")

        return result


class OpFilter(Operator):
    def __init__(self, *ops: Operator, predicate: Callable[[Operator], bool]):
        self.ops = list(ops)
        self.predicate = predicate

    def expression(self) -> ListExpression:
        return [op.expression() for op in self.ops if self.predicate(op)]

    @classmethod
    def non_empty(cls, *ops: Operator) -> OpFilter:
        return cls(*ops, predicate=lambda op: op.expression())


class Evaluable(Operator):
    def __init__(self, op: Any):
        self.op = op

    def expression(self) -> Any:
        match self.op:
            case Operator():
                return self.op.expression()
            case dict():
                return {k: Evaluable(v).expression() for k, v in self.op.items()}
            case list():
                return [Evaluable(v).expression() for v in self.op]
            case _:
                return self.op
