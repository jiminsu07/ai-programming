
import pytest
from load_scores import load_scores


def make_csv(tmp_path, content):
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8")
    return path


# 정상 테스트 1: 정상적인 데이터 읽기
def test_valid_scores(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\n철수,80\n영희,90\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("철수", 80), ("영희", 90)]
    assert skipped == []


# 정상 테스트 2: 헤더만 있는 파일
def test_header_only(tmp_path):
    path = make_csv(tmp_path, "name,score\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []


# 정상 테스트 3: 잘못된 행과 정상 행이 함께 있는 경우
def test_valid_and_invalid_rows(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\n철수,80\n영희,abc\n민수,90\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("철수", 80), ("민수", 90)]
    assert len(skipped) == 1


# 예외 테스트 1: 파일이 없는 경우
def test_file_not_found(tmp_path):
    path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)


# 예외 테스트 2: 열 개수가 2개가 아닌 경우
def test_wrong_column_count(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\n철수,80,추가항목\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


# 경계값 테스트 1: 점수가 비어 있는 경우
def test_empty_score(tmp_path):
    path = make_csv(tmp_path, "name,score\n철수,\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


# 경계값 테스트 2: 점수가 정수가 아닌 경우
def test_non_integer_score(tmp_path):
    path = make_csv(tmp_path, "name,score\n철수,abc\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


# 경계값 테스트 3: 점수 최솟값과 최댓값
@pytest.mark.parametrize("score", [0, 100])
def test_score_boundary(tmp_path, score):
    path = make_csv(
        tmp_path,
        f"name,score\n철수,{score}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("철수", score)]
    assert skipped == []


# 경계값 테스트 4: 점수 범위를 벗어난 경우
@pytest.mark.parametrize("score", [-1, 101])
def test_score_out_of_range(tmp_path, score):
    path = make_csv(
        tmp_path,
        f"name,score\n철수,{score}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


# 경계값 테스트 5: 이름이 비어 있는 경우
def test_empty_name(tmp_path):
    path = make_csv(tmp_path, "name,score\n,80\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
