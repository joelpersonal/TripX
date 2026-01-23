import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def quick_analysis():
    df = pd.read_csv('data/raw/dest.csv')
    
    print(f"Dataset: {len(df)} destinations")
    print(f"Regions: {df['region'].nunique()}")
    print(f"Trip types: {df['trip_type'].nunique()}")
    print(f"Cost range: ${df['avg_cost_per_day'].min()}-${df['avg_cost_per_day'].max()}")
    
    # quick plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # cost by region
    df.boxplot(column='avg_cost_per_day', by='region', ax=axes[0,0])
    axes[0,0].set_title('Cost by Region')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # trip type distribution
    df['trip_type'].value_counts().plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title('Trip Types')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # safety vs popularity
    axes[1,0].scatter(df['safety_score'], df['popularity_score'], alpha=0.6)
    axes[1,0].set_xlabel('Safety Score')
    axes[1,0].set_ylabel('Popularity Score')
    axes[1,0].set_title('Safety vs Popularity')
    
    # season distribution
    df['season_best'].value_counts().plot(kind='pie', ax=axes[1,1])
    axes[1,1].set_title('Best Seasons')
    
    plt.tight_layout()
    plt.show()
    
    print("\nTop budget destinations:")
    budget = df[df['avg_cost_per_day'] <= 50].nsmallest(5, 'avg_cost_per_day')
    print(budget[['destination', 'country', 'avg_cost_per_day', 'trip_type']])
    
    print("\nTop luxury destinations:")
    luxury = df[df['avg_cost_per_day'] >= 150].nlargest(5, 'avg_cost_per_day')
    print(luxury[['destination', 'country', 'avg_cost_per_day', 'trip_type']])

if __name__ == "__main__":
    quick_analysis()