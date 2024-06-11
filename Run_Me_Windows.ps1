# Run docker-compose up -d command
echo "Running docker-compose\n"
docker-compose up -d

# Run the Main.py file using Python
echo "Executing Main.py"
python .\Main\Main.py
echo "Completed"
Start-Sleep -Seconds 2