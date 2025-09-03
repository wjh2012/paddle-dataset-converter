from abc import abstractmethod, ABC
from typing import TypeVar, Generic


T = TypeVar("T")


class RecDataProcessor(ABC, Generic[T]):
    @abstractmethod
    def crop_and_save_words(
        self, label_data: T, image, image_filename: str, save_dir: str
    ):
        """라벨 데이터와 이미지를 받아 단어 영역을 자르고 저장"""
        pass
