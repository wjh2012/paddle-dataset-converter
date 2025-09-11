def sort_by_unicode(input_path: str, output_path: str = "results.txt") -> None:
    try:
        # 파일 읽기
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        # 빈 줄 제거 및 공백 제거
        chars = [line.strip() for line in lines if line.strip()]

        chars = list(set(chars))

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
    sort_by_unicode("../../charset/special.txt", "results.txt")
