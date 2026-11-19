
import pandas as pd
from analysis import 정제, 반별평균

df = pd.read_csv("scores_2026.csv")
clean_df = 정제(df)

mini = pd.read_csv("mini.csv")
clean_mini = 정제(mini)


def test_정제후_100행():
    assert len(clean_df) == 100


def test_반은_두종류():
    assert set(clean_df["반"].unique()) == {"1반", "2반"}


def test_반별합계는_전체합계와_같다():
    반별합계 = clean_df.groupby("반")["점수"].sum().sum()
    전체합계 = clean_df["점수"].sum()
    assert 반별합계 == 전체합계


def test_mini_1반평균은_80():
    평균 = 반별평균(clean_mini)
    assert 평균["1반"] == 80.0


# 일부러 실패시키는 테스트
