import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

print("Loading dataset...")
df = pd.read_csv('All_Diets.csv')
df.columns = df.columns.str.strip()

# Clean missing values
df['Protein(g)'].fillna(df['Protein(g)'].mean(), inplace=True)
df['Carbs(g)'].fillna(df['Carbs(g)'].mean(), inplace=True)
df['Fat(g)'].fillna(df['Fat(g)'].mean(), inplace=True)

print("Processing Question 1: Finding top 5 protein-rich recipes per diet...")
top_5_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5).reset_index(drop=True)
top_5_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].to_csv('top_5_protein_recipes.csv', index=False)

print("Processing Question 2: Calculating average protein by diet...")
avg_protein = df.groupby('Diet_type')['Protein(g)'].mean().sort_values(ascending=False).reset_index()
avg_protein.to_csv('avg_protein_by_diet.csv', index=False)

print("Processing Question 3: Extracting most common cuisines...")
common_cuisines = []
for diet, group in df.groupby('Diet_type'):
    mode_cuisine = group['Cuisine_type'].mode()[0]
    count = group['Cuisine_type'].value_counts().max()
    common_cuisines.append({'Diet_type': diet, 'Most_Common_Cuisine': mode_cuisine, 'Count': count})
pd.DataFrame(common_cuisines).to_csv('common_cuisines_by_diet.csv', index=False)

# New metrics
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']
print("New metrics calculated: Protein-to-Carbs ratio and Carbs-to-Fat ratio")

sns.set_theme(style="whitegrid")

# --- CHART 1: Bar chart ---
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean().reset_index()
avg_macros_melted = avg_macros.melt(id_vars='Diet_type', var_name='Macronutrient', value_name='Average(g)')

plt.figure(figsize=(12, 6))
sns.barplot(x='Diet_type', y='Average(g)', hue='Macronutrient', data=avg_macros_melted, palette='viridis')
plt.title(f'Average Macronutrients by Diet Type - {timestamp}', fontsize=14, pad=15)
plt.xlabel('Diet Type', fontsize=12)
plt.ylabel('Average (grams)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('diet_protein_analysis.png', dpi=300)
plt.show()
print("[SUCCESS] Bar chart saved.")

# --- CHART 2: Heatmap ---
plt.figure(figsize=(10, 5))
heatmap_data = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd')
plt.title(f'Macronutrient Heatmap - {timestamp}', fontsize=14)
plt.tight_layout()
plt.savefig('heatmap_macros.png', dpi=300)
plt.show()
print("[SUCCESS] Heatmap saved.")

# --- CHART 3: Scatter plot ---
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=top_protein,
    x='Cuisine_type',
    y='Protein(g)',
    hue='Diet_type',
    s=100
)
plt.title(f'Top 5 Protein-Rich Recipes by Cuisine - {timestamp}', fontsize=14)
plt.xlabel('Cuisine Type', fontsize=12)
plt.ylabel('Protein (g)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('scatter_protein_cuisine.png', dpi=300)
plt.show()
print("[SUCCESS] Scatter plot saved.")

print("\n[SUCCESS] Task 1 processing complete! Files and chart generated.")
print(f"Completed at: {datetime.now()}")
