"""
Machine Learning:
- Train RF, XGBoost, Gradient Boosting to predict LST
- Feature importance analysis
- Save models for 2030 prediction
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import os

print("=" * 60)
print("MACHINE LEARNING: Predicting LST from Environmental Features")
print("=" * 60)

# Load master
df = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
print(f"Loaded {len(df)} rows")

# Drop missing
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])
print(f"Clean rows: {len(df)}")

# ============================================================
# FEATURES AND TARGET
# ============================================================
feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year']
target_col = 'LST'

X = df[feature_cols].values
y = df[target_col].values

print(f"\nFeatures: {feature_cols}")
print(f"Target: {target_col}")
print(f"Samples: {len(X)}")

# Train/test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# ============================================================
# 1. RANDOM FOREST
# ============================================================
print()
print("=" * 60)
print("1. RANDOM FOREST")
print("=" * 60)

rf = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

rf_mae = mean_absolute_error(y_test, y_pred_rf)
rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
rf_r2 = r2_score(y_test, y_pred_rf)

print(f"MAE:  {rf_mae:.4f}")
print(f"RMSE: {rf_rmse:.4f}")
print(f"R²:   {rf_r2:.4f}")

# ============================================================
# 2. XGBOOST
# ============================================================
print()
print("=" * 60)
print("2. XGBOOST")
print("=" * 60)

xgb_model = xgb.XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

xgb_mae = mean_absolute_error(y_test, y_pred_xgb)
xgb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
xgb_r2 = r2_score(y_test, y_pred_xgb)

print(f"MAE:  {xgb_mae:.4f}")
print(f"RMSE: {xgb_rmse:.4f}")
print(f"R²:   {xgb_r2:.4f}")

# ============================================================
# 3. GRADIENT BOOSTING
# ============================================================
print()
print("=" * 60)
print("3. GRADIENT BOOSTING")
print("=" * 60)

gb = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)

gb_mae = mean_absolute_error(y_test, y_pred_gb)
gb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_gb))
gb_r2 = r2_score(y_test, y_pred_gb)

print(f"MAE:  {gb_mae:.4f}")
print(f"RMSE: {gb_rmse:.4f}")
print(f"R²:   {gb_r2:.4f}")

# ============================================================
# 4. MODEL COMPARISON
# ============================================================
print()
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

comparison = pd.DataFrame({
    'Model': ['Random Forest', 'XGBoost', 'Gradient Boosting'],
    'MAE': [rf_mae, xgb_mae, gb_mae],
    'RMSE': [rf_rmse, xgb_rmse, gb_rmse],
    'R2': [rf_r2, xgb_r2, gb_r2]
})
print(comparison.round(4).to_string(index=False))
comparison.to_csv("03_results/tables/model_comparison.csv", index=False)

# ============================================================
# 5. FEATURE IMPORTANCE
# ============================================================
importance = pd.DataFrame({
    'Feature': feature_cols,
    'RF_Importance': rf.feature_importances_,
    'XGB_Importance': xgb_model.feature_importances_,
    'GB_Importance': gb.feature_importances_
}).sort_values('RF_Importance', ascending=False)

print()
print("Feature Importance:")
print(importance.round(4).to_string(index=False))
importance.to_csv("03_results/tables/feature_importance.csv", index=False)

# Plot feature importance
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(feature_cols))
width = 0.25
ax.bar(x - width, importance.set_index('Feature').loc[feature_cols, 'RF_Importance'],
       width, label='Random Forest', color='forestgreen')
ax.bar(x, importance.set_index('Feature').loc[feature_cols, 'XGB_Importance'],
       width, label='XGBoost', color='steelblue')
ax.bar(x + width, importance.set_index('Feature').loc[feature_cols, 'GB_Importance'],
       width, label='Gradient Boosting', color='coral')
ax.set_xticks(x)
ax.set_xticklabels(feature_cols)
ax.set_ylabel('Importance')
ax.set_title('Feature Importance for LST Prediction')
ax.legend()
plt.tight_layout()
plt.savefig("03_results/figures/feature_importance.png", dpi=150)
plt.close()

# ============================================================
# 6. ACTUAL VS PREDICTED PLOT
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(y_test, y_pred_xgb, alpha=0.3, s=5, c='steelblue')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
        'r--', linewidth=2, label='Perfect prediction')
ax.set_xlabel('Actual LST (°C)', fontsize=12)
ax.set_ylabel('Predicted LST (°C)', fontsize=12)
ax.set_title(f'XGBoost: Actual vs Predicted LST (R² = {xgb_r2:.3f})', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("03_results/figures/actual_vs_predicted.png", dpi=150)
plt.close()

# ============================================================
# 7. SAVE BEST MODEL
# ============================================================
best_idx = comparison['R2'].idxmax()
best_name = comparison.loc[best_idx, 'Model']
best_r2 = comparison.loc[best_idx, 'R2']
print(f"\n🏆 Best model: {best_name} (R² = {best_r2:.4f})")

os.makedirs("03_results/models", exist_ok=True)
if best_name == 'Random Forest':
    joblib.dump(rf, "03_results/models/best_model_lst.pkl")
elif best_name == 'XGBoost':
    joblib.dump(xgb_model, "03_results/models/best_model_lst.pkl")
else:
    joblib.dump(gb, "03_results/models/best_model_lst.pkl")

print(f"Model saved to: 03_results/models/best_model_lst.pkl")
print()
print("=" * 60)
print("✅ Machine learning complete")
print("=" * 60)