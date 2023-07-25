# coding: utf-8
#!/bin/bash

# Get the directory of the setup.sh script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Install required tools
echo "Installing required tools..."
apt-get update
apt-get install -y aircrack-ng crunch xterm reaver pixiewps bully wifite macchanger

# Install wordlists
echo "Downloading wordlists..."
mkdir -p /usr/share/wordlists
cd /usr/share/wordlists
wget https://github.com/danielmiessler/SecLists/archive/master.zip
unzip master.zip
rm master.zip
mv SecLists-master/* .
rm -r SecLists-master

# Create the airhunt command
cat <<EOT >> /usr/local/bin/airhunt
#!/bin/bash

python "$DIR/airhunt.py" "\$@"
EOT

# Make the airhunt script executable
chmod +x /usr/local/bin/airhunt

# Set environment variable
echo "export AIRHUNT=$DIR/airhunt.py" >> ~/.bashrc

echo "Setup complete. You can now use 'airhunt' command to run the AirHunt tool."
