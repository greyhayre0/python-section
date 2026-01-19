from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    '''Дескриптор данных'''
    def __init__(self, path: str):
        self.path = path

    def __get__(self, instance: 'Model', owner) -> Any: # Либо через класс получаем дескриптор либо через экземпляр то вызов метода чтение
        if instance is None:
            return self
        return self._get_value(instance.payload)

    def __set__(self, instance: 'Model', value: Any) -> None: # Для присвоения атрибута используем кастом функцию запись
        self._set_value(instance.payload, value)

    def _get_value(self, payload: JSON) -> Any: # Извлекатель
        parts = self.path.split('.')
        current = payload
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    def _set_value(self, payload: JSON, value: Any) -> None: # Ну по сути записывает данные
        parts = self.path.split('.')
        current = payload
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
