from pydantic import BaseModel, fields
from typing import TypeVar, Generic, Type, Dict
from typing import Literal, get_origin, get_args, Union
import uuid, time


# 현재 클래스 형을 나타내는 TypeVar 생성
T = TypeVar('T', bound='DynamoModel')

class DynamoModel(BaseModel, Generic[T]):
    id: str = fields.Field(default_factory=lambda: str(uuid.uuid4()))
    crt: int = fields.Field(default_factory=lambda: int(time.time()))
    u_b:str = '_'  # 파티션 쿼리용

    @classmethod
    def _table_name(cls):
        return cls._table.get_default()

    @classmethod
    def get_item(cls: Type[T], id: str, consistent_read: bool = True) -> T:
        data = cls.__dynamo__.get_item(
            cls._table_name(), id, consistent_read
        )
        return cls(**data)

    def put_item(self: Type[T], can_overwrite: bool=False)->Dict:
        """
        Save to DB
        :return:
        """
        data = self.__dynamo__.put_item(
            self._table_name(), self.model_dump(), can_overwrite
        )
        return data

    def update_item(self: Type[T]) -> T:
        updated = self.__dynamo__.update_item(
            self._table_name(), self.id, self.model_dump()
        )
        if updated:
            # 반환된 data를 사용하여 인스턴스 업데이트
            for key, value in updated.items():
                setattr(self, key, value)
            return self
        else:
            raise ValueError(f'Cannot update item: {self}')


    @classmethod
    def sync_table(cls):
        """
        테이블이 없으면 생성, 인덱스도 없으면 생성합니다.
        :return:
        """
        cls.__dynamo__.create_table(cls._table_name())
        # 기본 u_ index (파티션 정렬 쿼리용)
        cls.__dynamo__.create_global_index(
            cls._table_name(),
            'u_b', 'S',
            'crt', 'N'
        )
        for partition_key, sort_key in cls._indexes.get_default():
            partition_key_type = extract_dynamodb_type(cls.model_fields[partition_key].annotation)
            if sort_key:
                sort_key_type = extract_dynamodb_type(cls.model_fields[sort_key].annotation)
                cls.__dynamo__.create_global_index(
                    cls._table_name(),
                    partition_key, partition_key_type,
                    sort_key, sort_key_type
                )
            else:
                cls.__dynamo__.create_global_index(
                    cls._table_name(),
                    partition_key, partition_key_type,
                )


def extract_dynamodb_type(annotation) -> str:
    # Optional 타입 처리
    if get_origin(annotation) is Union:
        args = get_args(annotation)
        # Optional[X]는 Union[X, NoneType]과 같으므로, NoneType을 제외하고 처리
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return extract_dynamodb_type(non_none_args[0])

    # Literal 타입 처리
    if get_origin(annotation) is Literal:
        # Literal 내부의 모든 값이 문자열이면 'S', 그렇지 않으면 예외 처리
        args = get_args(annotation)
        if all(isinstance(arg, str) for arg in args):
            return 'S'
        else:
            raise ValueError("DynamoDB does not support this kind of Literal directly.")

    # 기본 타입 처리
    if annotation is int or annotation is float:
        return 'N'
    elif annotation is str:
        return 'S'
    elif annotation is bytes:
        return 'B'

    # 지원되지 않는 타입
    raise ValueError(f"Unsupported type annotation: {annotation}")
