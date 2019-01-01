# Stock Price Prediction
Programs for stock price prediction

* StockPricePrediction_v1_xgboost.ipynb:
	* Predict stock price in next day using XGBoost
	* Here we split 3 years of data into train(60%), dev(20%) and test(20%)
* StockPricePrediction_v2_lin_reg.ipynb:
	* Predict stock price in next day using linear regression
	* Given prices for the last N days, we train a model, and predict for day N+1
* StockPricePrediction_v3_mov_avg.ipynb:
    * Predict stock price in next day using simple moving average
    * Given prices for the last N days, we do prediction for day N+1
