import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

class SewerInfrastructureIndex:
    """
    하수도 인프라 지수 계산 클래스
    """
    
    def __init__(self, data_path):
        """
        초기화
        Args:
            data_path (str): 하수도 보급률 데이터 파일 경로
        """
        self.data_path = data_path
        self.df = None
        self.processed_df = None
        self.index_df = None
        
    def load_data(self):
        """데이터 로드"""
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            print(f"데이터 로드 완료: {len(self.df)}개 행, {len(self.df.columns)}개 컬럼")
            return True
        except Exception as e:
            print(f"데이터 로드 실패: {e}")
            return False
    
    def explore_data(self):
        """데이터 탐색"""
        print("=== 데이터 기본 정보 ===")
        print(f"데이터 형태: {self.df.shape}")
        print(f"컬럼명: {list(self.df.columns)}")
        
        print("\n=== 주요 통계 ===")
        numeric_cols = ['총인구(명)', '총면적', '하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률']
        print(self.df[numeric_cols].describe())
        
        print("\n=== 결측값 확인 ===")
        print(self.df.isnull().sum())
        
        print("\n=== 시도별 데이터 수 ===")
        print(self.df['시도'].value_counts())
    
    def clean_data(self):
        """데이터 정제"""
        print("=== 데이터 정제 시작 ===")
        
        # 1. 필요한 컬럼만 선택
        essential_cols = [
            '시도', '구군', '행정구역명', '총인구(명)', '총면적',
            '하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률'
        ]
        
        self.processed_df = self.df[essential_cols].copy()
        
        # 2. 결측값 처리
        self.processed_df = self.processed_df.dropna()
        
        # 3. 이상값 처리 (0보다 작거나 100보다 큰 값)
        for col in ['하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률']:
            self.processed_df = self.processed_df[
                (self.processed_df[col] >= 0) & (self.processed_df[col] <= 100)
            ]
        
        # 4. 인구 밀도 계산 (명/km²)
        self.processed_df['인구밀도'] = self.processed_df['총인구(명)'] / self.processed_df['총면적']
        
        # 5. 인구 밀도 이상값 처리 (너무 높은 값 제거)
        self.processed_df = self.processed_df[self.processed_df['인구밀도'] <= 50000]
        
        print(f"정제 후 데이터: {len(self.processed_df)}개 행")
        
        return self.processed_df
    
    def calculate_infrastructure_index(self, weights=None):
        """
        하수도 인프라 지수 계산
        Args:
            weights (dict): 각 지표별 가중치
        """
        if weights is None:
            weights = {
                '하수도설치율': 0.3,
                '공공하수처리구역 인구보급률': 0.3,
                '고도처리인구 보급률': 0.2,
                '인구밀도_정규화': 0.2
            }
        
        print("=== 하수도 인프라 지수 계산 ===")
        
        # 1. 인구 밀도 정규화 (0-100 스케일)
        scaler = MinMaxScaler(feature_range=(0, 100))
        self.processed_df['인구밀도_정규화'] = scaler.fit_transform(
            self.processed_df[['인구밀도']]
        )
        
        # 2. 가중 평균으로 인프라 지수 계산
        self.processed_df['하수도_인프라_지수'] = (
            self.processed_df['하수도설치율'] * weights['하수도설치율'] +
            self.processed_df['공공하수처리구역 인구보급률'] * weights['공공하수처리구역 인구보급률'] +
            self.processed_df['고도처리인구 보급률'] * weights['고도처리인구 보급률'] +
            self.processed_df['인구밀도_정규화'] * weights['인구밀도_정규화']
        )
        
        # 3. 지수 등급 분류
        self.processed_df['인프라_등급'] = pd.cut(
            self.processed_df['하수도_인프라_지수'],
            bins=[0, 40, 60, 80, 100],
            labels=['매우 낮음', '낮음', '보통', '높음'],
            include_lowest=True
        )
        
        print("인프라 지수 계산 완료")
        return self.processed_df
    
    def analyze_by_region(self):
        """지역별 분석"""
        print("=== 지역별 하수도 인프라 분석 ===")
        
        # 시도별 평균 지수
        region_analysis = self.processed_df.groupby('시도').agg({
            '하수도_인프라_지수': ['mean', 'std', 'count'],
            '하수도설치율': 'mean',
            '공공하수처리구역 인구보급률': 'mean',
            '고도처리인구 보급률': 'mean'
        }).round(2)
        
        region_analysis.columns = [
            '평균_인프라_지수', '표준편차', '지역수',
            '평균_하수도설치율', '평균_공공하수처리보급률', '평균_고도처리보급률'
        ]
        
        print(region_analysis.sort_values('평균_인프라_지수', ascending=False))
        
        return region_analysis
    
    def create_visualizations(self, save_path='results/figures/'):
        """시각화 생성"""
        print("=== 시각화 생성 ===")
        
        # 1. 인프라 지수 분포
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.hist(self.processed_df['하수도_인프라_지수'], bins=30, alpha=0.7, color='skyblue')
        plt.title('하수도 인프라 지수 분포')
        plt.xlabel('인프라 지수')
        plt.ylabel('빈도')
        
        # 2. 등급별 분포
        plt.subplot(2, 2, 2)
        grade_counts = self.processed_df['인프라_등급'].value_counts()
        plt.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%')
        plt.title('인프라 등급별 분포')
        
        # 3. 시도별 평균 지수
        plt.subplot(2, 2, 3)
        region_means = self.processed_df.groupby('시도')['하수도_인프라_지수'].mean().sort_values(ascending=True)
        plt.barh(range(len(region_means)), region_means.values)
        plt.yticks(range(len(region_means)), region_means.index)
        plt.title('시도별 평균 하수도 인프라 지수')
        plt.xlabel('평균 인프라 지수')
        
        # 4. 지표별 상관관계
        plt.subplot(2, 2, 4)
        correlation_cols = ['하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률', '하수도_인프라_지수']
        correlation_matrix = self.processed_df[correlation_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('지표별 상관관계')
        
        plt.tight_layout()
        plt.savefig(f'{save_path}sewer_infrastructure_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"시각화 저장 완료: {save_path}sewer_infrastructure_analysis.png")
    
    def save_results(self, output_path='data/processed/'):
        """결과 저장"""
        print("=== 결과 저장 ===")
        
        # 1. 전체 데이터 저장
        self.processed_df.to_csv(f'{output_path}sewer_infrastructure_index.csv', 
                                index=False, encoding='utf-8-sig')
        
        # 2. 시도별 요약 데이터 저장
        region_summary = self.analyze_by_region()
        region_summary.to_csv(f'{output_path}sewer_infrastructure_by_region.csv', 
                             encoding='utf-8-sig')
        
        # 3. 상위/하위 지역 저장
        top_regions = self.processed_df.nlargest(20, '하수도_인프라_지수')[
            ['시도', '구군', '행정구역명', '하수도_인프라_지수', '인프라_등급']
        ]
        bottom_regions = self.processed_df.nsmallest(20, '하수도_인프라_지수')[
            ['시도', '구군', '행정구역명', '하수도_인프라_지수', '인프라_등급']
        ]
        
        top_regions.to_csv(f'{output_path}top_sewer_infrastructure_regions.csv', 
                          index=False, encoding='utf-8-sig')
        bottom_regions.to_csv(f'{output_path}bottom_sewer_infrastructure_regions.csv', 
                             index=False, encoding='utf-8-sig')
        
        print(f"결과 저장 완료: {output_path}")
        
        return {
            'full_data': self.processed_df,
            'region_summary': region_summary,
            'top_regions': top_regions,
            'bottom_regions': bottom_regions
        }

def main():
    """메인 실행 함수"""
    # 1. 데이터 경로 설정
    data_path = 'data/raw/Sewer_Coverage_Rate.csv'
    
    # 2. 인프라 지수 계산 객체 생성
    sewer_index = SewerInfrastructureIndex(data_path)
    
    # 3. 데이터 로드
    if not sewer_index.load_data():
        return
    
    # 4. 데이터 탐색
    sewer_index.explore_data()
    
    # 5. 데이터 정제
    sewer_index.clean_data()
    
    # 6. 인프라 지수 계산
    sewer_index.calculate_infrastructure_index()
    
    # 7. 지역별 분석
    sewer_index.analyze_by_region()
    
    # 8. 시각화 생성
    sewer_index.create_visualizations()
    
    # 9. 결과 저장
    results = sewer_index.save_results()
    
    print("\n=== 분석 완료 ===")
    print(f"총 {len(sewer_index.processed_df)}개 지역의 하수도 인프라 지수 계산 완료")
    print(f"평균 인프라 지수: {sewer_index.processed_df['하수도_인프라_지수'].mean():.2f}")
    print(f"최고 인프라 지수: {sewer_index.processed_df['하수도_인프라_지수'].max():.2f}")
    print(f"최저 인프라 지수: {sewer_index.processed_df['하수도_인프라_지수'].min():.2f}")

if __name__ == "__main__":
    main() 