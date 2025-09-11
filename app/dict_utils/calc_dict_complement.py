import argparse
from pathlib import Path


def _read_txt_to_set(txt_path: Path):
    p = Path(txt_path)
    if not p.exists():
        raise FileNotFoundError(f"파일이 존재하지 않습니다: {p.resolve()}")
    with p.open("r", encoding="utf-8") as f:
        items = {line.strip() for line in f if line.strip()}
    return items


def process(standard_set, test_set, save_dir: Path):
    only_standard = standard_set - test_set
    only_test = test_set - standard_set

    p = Path(save_dir)
    p.mkdir(parents=True, exist_ok=True)

    def _write_list(lines, dest_path: Path):
        sorted_lines = sorted(lines)
        tmp = dest_path.with_suffix(dest_path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8", newline="\n") as f:
            for ch in sorted_lines:
                f.write(ch + "\n")
        tmp.replace(dest_path)

    only_standard_path = p / "only_standard.txt"
    only_test_path = p / "only_test.txt"

    _write_list(only_standard, only_standard_path)
    _write_list(only_test, only_test_path)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="두 텍스트 파일의 차집합을 구해 저장합니다."
    )
    parser.add_argument("--mode", type=str, default=None, help="rec 또는 det")
    parser.add_argument(
        "--standard", "-s", type=str, default=None, help="기준 파일 경로"
    )
    parser.add_argument("--test", "-t", type=str, default=None, help="비교할 파일 경로")
    parser.add_argument(
        "--save_dir", "-o", type=str, default=None, help="결과 저장 디렉토리"
    )

    args = parser.parse_args(argv)

    standard_path = "../../charset/basic-sup.txt"
    test_path = "../../charset/finance_ocr_charset.txt"
    save_dir = "save"

    if args.standard:
        standard_path = args.standard
    if args.test:
        test_path = args.test
    if args.save_dir:
        save_dir = args.save_dir

    standard_path = Path(standard_path).expanduser()
    test_path = Path(test_path).expanduser()
    save_dir = Path(save_dir).expanduser()

    print(f"standard_path -> {standard_path.resolve()}")
    print(f"test_path     -> {test_path.resolve()}")
    print(f"save_dir      -> {save_dir.resolve()}")

    standard_charset = _read_txt_to_set(standard_path)
    test_charset = _read_txt_to_set(test_path)

    process(standard_charset, test_charset, save_dir)


if __name__ == "__main__":
    main()
