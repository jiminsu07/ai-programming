
import pytest
from load_scores import load_scores


def 파일_만들기(tmp_path, 내용):
    path = tmp_path / "test.csv"
    path.write_text(내용, encoding="utf-8-sig")
    return path


# 정상 테스트
def test_정상적으로_성적을_읽는다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        "name,score\n김하나,88\n이민수,95\n"
    )
    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("이민수", 95)]
    assert skipped == []


def test_헤더만_있는_파일(tmp_path):
    path = 파일_만들기(tmp_path, "name,score\n")
    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []


def test_빈_줄을_건너뛴다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        "name,score\n김하나,88\n\n이민수,95\n"
    )
    kept, skipped = load_scores(path)

    assert len(kept) == 2
    assert skipped == []


def test_동명이인을_모두_남긴다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        "name,score\n김하나,88\n김하나,91\n"
    )
    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("김하나", 91)]
    assert skipped == []


def test_이름에_쉼표가_있다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        'name,score\n"김하나,학생",88\n'
    )
    kept, skipped = load_scores(path)

    assert kept == [("김하나,학생", 88)]
    assert skipped == []


# 예외 테스트
def test_없는_파일은_FileNotFoundError(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "없는파일.csv")


# 잘못된 데이터 테스트
def test_열_개수가_다르면_건너뛴다(tmp_path):
    path = 파일_만들기(
        tmp_path,
        "name,score\n김하나,88,추가\n"
    )
    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


def test_이름이_비어_있으면_건너뛴다(tmp_path):
    path = 파일_만들기(tmp_path, "name,score\n,88\n")
    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


def test_점수가_비어_있으면_건너뛴다(tmp_path):
    path = 파일_만들기(tmp_path, "name,score\n김하나,\n")
    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


def test_점수가_정수가_아니면_건너뛴다(tmp_path):
    path = 파일_만들기(tmp_path, "name,score\n김하나,abc\n")
    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


# 경계값 테스트
@pytest.mark.parametrize(
    "score, expected_kept, expected_skipped",
    [
        (0, 1, 0),
        (100, 1, 0),
        (101, 0, 1),
        (-1, 0, 1),
    ]
)
def test_점수_경계값(
    tmp_path, score, expected_kept, expected_skipped
):
    path = 파일_만들기(
        tmp_path,
        f"name,score\n김하나,{score}\n"
    )
    kept, skipped = load_scores(path)

    assert len(kept) == expected_kept
    assert len(skipped) == expected_skipped
