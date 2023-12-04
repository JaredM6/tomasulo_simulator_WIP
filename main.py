import os
import tom_architecture
import tom_simulator

if __name__ == "__main__":
    # Some file management before starting
    if os.path.exists("simulation_log.txt") and os.path.exists("register_contents_final.txt"):
        os.remove("simulation_log.txt")
        os.remove("register_contents_final.txt")
    with open("register_contents_initial.txt", 'r') as file:
        register_init = file.read()
    with open("register_contents_final.txt", 'w') as file2:
        file2.write(register_init)
    # Setup and start
    processor = tom_architecture.TomasuloProcessor()
    simulator = tom_simulator.TomasuloSimulator()
    simulator.run_simulation()

