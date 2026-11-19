
import pytest
from load_scores import load_scores


def 파일_만들기(tmp_path, 내용):
    path = tmp_path / "test.csv"
    path.write_text(내용, encoding="utf-8-sig")
    return path


# 정상 ① 평범한 파일
def test_정상_파일을_읽는다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        "name,score\n김하나,88\n이민수,95\n"
    )
    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("이민수", 95)]
    assert skipped == []


# 정상 ② 빈 줄 건너뛰기
def test_빈_줄은_건너뛴다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        "name,score\n김하나,88\n\n이민수,95\n"
    )
    kept, skipped = load_scores(path)

    assert len(kept) == 2
    assert skipped == []


# 정상 ③ 이름에 쉼표가 있는 경우
def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        'name,score\n"김하나,학생",88\n'
    )
    kept, skipped = load_scores(path)

    assert kept == [("김하나,학생", 88)]
    assert skipped == []


# 예외 ① 없는 파일
def test_없는_파일이면_오류가_난다(tmp_path):
    path = tmp_path / "없는파일.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)


# 예외 ② 헤더만 있는 파일
def test_헤더만_있으면_빈_결과가_나온다(tmp_path):
    path = 파일_만들기(tmp_path, "name,score\n")
    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []


# 경계값 0점, 100점, 101점
@pytest.mark.parametrize(
    "점수, 유효한가",
    [
        (0, True),
        (100, True),
        (101, False),
    ]
)
def test_점수_경계값(tmp_path, 점수, 유효한가):
    path = 파일_만들기(
        tmp_path,
        f"name,score\n김하나,{점수}\n"
    )
    kept, skipped = load_scores(path)

    assert (len(kept) == 1) == 유효한가
    assert (len(skipped) == 1) == (not 유효한가)
