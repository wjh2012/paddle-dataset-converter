def convert():
    # basic-ksx1001.txt 읽기 (기준 문자 집합)
    with open("charset/basic-ksx1001.txt", "r", encoding="utf-8") as f:
        basic_set = set(line.strip() for line in f if line.strip())

    # various_char_set_count.txt 읽어서 문자-빈도 dict 생성
    char_count_dict = {}
    with open("./various_forms_of_hangul/various_char_set.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                char, count = parts
                char_count_dict[char] = int(count)

    # basic_set에 없는 문자만 추출
    only_in_results = {
        char: count for char, count in char_count_dict.items() if char not in basic_set
    }

    # 결과 출력
    print("basic-ksx1001.txt에 없는 문자 및 빈도수:")
    for char, count in only_in_results.items():
        print(f"{char}: {count}")


if __name__ == "__main__":
    convert()
