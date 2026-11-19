
from bug3_logic_fixed import find_max, count_pass


# 최고점 기본 테스트
def test_find_max_normal():
    assert find_max([70, 85, 60, 95]) == 95


# 최고점이 첫 번째인 경우
def test_find_max_first():
    assert find_max([95, 85, 70, 60]) == 95


# 최고점이 마지막인 경우
def test_find_max_last():
    assert find_max([10, 20, 30]) == 30


# 최고점이 중간인 경우
def test_find_max_middle():
    assert find_max([10, 30, 20, 15]) == 30


# 합격자 수 기본 테스트
def test_count_pass_normal():
    assert count_pass([70, 85, 95]) == 3


# 60점도 합격
def test_count_pass_cutoff():
    assert count_pass([60, 60, 59]) == 2


# 모두 불합격인 경우
def test_count_pass_below_cutoff():
    assert count_pass([59, 58, 40]) == 0


# 사용자 지정 합격 기준
def test_count_pass_custom_cutoff():
    assert count_pass([70, 80, 90], cutoff=80) == 2
