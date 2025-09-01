# 재귀적 unzip
find . -name "*.zip" -print0 | while IFS= read -r -d '' zipfile; do
    echo "==> 압축 해제 중: $zipfile"
    unzip "$zipfile" -d "${zipfile%*.zip}"
done

# 재귀적 zip 삭제
find . -name "*.zip" -delete

# unzip 후 zip 삭제
find . -name "*.zip" -print0 | while IFS= read -r -d '' zipfile; do
    echo "==> 압축 해제 중: $zipfile"
    unzip "$zipfile" -d "${zipfile%*.zip}"
    if [ $? -eq 0 ]; then
        echo "==> 해제 완료: $zipfile, 원본 zip 삭제"
        rm "$zipfile"
    else
        echo "==> 오류 발생: $zipfile, zip 파일은 삭제하지 않음"
    fi
done

# unzip 후 내부 zip 삭제, unzip 한 zip도 삭제
find . -name "*.zip" -print0 | while IFS= read -r -d '' zipfile; do
    echo "==> 압축 해제 중: $zipfile"
    unzip "$zipfile" -d "${zipfile%*.zip}"
    if [ $? -eq 0 ]; then
        echo "==> 해제 완료: $zipfile, 원본 zip 삭제"
        rm "$zipfile"

        # 새로 풀린 폴더 내에 있는 zip 파일들 삭제
        echo "==> 추가로 생성된 zip 파일 삭제 중..."
        find "${zipfile%*.zip}" -type f -name "*.zip" -exec rm {} +
    else
        echo "==> 오류 발생: $zipfile, zip 파일은 삭제하지 않음"
    fi
done

# zip 아닌 파일 삭제
find . -type f ! -name "*.zip" -delete
# 빈 디렉토리 삭제
find . -type d -empty -delete
