# Stock Price Prediction
Programs for stock price prediction

* StockPricePrediction_v1_xgboost.ipynb:
	* Predict stock price in next day using XGBoost
        * Given prices and other features for the last N days, we do prediction for day N+1
	* Here we split 3 years of data into train(60%), dev(20%) and test(20%)
	* Doesn't work well, likely because data is not normalized
* StockPricePrediction_v1a_xgboost.ipynb:
        * Predict stock price in next day using XGBoost
        * Given prices and other features for the last N days, we do prediction for day N+1
        * Here we split 3 years of data into train(60%), dev(20%) and test(20%)
        * Here we scale the train set to have mean 0 and variance 1, and apply the same transformation to dev and test sets
        * Doesn't work well, likely because the model was trained on prices below ~1.7 and so when it saw prices above 1.7 for the dev set, it could not generalize well
* StockPricePrediction_v1b_xgboost.ipynb:
        * Predict stock price in next day using XGBoost
        * Given prices and other features for the last N days, we do prediction for day N+1
        * Here we split 3 years of data into train(60%), dev(20%) and test(20%)
        * Here for the past N values for the dev set, we scale them to have mean 0 and variance 1, and do prediction on them
        * Doesn't work well, likely because the model was trained on prices below ~1.7 and so when it saw prices above 1.7 for the dev set, it could not generalize well
* StockPricePrediction_v1c_xgboost.ipynb:
        * Predict stock price in next day using XGBoost
        * Given prices and other features for the last N days, we do prediction for day N+1
        * Here we split 3 years of data into train(60%), dev(20%) and test(20%)
        * Whenever we do prediction on dev or test set we scale the previous N values to also have mean 0 and var 1
        * On the test set, the RMSE is 1.162 and MAPE is 0.58% after hyperparamter tuning and using N_opt=3
* StockPricePrediction_v2_lin_reg.ipynb:
	* Predict stock price in next day using linear regression
	* Given prices for the last N days, we train a model, and predict for day N+1
        * On the test set, the RMSE is 1.42 and MAPE is 0.707% using N_opt=5
* StockPricePrediction_v3_mov_avg.ipynb:
    * Predict stock price in next day using simple moving average
    * Given prices for the last N days, we do prediction for day N+1

<img src="./data/vti_predictions_xgboost.png">
