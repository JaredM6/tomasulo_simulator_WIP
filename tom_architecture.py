class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.busy = None
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.destination = None
        # Just entered issue stage
        self.just_issued = False
        # In the middle of issuing or waiting to issue
        self.issuing = False
        self.just_start_execute = False
        self.executing = False
        self.execution_done = False
        self.writing_back = False
        self.remaining_cycles = None


class FunctionalUnit:
    def __init__(self, name, reservation_station):
        self.name = name
        self.rs = reservation_station
        self.busy = False
        self.execution_time = None
        self.time_to_completion = None
        self.instruction_tag = None

    def clear_functional_unit(self, name):
        self.busy = False
        self.execution_time = None
        self.time_to_completion = None
        self.instruction_tag = None
        self.rs = ReservationStation(name)


class Pipeline:
    def __init__(self, processor):
        self.fu_list = [processor.add_fu1, processor.add_fu2, processor.sub_fu1, processor.sub_fu2,
                        processor.mul_fu1, processor.mul_fu2, processor.int_fu1]
        self.issue = False
        self.execute = False
        self.write_back = False

    def check_issue_stage(self):
        for fu in self.fu_list:
            if (fu.rs.just_issued is True) or (fu.rs.issuing is True):
                # Found an instruction in the issue stage, can't leave
                return True
        return False

    def check_execute_stage(self):
        for fu in self.fu_list:
            if (fu.rs.just_start_execute is True) or (fu.rs.executing is True):
                # Found an instruction in the execute stage, can't leave
                return True
        return False

    def check_wb_stage(self):
        for fu in self.fu_list:
            if fu.rs.writing_back is True:
                # Found an instruction in the write-back stage, can't leave
                return True
        return False

    def check_empty(self):
        self.issue = self.check_issue_stage()
        self.execute = self.check_execute_stage()
        self.write_back = self.check_wb_stage()
        if (self.issue is False) and (self.execute is False) and (self.write_back is False):
            return True


