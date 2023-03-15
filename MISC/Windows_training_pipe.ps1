
# Set path to virtual environment
$base_venv = Get-Content -Path ".\project_config.json" | ConvertFrom-Json  
$base_venv = $base_venv.venv_path

. "$base_venv\Scripts\Activate.ps1"


# config filling

python -m spacy init fill-config input/base_config.cfg input/config.cfg


python -m spacy debug data input/config.cfg

python -m spacy train input/config.cfg --output ./Model