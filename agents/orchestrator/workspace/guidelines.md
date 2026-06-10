# Research Guidelines — Spaceship Titanic

## Competition summary
Binary classification: predict `Transported` (True/False). Metric: Accuracy. Baseline LightGBM CV = 0.8032 ± 0.0078. Public LB top ~0.830.

## CV strategy
- **StratifiedGroupKFold(n_splits=5)**, groups = first 4 chars of PassengerId (GGGG from GGGG_PP format)
- Target rate per fold: ~50.3% (very stable, CV=0.00014)
- Never split group members across train/val — this is the main leakage vector to avoid

## Key data insights (from dp_001)
- Class balance: 50.4% Transported=True (essentially balanced, no weighting needed)
- Missing values: ~180-220 per column across all features — impute carefully
- Cabin format: `Deck/Number/Side` — parse into 3 features (Deck: A-G+T, Side: P/S)
- **CryoSleep is the strongest signal**: cryo passengers have ~98% zero spending; creates near-perfect indicator
- PassengerId: GGGG_PP format encodes travel group membership — group size is a useful feature
- Spending features (RoomService, FoodCourt, ShoppingMall, Spa, VRDeck): 61-64% zeros

## Feature engineering priorities (ranked)
1. **Cabin parsing**: CabinDeck, CabinNum, CabinSide — especially Deck and Side
2. **CryoSleep × spending**: `is_cryo_but_spending` flag (anomaly indicator)
3. **Total spend**: sum of all 5 amenity columns; log1p transform
4. **Group features**: group_size from PassengerId[:4], group_has_child (any Age<18 in group)
5. **Spending log-transforms**: log1p for all 5 amenity features
6. **Age bins**: child (<13), teen (13-17), adult (18-60), senior (60+)
7. **HomePlanet × Destination** cross feature

## Known leakage vectors
- Do NOT use PassengerId or Name as features
- Group-level target encoding requires careful in-fold computation only

## Model notes
- LightGBM baseline established at CV=0.803
- Try XGBoost and CatBoost for diversity
- Neural network (TabNet or MLP) may add ensemble value given tabular structure
- Online LB top quartile: ~0.820+; top 10: ~0.830+

## CV-LB calibration
- sub_001: CV=0.8127, Online=0.79728, gap=-0.0154 (CV OVERESTIMATES by 1.5%)
- ROOT CAUSE IDENTIFIED: model_trainer.py fits fresh LabelEncoder on test — different int mappings than train
- FIX: save encoders from _load_data(), reuse on test with transform() + handle unseen as -1
- Also drop GroupId from features (high-cardinality string, adds noise, GroupSize already captures group info)
- sub_002 after fix: CV=0.8150, online=0.80102, gap=-0.0148 (still large)
- REMAINING ISSUE: test NaN filled with test.median() instead of train.median() — fix in model_trainer
- Gap may also reflect genuine distribution shift (test is harder)

## Submission cadence
- Max submissions/day: 10 (standard Kaggle getting-started competition)
- Spend slots only when CV improvement is meaningful (>0.003 delta)
