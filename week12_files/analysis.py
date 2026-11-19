
import pandas as pd


# A. 데이터 정제
def 정제(df):
    # 원본 데이터를 보호하기 위해 복사한다.
    df = df.copy()

    # 1. 점수가 비어 있는 행을 삭제한다.
    df = df.dropna(subset=["점수"])
    print("결측치 제거 후:", len(df), "행")

    # 2. 모든 열이 같은 중복 행을 하나만 남긴다.
    df = df.drop_duplicates()
    print("중복 제거 후:", len(df), "행")

    # 3. 반과 과목의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거 후:", len(df), "행")

    # 4. 점수가 0~100 사이인 행만 남긴다.
    df = df[df["점수"].between(0, 100)]
    print("점수 범위 정리 후:", len(df), "행")

    return df


# B. 필터링
def 수학만(df):
    result = df[df["과목"] == "수학"]
    print(result)
    print("수학 행 수:", len(result))
    return result


def 일반_90점이상(df):
    result = df[(df["반"] == "1반") & (df["점수"] >= 90)]
    print(result)
    return result


# C. 그룹화
def 반별과목평균(df):
    반별 = df.groupby("반")["점수"].mean()
    과목별반별 = df.groupby(["과목", "반"])["점수"].mean()

    print("반별 평균:")
    print(반별)

    print("과목별 반별 평균:")
    print(과목별반별)

    return 반별, 과목별반별


# D. 통계
def 반별통계(df):
    result = df.groupby("반")["점수"].agg(
        ["count", "mean", "median", "max"]
    ).round(2)

    print(result)
    return result


def 반별평균(df):
    return df.groupby("반")["점수"].mean()


# 파일 실행 및 분석
if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv")
    clean_df = 정제(df)

    print("\n수학 필터링:")
    수학만(clean_df)

    print("\n1반 90점 이상:")
    일반_90점이상(clean_df)

    print("\n그룹화:")
    반별과목평균(clean_df)

    print("\n반별 통계:")
    반별통계(clean_df)

    print("\n반별 평균:")
    print(반별평균(clean_df))
