import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load all sensitivity data files
maarssen = pd.read_csv('sensitivity_Maarssen.csv')
millingen = pd.read_csv('sensitivity_Millingen.csv')
ommen = pd.read_csv('sensitivity_Ommen.csv')
weesp = pd.read_csv('sensitivity_Weesp.csv')

# Add location identifiers
maarssen['location'] = 'Maarssen'
millingen['location'] = 'Millingen'
ommen['location'] = 'Ommen'
weesp['location'] = 'Weesp'

# Combine all data
all_data = pd.concat([maarssen, millingen, ommen, weesp], ignore_index=True)

# ============ FIGURE 1: Top Parameters by Location ============
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Top 10 Most Important Parameters by Location', fontsize=16, fontweight='bold')

locations = ['Maarssen', 'Millingen', 'Ommen', 'Weesp']
for idx, location in enumerate(locations):
    ax = axes[idx // 2, idx % 2]
    loc_data = all_data[all_data['location'] == location].copy()
    top_params = loc_data.nlargest(10, 'importance')

    # Color code by model type
    colors = ['#1f77b4' if m == 'SimpleModel' else '#ff7f0e' for m in top_params['model']]
    y_pos = np.arange(len(top_params))

    ax.barh(y_pos, top_params['importance'], color=colors, alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{p} ({m})" for p, m in zip(top_params['parameter'], top_params['model'])], fontsize=9)
    ax.set_xlabel('Importance', fontsize=11)
    ax.set_title(f'{location}', fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

# Add legend
from matplotlib.patches import Patch

legend_elements = [Patch(facecolor='#1f77b4', label='SimpleModel'),
                   Patch(facecolor='#ff7f0e', label='ComplexModel')]
fig.legend(handles=legend_elements, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.savefig('sensitivity_top_params_by_location.png', dpi=300, bbox_inches='tight')

# ============ FIGURE 2: Model Comparison for Key Parameters ============
key_params = ['w_t', 'Idry', 'lag_b', 'perc_rate', 'w_b', 'alpha_w', 'Emax']
filtered_data = all_data[all_data['parameter'].isin(key_params)].copy()

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(key_params))
width = 0.15
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

for i, location in enumerate(locations):
    simple_vals = []
    complex_vals = []

    for param in key_params:
        simple_val = filtered_data[(filtered_data['parameter'] == param) &
                                   (filtered_data['location'] == location) &
                                   (filtered_data['model'] == 'SimpleModel')]['importance']
        complex_val = filtered_data[(filtered_data['parameter'] == param) &
                                    (filtered_data['location'] == location) &
                                    (filtered_data['model'] == 'ComplexModel')]['importance']
        simple_vals.append(simple_val.values[0] if len(simple_val) > 0 else 0)
        complex_vals.append(complex_val.values[0] if len(complex_val) > 0 else 0)

    offset = (i - 1.5) * width
    ax.bar(x + offset, simple_vals, width, label=f'{location} (Simple)', color=colors[i], alpha=0.7)
    ax.bar(x + offset, complex_vals, width, bottom=simple_vals, color=colors[i], alpha=0.4, hatch='//')

ax.set_xlabel('Parameter', fontsize=12, fontweight='bold')
ax.set_ylabel('Importance', fontsize=12, fontweight='bold')
ax.set_title('Parameter Importance Comparison: SimpleModel vs ComplexModel', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(key_params, fontsize=11)
ax.legend(loc='upper right', ncol=2, fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('sensitivity_model_comparison.png', dpi=300, bbox_inches='tight')

# ============ FIGURE 3: Tornado Plots (MSE Changes) ============
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('Tornado Plots: MSE Changes for Top Parameters', fontsize=16, fontweight='bold')

for idx, location in enumerate(locations):
    ax = axes[idx // 2, idx % 2]
    loc_data = all_data[all_data['location'] == location].copy()
    top_params = loc_data.nlargest(8, 'importance')

    # Calculate MSE changes from base value
    mse_base = top_params['mse'].values
    mse_up = top_params['mse_up'].values
    mse_down = top_params['mse_down'].values

    change_up = mse_up - mse_base
    change_down = mse_base - mse_down

    y_pos = np.arange(len(top_params))

    # Create tornado plot (bidirectional horizontal bar chart)
    ax.barh(y_pos, -change_down, left=0, height=0.7, color='#2ca02c', alpha=0.7, label='Decrease')
    ax.barh(y_pos, change_up, left=0, height=0.7, color='#d62728', alpha=0.7, label='Increase')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{p} ({m[0]})" for p, m in zip(top_params['parameter'], top_params['model'])], fontsize=9)
    ax.set_xlabel('Change in MSE from Base Value', fontsize=11)
    ax.set_title(f'{location}', fontsize=13, fontweight='bold')
    ax.axvline(x=0, color='black', linewidth=1.5)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    if idx == 0:
        ax.legend(loc='best', fontsize=10)

plt.tight_layout()
plt.savefig('sensitivity_tornado_plots.png', dpi=300, bbox_inches='tight')

# ============ FIGURE 4: Parameter Importance Heatmap ============
# Average importance across models for each parameter-location combination
pivot_data = all_data.groupby(['parameter', 'location'])['importance'].mean().reset_index()
pivot_table = pivot_data.pivot(index='parameter', columns='location', values='importance')

# Select top 15 parameters by maximum importance
pivot_table = pivot_table.loc[pivot_table.max(axis=1).nlargest(15).index]

fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(pivot_table.values, cmap='YlOrRd', aspect='auto')

# Set ticks and labels
ax.set_xticks(np.arange(len(pivot_table.columns)))
ax.set_yticks(np.arange(len(pivot_table.index)))
ax.set_xticklabels(pivot_table.columns, fontsize=11)
ax.set_yticklabels(pivot_table.index, fontsize=10)

plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

# Add text annotations
for i in range(len(pivot_table.index)):
    for j in range(len(pivot_table.columns)):
        value = pivot_table.values[i, j]
        if not np.isnan(value):
            text = ax.text(j, i, f'{value:.1f}' if value < 1000 else f'{value:.0f}',
                           ha="center", va="center",
                           color="black" if value < pivot_table.values.max() / 2 else "white",
                           fontsize=8)

ax.set_title('Parameter Importance Heatmap Across Locations', fontsize=14, fontweight='bold', pad=20)
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Importance', rotation=270, labelpad=20, fontsize=11)

plt.tight_layout()
plt.savefig('sensitivity_heatmap.png', dpi=300, bbox_inches='tight')

plt.show()
print("All figures saved successfully!")
