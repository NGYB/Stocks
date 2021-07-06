# Stock Returns Prediction
Programs for stock **returns** prediction. 
Here we aim to do predictions with a forecast horizon of 21 days.
The results have been compiled into blog posts [here](https://medium.com/ai-trading-labs/forecasting-stock-prices-using-xgboost-part-3-3-c7b13d7a84df).

* **StockReturnsPrediction_v1_SExpSmoothing.ipynb**:
	* Predict stock returns using single exponential smoothing
	* Using 3 years of data for training and 1 year of data for validation
* **StockReturnsPrediction_v2_DExpSmoothing.ipynb**:
	* Predict stock returns using double exponential smoothing
	* Using 3 years of data for training and 1 year of data for validation
* **StockReturnsPrediction_v3_xgboost.ipynb**:
	* Predict stock returns using XGBoost
	* Using 3 years of data for training and 1 year of data for validation
	* Includes hyperparameter tuning on validation set
	* Includes date features
* **StockReturnsPrediction_v4_xgboost.ipynb**:
	* Predict stock returns using XGBoost
	* Using 3 years of data for training and 1 year of data for validation
	* Includes hyperparameter tuning on validation set
	* Without date features
* **StockReturnsPrediction_v5_xgboost.ipynb**:
	* Predict stock returns using XGBoost
	* Using 3 years of data for training and 1 year of data for validation
	* Includes hyperparameter tuning on validation set
	* Without date features
	* Includes technical indicators as features
  
