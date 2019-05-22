#  Where is the team having lunch today? Let's vote - majority rules

## Usage

`startballot` script expects menu options JSON on its stdin.
Run `./startballot < <(wget -qO- http://manger_url/todays_menus)` to bootstrap ballot with todays' menus from manger.
for testing run `./startballot < mock_menu_file.txt`
