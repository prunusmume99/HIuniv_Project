#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
하수도 인프라 분석 노트북 생성 스크립트

이 스크립트는 하수도 인프라 분석을 위한 Jupyter 노트북을 생성합니다.
"""

import os
import json
import pandas as pd
from pathlib import Path

def create_sewer_infrastructure_notebook():
    """하수도 인프라 분석 노트북을 생성합니다."""
    
    # 프로젝트 디렉토리 설정
    project_dir = r"C:\Users\f4141\Desktop\HIuniv_Project"
    
    # 노트북 내용
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 하수도 인프라 분석\n",
                    "\n",
                    "이 노트북은 하수도 인프라 데이터를 분석하고 지수를 계산합니다."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import os\n",
                    "from pathlib import Path\n",
                    "\n",
                    "# 한글 폰트 설정\n",
                    "plt.rcParams['font.family'] = 'Malgun Gothic'\n",
                    "plt.rcParams['axes.unicode_minus'] = False\n",
                    "\n",
                    "# 프로젝트 디렉토리 설정\n",
                    "project_dir = r\"/Users/sullem/yj/HIuniv_Project\"\n",
                    "os.chdir(project_dir)\n",
                    "\n",
                    "print(f\"현재 작업 디렉토리: {os.getcwd()}\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 하수도 인프라 데이터 로드\n",
                    "data_path = os.path.join(project_dir, \"data\", \"raw\", \"Sewer_Coverage_Rate.csv\")\n",
                    "df = pd.read_csv(data_path)\n",
                    "\n",
                    "print(f\"데이터 로드 완료: {len(df)}개 행\")\n",
                    "print(f\"컬럼: {list(df.columns)}\")\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 데이터 전처리\n",
                    "# 숫자 컬럼 변환\n",
                    "numeric_cols = ['총인구(명)', '총면적', '하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률']\n",
                    "\n",
                    "for col in numeric_cols:\n",
                    "    if col in df.columns:\n",
                    "        df[col] = pd.to_numeric(df[col], errors='coerce')\n",
                    "\n",
                    "# 인구밀도 계산\n",
                    "df['인구밀도'] = df['총인구(명)'] / df['총면적']\n",
                    "\n",
                    "# 인구밀도 정규화 (0-1)\n",
                    "df['인구밀도_정규화'] = (df['인구밀도'] - df['인구밀도'].min()) / (df['인구밀도'].max() - df['인구밀도'].min())\n",
                    "\n",
                    "print(\"데이터 전처리 완료\")\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 하수도 인프라 지수 계산\n",
                    "# 가중치 설정\n",
                    "weights = {\n",
                    "    '하수도설치율': 0.3,\n",
                    "    '공공하수처리구역 인구보급률': 0.3,\n",
                    "    '고도처리인구 보급률': 0.2,\n",
                    "    '인구밀도_정규화': 0.2\n",
                    "}\n",
                    "\n",
                    "# 각 지표 정규화 (0-1)\n",
                    "df['하수도설치율_정규화'] = (df['하수도설치율'] - df['하수도설치율'].min()) / (df['하수도설치율'].max() - df['하수도설치율'].min())\n",
                    "df['공공하수처리구역_정규화'] = (df['공공하수처리구역 인구보급률'] - df['공공하수처리구역 인구보급률'].min()) / (df['공공하수처리구역 인구보급률'].max() - df['공공하수처리구역 인구보급률'].min())\n",
                    "df['고도처리_정규화'] = (df['고도처리인구 보급률'] - df['고도처리인구 보급률'].min()) / (df['고도처리인구 보급률'].max() - df['고도처리인구 보급률'].min())\n",
                    "\n",
                    "# 하수도 인프라 지수 계산\n",
                    "df['하수도_인프라_지수'] = (\n",
                    "    df['하수도설치율_정규화'] * weights['하수도설치율'] +\n",
                    "    df['공공하수처리구역_정규화'] * weights['공공하수처리구역 인구보급률'] +\n",
                    "    df['고도처리_정규화'] * weights['고도처리인구 보급률'] +\n",
                    "    df['인구밀도_정규화'] * weights['인구밀도_정규화']\n",
                    ") * 100\n",
                    "\n",
                    "# 인프라 등급 분류\n",
                    "def classify_infrastructure(score):\n",
                    "    if score >= 80:\n",
                    "        return '높음'\n",
                    "    elif score >= 60:\n",
                    "        return '보통'\n",
                    "    elif score >= 40:\n",
                    "        return '낮음'\n",
                    "    else:\n",
                    "        return '매우 낮음'\n",
                    "\n",
                    "df['인프라_등급'] = df['하수도_인프라_지수'].apply(classify_infrastructure)\n",
                    "\n",
                    "print(\"하수도 인프라 지수 계산 완료\")\n",
                    "df[['행정구역명', '하수도_인프라_지수', '인프라_등급']].head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 결과 저장\n",
                    "output_path = os.path.join(project_dir, \"data\", \"processed\", \"sewer_infrastructure_analysis.csv\")\n",
                    "df.to_csv(output_path, index=False, encoding='utf-8')\n",
                    "print(f\"결과가 저장되었습니다: {output_path}\")\n",
                    "\n",
                    "# 인프라 등급별 분포 확인\n",
                    "print(\"\\n=== 인프라 등급별 분포 ===\")\n",
                    "grade_counts = df['인프라_등급'].value_counts()\n",
                    "for grade, count in grade_counts.items():\n",
                    "    print(f\"{grade}: {count}개 ({count/len(df)*100:.1f}%)\")\n",
                    "\n",
                    "# 상위 10개 지역 (인프라 지수 높음)\n",
                    "print(\"\\n=== 상위 10개 지역 (인프라 지수 높음) ===\")\n",
                    "top_10 = df.nlargest(10, '하수도_인프라_지수')[['행정구역명', '하수도_인프라_지수', '인프라_등급']]\n",
                    "print(top_10)"
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
    
    # 노트북 파일 저장
    output_path = os.path.join(project_dir, "notebooks", "02_sewer_infrastructure_analysis.ipynb")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_content, f, ensure_ascii=False, indent=2)
    
    print(f"노트북이 생성되었습니다: {output_path}")

if __name__ == "__main__":
    create_sewer_infrastructure_notebook() 