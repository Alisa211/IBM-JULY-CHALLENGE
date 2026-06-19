Write-Host "Running Workflow Evaluations..."
.\venv\Scripts\pytest tests\evaluation\test_workflow_eval.py -v
Write-Host "Evaluations Complete."

