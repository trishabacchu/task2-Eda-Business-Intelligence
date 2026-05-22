# Task 2 - Exploratory Data Analysis (EDA)
# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("cleaned_superstore.csv")

# Step 1: Descriptive Statistics
print("=== BASIC STATISTICS ===")
print(df.describe())

print("\n=== SALES BY CATEGORY ===")
print(df.groupby('Category')['Sales'].sum())

print("\n=== TOP 5 STATES BY SALES ===")
print(df.groupby('State')['Sales'].sum().sort_values(ascending=False).head())

print("\n=== CUSTOMER SEGMENTS ===")
print(df['Segment'].value_counts())
# Step 2: Create Visualizations

# Chart 1: Sales by Category (Bar Chart)
plt.figure(figsize=(8,5))
df.groupby('Category')['Sales'].sum().plot(kind='bar', color=['blue','orange','green'])
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('sales_by_category.png')
plt.show()
print("✅ Chart 1 saved!")

# Chart 2: Sales by Region (Pie Chart)
plt.figure(figsize=(8,5))
df.groupby('Region')['Sales'].sum().plot(kind='pie', autopct='%1.1f%%')
plt.title('Sales by Region')
plt.tight_layout()
plt.savefig('sales_by_region.png')
plt.show()
print("✅ Chart 2 saved!")

# Chart 3: Monthly Sales Trend (Line Chart)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
monthly_sales = df.groupby('Month')['Sales'].sum()
plt.figure(figsize=(12,5))
monthly_sales.plot(kind='line', color='blue')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.tight_layout()
plt.savefig('monthly_sales_trend.png')
plt.show()
print("✅ Chart 3 saved!")
# Step 3: SQL for Business Questions
import sqlite3

# Create SQL database from our dataframe
conn = sqlite3.connect('superstore.db')
df.to_sql('superstore', conn, if_exists='replace', index=False)

# Question 1: Top 5 products by revenue
q1 = pd.read_sql_query("""
    SELECT "Product Name", ROUND(SUM(Sales),2) as Total_Sales
    FROM superstore
    GROUP BY "Product Name"
    ORDER BY Total_Sales DESC
    LIMIT 5
""", conn)
print("=== TOP 5 PRODUCTS BY REVENUE ===")
print(q1)

# Question 2: Monthly sales trend
q2 = pd.read_sql_query("""
    SELECT substr("Order Date",1,7) as Month,
    ROUND(SUM(Sales),2) as Monthly_Sales
    FROM superstore
    GROUP BY Month
    ORDER BY Month
    LIMIT 10
""", conn)
print("\n=== MONTHLY SALES TREND ===")
print(q2)

# Question 3: Sales by Customer Segment
q3 = pd.read_sql_query("""
    SELECT Segment, ROUND(SUM(Sales),2) as Total_Sales,
    ROUND(AVG(Profit),2) as Avg_Profit
    FROM superstore
    GROUP BY Segment
    ORDER BY Total_Sales DESC
""", conn)
print("\n=== SALES BY SEGMENT ===")
print(q3)

conn.close()
print("\n✅ SQL Queries Complete!")
# Step 4: Advanced Visualizations

# Chart 4: Heatmap - Correlation between numbers
plt.figure(figsize=(8,6))
numeric_cols = df[['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Days']]
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('heatmap.png')
plt.show()
print("✅ Heatmap saved!")

# Chart 5: Scatter Plot - Discount vs Profit
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category')
plt.title('Discount vs Profit by Category')
plt.tight_layout()
plt.savefig('scatter_discount_profit.png')
plt.show()
print("✅ Scatter plot saved!")

# Chart 6: Box Plot - Sales by Region
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='Region', y='Sales')
plt.title('Sales Distribution by Region')
plt.tight_layout()
plt.savefig('boxplot_region.png')
plt.show()
print("✅ Box plot saved!")
# Step 5: Dashboard Mockup
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Superstore Business Dashboard', fontsize=16)

# Plot 1: Sales by Category
df.groupby('Category')['Sales'].sum().plot(
    kind='bar', ax=axes[0,0], color=['blue','orange','green'])
axes[0,0].set_title('Sales by Category')

# Plot 2: Sales by Region
df.groupby('Region')['Sales'].sum().plot(
    kind='pie', ax=axes[0,1], autopct='%1.1f%%')
axes[0,1].set_title('Sales by Region')

# Plot 3: Monthly Trend
df.groupby('Month')['Sales'].sum().plot(
    kind='line', ax=axes[1,0], color='blue')
axes[1,0].set_title('Monthly Sales Trend')

# Plot 4: Profit by Category
df.groupby('Category')['Profit'].sum().plot(
    kind='bar', ax=axes[1,1], color=['red','green','blue'])
axes[1,1].set_title('Profit by Category')

plt.tight_layout()
plt.savefig('dashboard.png')
plt.show()
print("✅ Dashboard saved!")