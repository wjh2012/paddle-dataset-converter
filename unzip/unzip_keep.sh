#!/usr/bin/env bash
set -euo pipefail

find . -type f -iname "*.zip" -print0 | while IFS= read -r -d '' zipfile; do
    echo "==> 압축 해제 중: $zipfile"

    # zip 경로에서 .zip 제거 (대소문자 대응)
    dest="${zipfile%.[Zz][Ii][Pp]}"

    # dest가 파일이 아닌 디렉토리로 존재하도록 보장
    mkdir -p "$dest"

    unzip -o "$zipfile" -d "$dest"
    rc=$?
    if [ $rc -eq 0 ]; then
        echo "==> 해제 완료: $zipfile, 원본 zip 삭제"
        rm -- "$zipfile"

        # 새로 풀린 디렉토리 내부의 zip들(대소문자 포함)을 삭제
        echo "==> 추가로 생성된 zip 파일 삭제 중..."
        find "$dest" -type f -iname "*.zip" -exec rm -- {} +
    else
        echo "==> 오류 발생: $zipfile (exit $rc), zip 파일은 삭제하지 않음"
    fi
done