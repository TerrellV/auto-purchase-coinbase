# AutoPurchaseCoinbase

AWS Lambda Function used to make scheduled or recurring purchases through
Coinbase Pro. This lambda function is invoked by a scheduled CloudWatch Event.

## Build Notes
Desired zip file structure. `handler=func.main.event_handler`
```python
dependency_one/
dependency_two/
func
    main.py # event handler
    other.py
tests/
```
You must first include your requirements in the lambda_requirements.txt file.
Then install lambda dependencies into a designated folder
```bash
pip install -r lambda_requirements.txt -t dependencies
```
Combine content in dependencies and func folder in `lambda.zip` file
```bash
# PowerShell
Compress-Archive -Path func, dependencies/* -DestinationPath lambda.zip -F
```