class TomasuloProcessor:
    def __init__(self):
        # Functional Units
        self.add_rs1 = ReservationStation("add_rs1")
        self.add_rs2 = ReservationStation("add_rs2")
        self.sub_rs1 = ReservationStation("sub_rs1")
        self.sub_rs2 = ReservationStation("sub_rs2")
        self.mul_rs1 = ReservationStation("mul_rs1")
        self.mul_rs2 = ReservationStation("mul_rs2")
        self.int_rs1 = ReservationStation("int_rs1")

        self.add_fu1 = FunctionalUnit("add_fu1", self.add_rs1)
        self.add_fu2 = FunctionalUnit("add_fu2", self.add_rs2)
        self.sub_fu1 = FunctionalUnit("sub_fu1", self.sub_rs1)
        self.sub_fu2 = FunctionalUnit("sub_fu2", self.sub_rs2)
        self.mul_fu1 = FunctionalUnit("mul_fu1", self.mul_rs1)
        self.mul_fu2 = FunctionalUnit("mul_fu2", self.mul_rs2)
        self.int_fu1 = FunctionalUnit("int_fu1", self.int_rs1)

        self.execution_list = []
        self.cdb_value = 0
        self.registers = []

    # Returns the name of the reservation station handling the calculation
    # Example: ADD R1, R2, R3
    # TODO: Add the flag setting for other RS like in 'add_rs1' when multiple instructions of the same kind get issued
    def issue(self, op, vj, vk, destination):
        # Check for available reservation stations and issue instruction accordingly
        if op == "ADD":
            if not self.add_rs1.busy:
                self.add_rs1.busy = True
                self.add_rs1.op = op
                self.add_rs1.vj = vj
                self.add_rs1.vk = vk
                self.add_rs1.destination = destination
                self.add_rs1.just_issued = True
                self.add_rs1.issuing = True
                return self.add_rs1.name
            elif not self.add_rs2.busy:
                self.add_rs2.busy = True
                self.add_rs2.op = op
                self.add_rs2.vj = vj
                self.add_rs2.vk = vk
                self.add_rs2.destination = destination
                self.add_rs2.just_issued = True
                self.add_rs2.issuing = True
                return self.add_rs2.name
            else:
                return "all_busy"
        if op == "SUB":
            if not self.sub_rs1.busy:
                self.sub_rs1.busy = True
                self.sub_rs1.op = op
                self.sub_rs1.vj = vj
                self.sub_rs1.vk = vk
                self.sub_rs1.destination = destination
                self.sub_rs1.just_issued = True
                self.sub_rs1.issuing = True
                return self.sub_rs1.name
            elif not self.sub_rs2.busy:
                self.sub_rs2.busy = True
                self.sub_rs2.op = op
                self.sub_rs2.vj = vj
                self.sub_rs2.vk = vk
                self.sub_rs2.destination = destination
                self.sub_rs2.just_issued = True
                self.sub_rs2.issuing = True
                return self.sub_rs2.name
            else:
                return "all_busy"
        elif op == "MUL":
            if not self.mul_rs1.busy:
                self.mul_rs1.busy = True
                self.mul_rs1.op = op
                self.mul_rs1.vj = vj
                self.mul_rs1.vk = vk
                self.mul_rs1.destination = destination
                self.mul_rs1.just_issued = True
                self.mul_rs1.issuing = True
                return self.mul_rs1.name
            elif not self.mul_rs2.busy:
                self.mul_rs2.busy = True
                self.mul_rs2.op = op
                self.mul_rs2.vj = vj
                self.mul_rs2.vk = vk
                self.mul_rs2.destination = destination
                self.mul_rs2.just_issued = True
                self.mul_rs2.issuing = True
                return self.mul_rs2.name
            else:
                return "all_busy"
        elif op == "INT":
            if not self.int_rs1.busy:
                self.int_rs1.busy = True
                self.int_rs1.op = op
                self.int_rs1.vj = vj
                self.int_rs1.vk = vk
                self.int_rs1.destination = destination
                self.int_rs1.just_issued = True
                self.int_rs1.issuing = True
                return self.int_rs1.name
            else:
                return "all_busy"
        # Error case
        return None

    def execute(self, op):
        # Check for available functional units and execute accordingly
        if op == "ADD" and not self.add_fu1.busy:
            # Execute ADD operation using Functional Unit 1
            self.add_fu1.busy = True
            self.add_fu1.execution_time = 4  # 4 cycles for ADD
            self.execution_list.append(self.add_rs1.name)
            self.add_rs1.issuing = False
            self.add_rs1.just_start_execute = True
            self.add_rs1.executing = True
            return self.add_fu1
        elif op == "ADD" and not self.add_fu2.busy:
            # Execute ADD operation using Functional Unit 2
            self.add_fu2.busy = True
            self.add_fu2.execution_time = 4  # 4 cycles for ADD
            self.execution_list.append(self.add_rs2.name)
            self.add_rs2.issuing = False
            self.add_rs2.just_start_execute = True
            self.add_rs2.executing = True
            return self.add_fu2
        if op == "SUB" and not self.sub_fu1.busy:
            # Execute SUB operation using Functional Unit 1
            self.sub_fu1.busy = True
            self.sub_fu1.execution_time = 4  # 4 cycles for SUB
            self.execution_list.append(self.sub_rs1.name)
            self.sub_rs1.issuing = False
            self.sub_rs1.just_start_execute = True
            self.sub_rs1.executing = True
            return self.sub_fu1
        elif op == "SUB" and not self.sub_fu2.busy:
            # Execute SUB operation using Functional Unit 2
            self.sub_fu2.busy = True
            self.sub_fu2.execution_time = 4  # 4 cycles for SUB
            self.execution_list.append(self.sub_rs2.name)
            self.sub_rs2.issuing = False
            self.sub_rs2.just_start_execute = True
            self.sub_rs2.executing = True
            return self.sub_fu2
        elif op == "MUL" and not self.mul_fu1.busy:
            # Execute MUL operation using Functional Unit 1
            self.mul_fu1.busy = True
            self.mul_fu1.execution_time = 8  # 8 cycles for MUL
            self.execution_list.append(self.mul_rs1.name)
            self.mul_rs1.issuing = False
            self.mul_rs1.just_start_execute = True
            self.mul_rs1.executing = True
            return self.mul_fu1
        elif op == "MUL" and not self.mul_fu2.busy:
            # Execute MUL operation using Functional Unit 2
            self.mul_fu2.busy = True
            self.mul_fu2.execution_time = 8  # 8 cycles for MUL
            self.execution_list.append(self.mul_rs2.name)
            self.mul_rs2.issuing = False
            self.mul_rs2.just_start_execute = True
            self.mul_rs2.executing = True
            return self.mul_fu2
        elif op == "INT" and not self.int_fu1.busy:
            # Execute int operation using Integer Functional Unit
            self.int_fu1.busy = True
            self.int_fu1.execution_time = 1  # 1 cycle for int
            self.execution_list.append(self.int_rs1.name)
            self.int_rs1.issuing = False
            self.int_rs1.just_start_execute = True
            self.int_rs1.executing = True
            return self.int_fu1
        else:
            return None

    def write_back(self, regs_used, fu):
        operand1, operand2, destination, operator, old_value, result = None, None, None, None, None, None

        # Read the register contents and find the registers needed for the calculation
        with open("register_contents_final.txt", 'r') as file:
            self.registers = file.readlines()
        with open("register_contents_final.txt", 'r') as file:
            filedata = file.read()

        # 'regs_used' comes as a string like "R1,R2" or "R1,1"
        operand1, operand2 = regs_used.split(",")

        # Get the actual values of the registers before writing
        for register in self.registers:
            reg_name, value = register.split()
            # Source register
            if (str(operand1).startswith("R")) and (str(operand1) == reg_name):
                operand1 = value
            # Source register, right in
            elif (str(operand2).startswith("R")) and (str(operand2) == reg_name):
                operand2 = value
            # Destination register found
            elif fu.rs.destination == reg_name:
                destination = reg_name
                old_value = value

        # Calculate result
        operand1 = int(operand1)
        operand2 = int(operand2)
        if fu.rs.op == "ADD":
            result = operand1 + operand2
        elif fu.rs.op == 'SUB':
            result = operand1 - operand2
        elif fu.rs.op == "MUL":
            result = operand1 * operand2
        elif fu.rs.op == "DIV":
            result = operand1 / operand2
        else:
            # TODO: Load, store, branch
            exit(-1)

        # Update the file
        filedata = filedata.replace(f"{destination} {old_value}", f"{destination} {result}")
        with open("register_contents_final.txt", 'w') as file2:
            file2.write(filedata)

        # Set flag and return
        fu.rs.writing_back = True
        return result

