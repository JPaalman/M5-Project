# use chmod +x path_to_this_file to make it executable
if [ ! -d "M5-Project" ]; then
git clone https://github.com/JPaalman/M5-Project.git
else
( cd M5-Project ; git pull )
fi
python3 M5-Project/Game.py
