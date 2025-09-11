import argparse
from typing import TypeVar


T = TypeVar("T")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default=None, help="rec 또는 det")
    parser.add_argument(
        "--data_dir",
        type=str,
        default=None,
        help="데이터 경로",
    )
    parser.add_argument(
        "--label_dir",
        type=str,
        default=None,
        help="라벨 경로",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        default=None,
        help="데이터 저장 경로",
    )
    parser.add_argument(
        "--sampler",
        type=int,
        default=None,
        help="샘플 비율 N",
    )
    return parser.parse_args()
