def sort_by_unicode(input_path: str, output_path: str = "results.txt") -> None:
    """
    파일 내 각 줄의 문자들을 유니코드 코드 포인트 순서로 정렬하고,
    결과를 지정한 파일(output_path)에 저장합니다.

    :param input_path: 원본 파일 경로 (예: 'sample.txt')
    :param output_path: 정렬된 결과를 저장할 파일 경로 (예: 'results.txt')
    """
    try:
        # 파일 읽기
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        # 빈 줄 제거 및 공백 제거
        chars = [line.strip() for line in lines if line.strip()]

        # 유니코드 코드 포인트 기준 정렬
        sorted_chars = sorted(chars, key=lambda c: ord(c))

        # 결과를 output_path에 저장
        with open(output_path, "w", encoding="utf-8") as f:
            for char in sorted_chars:
                f.write(char + "\n")

        print(f"정렬 완료! 파일에 저장되었습니다: {output_path}")

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_path}")
    except Exception as e:
        print(f"오류 발생: {e}")


# 예제 사용
if __name__ == "__main__":
    sort_by_unicode("charset/special.txt", "results.txt")
