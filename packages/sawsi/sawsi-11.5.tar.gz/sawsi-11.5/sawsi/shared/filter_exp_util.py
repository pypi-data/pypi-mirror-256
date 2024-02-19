import json
from typing import Literal


class Exp:
    def __init__(self,
                 field, value, condition:Literal['eq', 'neq', 'lte', 'lt', 'gte', 'gt', 'btw', 'stw', 'is_in', 'contains', 'exist', 'not_exist'],
                 operation:Literal['or', 'and']=None, left=None, right=None):
        """
        DynamoDB Filter Expression (Recursive Version)
        :param field:
        :param value:
        :param condition: 'eq' | 'neq' | 'lte' | 'lt' | 'gte' | 'gt' | 'btw' | 'stw' |
                        'is_in' | 'contains' | 'exist' | 'not_exist'
        :param operation:
        :param left:
        :param right:
        """
        allow_conditions = {'eq', 'neq', 'lte', 'lt', 'gte', 'gt', 'btw', 'stw', 'is_in', 'contains', 'exist', 'not_exist'}
        allow_operations = {'or', 'and', None}
        if left and right:
            if operation not in allow_operations:
                raise Exception(f'operation(={operation}) not in {allow_operations}')
        else:
            if condition not in allow_conditions:
                raise Exception(f"condition(={condition}) not in {allow_conditions}")

        self.field = field
        self.value = value
        self.condition = condition
        self.operation = operation
        self.left = left
        self.right = right

    def to_dict(self):
        if self.operation:
            return {
                'left': self.left.to_dict(),
                'operation': self.operation,
                'right': self.right.to_dict(),
            }
        else:
            return {
                'field': self.field,
                'value': self.value,
                'condition': self.condition,
            }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)

    def or_(self, other):
        return Exp(None, None, None, operation='or', left=self, right=other)

    def and_(self, other):
        return Exp(None, None, None, operation='and', left=self, right=other)


if __name__ == '__main__':
    # Example usage
    expression = Exp('name1', 'example', 'contains').or_(
        Exp('name2', 'example2', 'contains').and_(
            Exp('name3', 'example3', 'contains')
        )
    )

    print(expression)
