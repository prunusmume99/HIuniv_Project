#!/usr/bin/env python3
"""
하수도 인프라 분석 노트북 생성 스크립트 (세종특별자치시 포함)
"""
import json
import os

def create_sewer_infrastructure_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 📊 하수도 인프라 지수 분석\n",
                    "\n",
                    "## 📋 분석 개요\n",
                    "\n",
                    "이 노트북은 한국환경공단의 하수도 보급률 데이터를 분석하여 지역별 하수도 인프라 지수를 계산하고 시각화합니다.\n",
                    "\n",
                    "### 🎯 분석 목표\n",
                    "- 지역별 하수도 인프라 현황 파악\n",
                    "- 하수도 인프라 지수 개발 및 등급 분류\n",
                    "- 지역간 인프라 격차 분석\n",
                    "- 시각화를 통한 인사이트 도출\n",
                    "\n",
                    "### 📊 주요 지표\n",
                    "- 하수도 설치율\n",
                    "- 공공하수처리구역 인구보급률\n",
                    "- 고도처리인구 보급률\n",
                    "- 인구 밀도\n",
                    "\n",
                    "### 🏆 인프라 지수 구성\n",
                    "- 하수도설치율 (30%)\n",
                    "- 공공하수처리구역 인구보급률 (30%)\n",
                    "- 고도처리인구 보급률 (20%)\n",
                    "- 인구밀도 정규화 (20%)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 라이브러리 임포트\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from sklearn.preprocessing import MinMaxScaler\n",
                    "import warnings\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "# 한글 폰트 설정\n",
                    "plt.rcParams['font.family'] = 'DejaVu Sans'\n",
                    "plt.rcParams['axes.unicode_minus'] = False\n",
                    "\n",
                    "print(\"라이브러리 임포트 완료\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📁 전처리된 데이터 로드"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 전처리된 데이터 로드\n",
                    "import os\n",
                    "# 현재 작업 디렉토리 확인\n",
                    "print(f\"현재 작업 디렉토리: {os.getcwd()}\")\n",
                    "# 절대 경로 사용\n",
                    "project_dir = r\"C:\\Users\\MakerSpace\\Desktop\\HIuniv_Project\"\n",
                    "file_path = os.path.join(project_dir, \"data\", \"processed\", \"sewer_infrastructure_processed.csv\")\n",
                    "print(f\"절대 경로: {file_path}\")\n",
                    "print(f\"파일 존재 여부: {os.path.exists(file_path)}\")\n",
                    "df = pd.read_csv(file_path, encoding='utf-8')\n",
                    "\n",
                    "print(f\"전처리된 데이터 로드 완료: {len(df)}개 행, {len(df.columns)}개 컬럼\")\n",
                    "print(f\"컬럼명: {list(df.columns)}\")\n",
                    "print(f\"\\n시도별 데이터 개수:\")\n",
                    "print(df['시도'].value_counts())\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🔍 데이터 탐색"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 기본 정보 확인\n",
                    "print(\"=== 데이터 기본 정보 ===\")\n",
                    "print(df.info())\n",
                    "\n",
                    "print(\"\\n=== 기술 통계 ===\")\n",
                    "print(df.describe())\n",
                    "\n",
                    "print(\"\\n=== 결측값 현황 ===\")\n",
                    "print(df.isnull().sum())"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📊 하수도 인프라 지수 계산"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 가중치 설정\n",
                    "weights = {\n",
                    "    '하수도설치율': 0.3,\n",
                    "    '공공하수처리구역 인구보급률': 0.3,\n",
                    "    '고도처리인구 보급률': 0.2,\n",
                    "    '인구밀도_정규화': 0.2\n",
                    "}\n",
                    "\n",
                    "# 인구 밀도 정규화 (0-100 스케일)\n",
                    "scaler = MinMaxScaler(feature_range=(0, 100))\n",
                    "df['인구밀도_정규화'] = scaler.fit_transform(df[['인구밀도']])\n",
                    "\n",
                    "# 가중 평균으로 인프라 지수 계산\n",
                    "df['하수도_인프라_지수'] = (\n",
                    "    df['하수도설치율'] * weights['하수도설치율'] +\n",
                    "    df['공공하수처리구역 인구보급률'] * weights['공공하수처리구역 인구보급률'] +\n",
                    "    df['고도처리인구 보급률'] * weights['고도처리인구 보급률'] +\n",
                    "    df['인구밀도_정규화'] * weights['인구밀도_정규화']\n",
                    ")\n",
                    "\n",
                    "# 지수 등급 분류\n",
                    "df['인프라_등급'] = pd.cut(\n",
                    "    df['하수도_인프라_지수'],\n",
                    "    bins=[0, 40, 60, 80, 100],\n",
                    "    labels=['매우 낮음', '낮음', '보통', '높음'],\n",
                    "    include_lowest=True\n",
                    ")\n",
                    "\n",
                    "print(\"하수도 인프라 지수 계산 완료\")\n",
                    "print(f\"평균 인프라 지수: {df['하수도_인프라_지수'].mean():.2f}\")\n",
                    "print(f\"최고 인프라 지수: {df['하수도_인프라_지수'].max():.2f}\")\n",
                    "print(f\"최저 인프라 지수: {df['하수도_인프라_지수'].min():.2f}\")\n",
                    "\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📈 시각화"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 1. 인프라 지수 분포\n",
                    "plt.figure(figsize=(15, 10))\n",
                    "\n",
                    "plt.subplot(2, 3, 1)\n",
                    "plt.hist(df['하수도_인프라_지수'], bins=30, alpha=0.7, color='skyblue')\n",
                    "plt.title('하수도 인프라 지수 분포')\n",
                    "plt.xlabel('인프라 지수')\n",
                    "plt.ylabel('빈도')\n",
                    "\n",
                    "# 2. 등급별 분포\n",
                    "plt.subplot(2, 3, 2)\n",
                    "grade_counts = df['인프라_등급'].value_counts()\n",
                    "plt.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%')\n",
                    "plt.title('인프라 등급별 분포')\n",
                    "\n",
                    "# 3. 시도별 평균 지수\n",
                    "plt.subplot(2, 3, 3)\n",
                    "region_means = df.groupby('시도')['하수도_인프라_지수'].mean().sort_values(ascending=True)\n",
                    "plt.barh(range(len(region_means)), region_means.values)\n",
                    "plt.yticks(range(len(region_means)), region_means.index)\n",
                    "plt.title('시도별 평균 하수도 인프라 지수')\n",
                    "plt.xlabel('평균 인프라 지수')\n",
                    "\n",
                    "# 4. 지표별 상관관계\n",
                    "plt.subplot(2, 3, 4)\n",
                    "correlation_cols = ['하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률', '하수도_인프라_지수']\n",
                    "correlation_matrix = df[correlation_cols].corr()\n",
                    "sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)\n",
                    "plt.title('지표별 상관관계')\n",
                    "\n",
                    "# 5. 인구 밀도 vs 인프라 지수\n",
                    "plt.subplot(2, 3, 5)\n",
                    "plt.scatter(df['인구밀도'], df['하수도_인프라_지수'], alpha=0.6)\n",
                    "plt.xlabel('인구 밀도 (명/km²)')\n",
                    "plt.ylabel('하수도 인프라 지수')\n",
                    "plt.title('인구 밀도 vs 인프라 지수')\n",
                    "\n",
                    "# 6. 등급별 인구 밀도 분포\n",
                    "plt.subplot(2, 3, 6)\n",
                    "sns.boxplot(data=df, x='인프라_등급', y='인구밀도')\n",
                    "plt.title('등급별 인구 밀도 분포')\n",
                    "plt.xticks(rotation=45)\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🏆 상위/하위 지역 분석"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 상위 20개 지역\n",
                    "top_regions = df.nlargest(20, '하수도_인프라_지수')[\n",
                    "    ['시도', '행정구역명', '하수도_인프라_지수', '인프라_등급', '하수도설치율', '공공하수처리구역 인구보급률']\n",
                    "]\n",
                    "\n",
                    "print(\"=== 상위 20개 지역 ===\")\n",
                    "print(top_regions)\n",
                    "\n",
                    "# 하위 20개 지역\n",
                    "bottom_regions = df.nsmallest(20, '하수도_인프라_지수')[\n",
                    "    ['시도', '행정구역명', '하수도_인프라_지수', '인프라_등급', '하수도설치율', '공공하수처리구역 인구보급률']\n",
                    "]\n",
                    "\n",
                    "print(\"\\n=== 하위 20개 지역 ===\")\n",
                    "print(bottom_regions)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🏛️ 시도별 분석"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 시도별 통계\n",
                    "region_stats = df.groupby('시도').agg({\n",
                    "    '하수도_인프라_지수': ['mean', 'std', 'min', 'max', 'count'],\n",
                    "    '하수도설치율': 'mean',\n",
                    "    '공공하수처리구역 인구보급률': 'mean',\n",
                    "    '고도처리인구 보급률': 'mean',\n",
                    "    '인구밀도': 'mean'\n",
                    "}).round(2)\n",
                    "\n",
                    "region_stats.columns = [\n",
                    "    '평균_인프라지수', '표준편차', '최소값', '최대값', '지역수',\n",
                    "    '평균_하수도설치율', '평균_공공하수처리구역', '평균_고도처리', '평균_인구밀도'\n",
                    "]\n",
                    "\n",
                    "print(\"=== 시도별 하수도 인프라 통계 ===\")\n",
                    "print(region_stats.sort_values('평균_인프라지수', ascending=False))\n",
                    "\n",
                    "# 시도별 등급 분포\n",
                    "grade_by_region = pd.crosstab(df['시도'], df['인프라_등급'])\n",
                    "print(\"\\n=== 시도별 인프라 등급 분포 ===\")\n",
                    "print(grade_by_region)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 💾 결과 저장"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 결과 디렉토리 생성\n",
                    "import os\n",
                    "# 절대 경로 사용\n",
                    "project_dir = r\"C:\\Users\\MakerSpace\\Desktop\\HIuniv_Project\"\n",
                    "results_dir = os.path.join(project_dir, \"results\")\n",
                    "processed_dir = os.path.join(project_dir, \"data\", \"processed\")\n",
                    "\n",
                    "os.makedirs(results_dir, exist_ok=True)\n",
                    "os.makedirs(processed_dir, exist_ok=True)\n",
                    "\n",
                    "# 분석 결과 저장\n",
                    "analysis_file = os.path.join(processed_dir, \"sewer_infrastructure_analysis.csv\")\n",
                    "region_file = os.path.join(results_dir, \"sewer_infrastructure_by_region.csv\")\n",
                    "\n",
                    "df.to_csv(analysis_file, index=False, encoding='utf-8-sig')\n",
                    "region_stats.to_csv(region_file, encoding='utf-8-sig')\n",
                    "\n",
                    "print(\"=== 분석 결과 저장 완료 ===\")\n",
                    "print(f\"1. 전체 분석 결과: {analysis_file}\")\n",
                    "print(f\"2. 시도별 통계: {region_file}\")\n",
                    "\n",
                    "# 요약 통계 출력\n",
                    "print(f\"\\n=== 분석 요약 ===\")\n",
                    "print(f\"총 분석 지역: {len(df)}개\")\n",
                    "print(f\"평균 하수도 인프라 지수: {df['하수도_인프라_지수'].mean():.2f}\")\n",
                    "print(f\"세종특별자치시 포함 지역: {len(df[df['시도'] == '세종특별자치시'])}개\")\n",
                    "print(f\"세종특별자치시 평균 인프라 지수: {df[df['시도'] == '세종특별자치시']['하수도_인프라_지수'].mean():.2f}\")"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    notebook_path = 'notebooks/02_sewer_infrastructure_analysis.ipynb'
    os.makedirs('notebooks', exist_ok=True)
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    print(f"하수도 인프라 분석 노트북 생성 완료: {notebook_path}")
    return notebook_path

def main():
    print("=== 하수도 인프라 분석 노트북 생성 (세종특별자치시 포함) ===")
    notebook_path = create_sewer_infrastructure_notebook()
    print(f"\n노트북 생성 완료: {notebook_path}")
    print("\n노트북을 실행하려면:")
    print("jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb")

if __name__ == "__main__":
    main() 