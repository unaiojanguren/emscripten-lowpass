

class gNB:
    def __init__(self):
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)
    
    def send_mib_and_sib(self):
        for cell in self.cells:
            mib = cell.send_mib()
            sib = cell.send_sib()


class UE:
   
    def __init__(self, supported_plmn_ids):
        self.supported_plmn_ids = supported_plmn_ids

    def search_cells(self, available_cells):
        print("UE is searching for available cells...")
        return available_cells
    
    def select_cell(self, cells):
        valid_cells = []

        for cell in cells:
            mib = cell.send_mib()
            sib = cell.send_sib()
            if mib["plmn_id"] in self.supported_plmn_ids and not sib["cell_barred"]:
                valid_cells.append((cell, mib, sib))
        
        if not valid_cells:
            print("No suitable cell found. Search failed.")
            return None
        
        best_cell, best_mib, best_sib = max(valid_cells, key=lambda x: x[0].signal_strength)

        print(f"Selected Cell ID: {best_cell.cell_id}, Signal Strength: {best_cell.signal_strength}, PLMN ID: {best_cell.plmn_id}")
        return best_cell
    
    def rach_procedure(self, cell):
        
        if cell is None:
            print("No cell selected, aborting RACH procedure.")
            return

        rach_response = cell.send_rach(self)

        if rach_response == True:
            print("RACH procedure successful")
        else:
            print("RACH procedure failed. UE needs to try again.")
    
    
