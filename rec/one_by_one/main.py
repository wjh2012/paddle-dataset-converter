import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import importlib
import yaml

from rec.one_by_one.runner import Runner


def load_class(full_class_string):
    """
    문자열로 작성된 모듈 경로에서 클래스를 동적으로 import
    예: 'one_by_one.kor_pub_doc.data_structure.KorPubDocData'
    """
    module_path, class_name = full_class_string.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def validate_config(config):
    """
    YAML에서 필수 key들이 다 있는지 검증
    """
    required_keys = [
        "data_structure",
        "processor_class",
        "image_dir",
        "label_dir",
        "save_dir",
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Config에 '{key}' 항목이 없습니다.")


def run_dataset(dataset_name, config):
    """하나의 dataset 실행 함수"""
    validate_config(config)

    DataClass = load_class(config["data_structure"])
    ProcessorClass = load_class(config["processor_class"])
    processor = ProcessorClass()

    runner = Runner(
        DataClass,
        data_processor=processor,
        label_dir=config["label_dir"],
        image_dir=config["image_dir"],
        save_dir=config["save_dir"],
    )
    runner.run()

    print(f"[완료] {dataset_name} 데이터셋 처리 및 저장이 완료되었습니다.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="실행할 데이터셋 이름 (YAML key). 생략 시 전부 실행",
    )
    parser.add_argument(
        "--recipe",
        type=str,
        default="one_by_one/recipe.yaml",
        help="레시피 YAML 파일 경로",
    )
    args = parser.parse_args()

    # YAML 파일 읽기
    if not os.path.exists(args.recipe):
        raise FileNotFoundError(f"YAML 파일을 찾을 수 없습니다: {args.recipe}")

    with open(args.recipe, "r", encoding="utf-8") as f:
        recipes = yaml.safe_load(f)

    # dataset 지정 여부에 따라 분기
    if args.dataset:
        if args.dataset not in recipes:
            raise ValueError(f"YAML에 정의되지 않은 dataset 이름입니다: {args.dataset}")

        config = recipes[args.dataset]
        run_dataset(args.dataset, config)

    else:
        # 모든 데이터셋 실행
        for dataset_name, config in recipes.items():
            print(f"[시작] {dataset_name} 데이터셋 처리 중...")
            run_dataset(dataset_name, config)
