# 공공행정문서 압축해제
find . -name "*.zip" -print0 | while IFS= read -r -d '' zipfile; do
    echo "==> 압축 해제 중: $zipfile"

    # 1️⃣ zip 이름에서 확장자 제거
    basename_noext=$(basename "$zipfile" .zip)

    # 2️⃣ 공통 상위 폴더 이름 추출
    parent_folder=$(echo "$basename_noext" | sed -E 's/_[0-9]+$//' | sed -E 's/[0-9]+$//')

    # 3️⃣ 상위 폴더 생성
    target_dir="./$parent_folder"
    mkdir -p "$target_dir"

    # 4️⃣ zip 파일을 공통 상위 폴더에 직접 해제 (=> 내부 디렉토리 구조 유지하며 병합됨)
    unzip -o "$zipfile" -d "$target_dir"
    if [ $? -eq 0 ]; then
        echo "==> 해제 완료: $zipfile, 원본 zip 삭제"
        rm "$zipfile"

        # 내부 zip 파일 삭제
        echo "==> 추가로 생성된 zip 파일 삭제 중..."
        find "$target_dir" -type f -name "*.zip" -exec rm {} +
    else
        echo "==> 오류 발생: $zipfile, zip 파일은 삭제하지 않음"
    fi
done
