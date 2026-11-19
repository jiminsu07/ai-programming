
import pytest
from bug3_logic import find_max, count_pass


# 정상 테스트 1: 가장 큰 값 찾기
def test_find_max_normal():
    assert find_max([70, 85, 60, 95]) == 95


# 정상 테스트 2: 가장 큰 값이 첫 번째인 경우
def test_find_max_first():
    assert find_max([95, 85, 70, 60]) == 95


# 정상 테스트 3: 가장 큰 값이 중간에 있는 경우
def test_find_max_middle():
    assert find_max([10, 30, 20, 15]) == 30


# 정상 테스트 4: 합격자 수 세기
def test_count_pass_normal():
    assert count_pass([70, 85, 95]) == 3


# 경계값 테스트 1: 마지막 점수가 가장 큰 경우
def test_find_max_last_element():
    assert find_max([10, 20, 30]) == 30


# 경계값 테스트 2: 기준점 60점도 합격
def test_count_pass_cutoff():
    assert count_pass([60, 60, 59]) == 2


# 경계값 테스트 3: 기준점보다 낮은 점수
def test_count_pass_below_cutoff():
    assert count_pass([59, 58, 40]) == 0


# 경계값 테스트 4: 기준점을 직접 지정
def test_count_pass_custom_cutoff():
    assert count_pass([70, 80, 90], cutoff=80) == 2

