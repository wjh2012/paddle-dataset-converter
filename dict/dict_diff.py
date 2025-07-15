def convert():
    # 첫 번째 파일 읽기 (list -> set 변환)
    with open("basic.txt", "r", encoding="utf-8") as f:
        ksx1001 = set(line.strip() for line in f if line.strip())

    # 두 번째 파일 읽기 (list -> set 변환)
    with open("ppocrv5_korean_dict.txt", "r", encoding="utf-8") as f:
        ppocrv5_korean_dict = set(line.strip() for line in f if line.strip())

    # ksx1001에만 있는 글자
    only_in_ksx1001 = ksx1001 - ppocrv5_korean_dict

    # ppocrv5_korean_dict에만 있는 글자
    only_in_ppocrv5 = ppocrv5_korean_dict - ksx1001

    # 결과 출력
    print("ksx1001.txt에만 있는 글자:", only_in_ksx1001)
    print("ppocrv5_korean_dict.txt에만 있는 글자:", only_in_ppocrv5)


if __name__ == "__main__":
    convert()
