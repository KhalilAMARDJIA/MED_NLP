#!/bin/bash


# See who to handel first connection to doccano init and createuser
# # Initialize database.
# doccano init
# # Create a super user.
# doccano createuser --username admin --password pass

doccano init
doccano createuser --username admin --password pass

# need to parse project_config.json to get the base_venv path such as powershell
VENV_PATH=".OPHT_SPACY/bin/activate"
PYTHON_VERSION=$(python --version | awk '{print $2}' | cut -d. -f1,2)
BACKEND_PATH=".OPHT_SPACY/lib/python$PYTHON_VERSION/site-packages/backend"

# activate virtual environment
source $VENV_PATH

# navigate to the backend directory
cd $BACKEND_PATH

# start the doccano webserver on an available port
for port in {8000..9000}; do
    (echo >/dev/tcp/localhost/$port) &>/dev/null
    if [ $? -ne 0 ]; then
        break
    fi
done
echo "Starting server with port $port."
doccano webserver --port $port &

# start the doccano task in a separate terminal window
gnome-terminal -e "bash -c \"source /path/to/venv/bin/activate; cd /path/to/backend; doccano task\""

# wait for the webserver to start
sleep 5

# open the website in the default browser
xdg-open "http://localhost:$port/"
