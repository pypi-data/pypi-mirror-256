from pydantic import BaseModel, fields
from typing import TypeVar, Generic, Type, Dict, Tuple
from typing import Literal, get_origin, get_args, Union, Any, List, Iterator
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
        """
        아이템을 가져와 객체로 반환합니다.
        :param id: item.id
        :param consistent_read:
        :return:
        """
        data = cls.__dynamo__.get_item(
            cls._table_name(), id, consistent_read
        )
        return cls(**data)

    def put(self: Type[T], can_overwrite: bool=False)->Dict:
        """
        Save (create) item to DB
        :return:
        """
        data = self.__dynamo__.put_item(
            self._table_name(), self.model_dump(), can_overwrite
        )
        return data

    def update(self: Type[T]) -> T:
        """
        Update item to DB with state of this instance
        :return:
        """
        updated = self.__dynamo__.update_item(
            self._table_name(), self.id, self.model_dump()
        )
        return self

    def delete(self: Type[T]) -> None:
        """
        Delete Item
        :return:
        """
        self.__dynamo__.delete_item(
            self._table_name(), self.id
        )

    @classmethod
    def generate(cls: Type[T], pk_field:str, pk_value:Any,
                    sk_condition:Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"], sk_field:str, sk_value:Any,
                    sk_second_value:Any=None, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Dict=None, reverse:bool=False, limit:int=10000, consistent_read:bool=False,
                    recursive_filters:Dict=None) -> Iterator[T]:
        """
        Query and get all items by generator
        :param pk_field: Field name to query (EX: 'user_id')
        :param pk_value: Field value to query (EX: 'uui21-sqtx54-er2367-jsk36s')
        :param sk_condition: Sort key condition Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"]
        :param sk_field: Sort key field name to query (EX: 'crt')
        :param sk_value: Sort key field value to query with sk_condition (EX: 1645437454) [Non-required]
        :param sk_second_value: If you want to use sk_condition "btw" (between), You can query like "sk_value <= sk_field <= sk_second_value" [Non-required]
        :param filters: Filters
        :param start_key:
        :param reverse:
        :param limit:
        :param consistent_read:
        :param recursive_filters:
        :return:
        """
        gen = cls.__dynamo__.generate_items(
            cls._table_name(), pk_field=pk_field, pk_value=pk_value,
            sk_condition=sk_condition, sk_field=sk_field, sk_value=sk_value, sk_second_value=sk_second_value,
            filters=filters,
            start_key=start_key, reverse=reverse, limit=limit, consistent_read=consistent_read,
            recursive_filters=recursive_filters
        )
        for data in gen:
            yield cls(**data)

    @classmethod
    def query(cls: Type[T], pk_field:str, pk_value:Any,
                    sk_condition:Literal["eq", "lte", "lt", "gte", "gt", "btw", "stw"], sk_field:str, sk_value:Any,
                    sk_second_value:Any=None, filters:List[Dict[Literal["field", "condition", "value"], Any]]=None,
                    start_key:Dict=None, reverse:bool=False, limit:int=10000, consistent_read:bool=False,
                    recursive_filters:Dict=None) -> Tuple[List[T], str]:
        datas, end_key = cls.__dynamo__.query_items(
            cls._table_name(), pk_field=pk_field, pk_value=pk_value,
            sk_condition=sk_condition, sk_field=sk_field, sk_value=sk_value, sk_second_value=sk_second_value,
            filters=filters,
            start_key=start_key, reverse=reverse, limit=limit, consistent_read=consistent_read,
            recursive_filters=recursive_filters
        )
        return [cls(**data) for data in datas], end_key


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
