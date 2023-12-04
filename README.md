# tomasulo_simulator_WIP
Tomasulo simulator without ROB [Early WIP]

Features:
- Handles ADD
- Handles MUL
- Handles SUB
- Avoids structural hazards
- Creates a log file that details the process

Improvements:
- Add Divide functionality (easy, but tedious)
- Add Load and Store capability
- Add register renaming to avoid WAR and WAW and general Tomasulo function
- Add branch control
- Add floating point support
- Write back and issue are assumed one cycle each, modify to allow for robust delays
- Possible GUI to click through cycles
