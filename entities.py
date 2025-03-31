from initial_access import Cell  # Importamos la clase `Cell` correctamente

class UE:
    def __init__(self, supported_plmn_ids):
        self.supported_plmn_ids = supported_plmn_ids
        self.state = "Idle"
        self.selected_cell = None

    def search_cells(self, available_cells):
        """Simulate the UE searching for available cells"""
        print("UE: Searching for available cells...")
        return available_cells
    
    def select_cell(self, cells):
        """Select the best cell based on signal strength"""
        valid_cells = []

        for cell in cells:
            mib = cell.send_mib()
            sib = cell.send_sib()
            if mib["plmn_id"] in self.supported_plmn_ids and not sib["cell_barred"]:
                valid_cells.append((cell, mib, sib))
        
        if not valid_cells:
            print("No suitable cell found. Search failed.")
            return None
        
        # Choose the best cell based on signal strength
        best_cell, best_mib, best_sib = max(valid_cells, key=lambda x: x[0].signal_strength)
        self.selected_cell = best_cell
        print(f"UE: Selected Cell ID: {best_cell.cell_id}, Signal Strength: {best_cell.signal_strength}, Frequency: {best_cell.frequency}, PLMN ID: {best_cell.plmn_id}, Cell Type: {best_sib['cell_type']}")
        return best_cell
    
    def rrc_connection_request(self):
        """Simulate UE sending RRC connection request with additional details"""
        print(f"UE: Sending RRC connection request to gNB...")
        request_data = {
            "plmn_id": self.selected_cell.plmn_id,
            "cell_id": self.selected_cell.cell_id,
            "signal_strength": self.selected_cell.signal_strength,
            "frequency": self.selected_cell.frequency
        }
        self.state = "RRC Connection Request Sent"
        return request_data
    
    def rrc_connection_setup_complete(self):
        """Simulate UE completing the RRC connection setup"""
        print(f"UE: Received RRC connection setup response and completed setup.")
        self.state = "RRC Connected"
        return "RRC Connection Setup Complete"


class gNB:
    def __init__(self):
        self.cells = []
        self.state = "Idle"

    def add_cell(self, cell):
        """Add a cell to the gNB"""
        self.cells.append(cell)
    
    def process_rrc_connection_request(self, ue):
        """Simulate gNB receiving the RRC connection request and sending setup"""
        print(f"gNB: Processing RRC connection request from UE with selected cell ID: {ue.selected_cell.cell_id}...")
        setup_data = {
            "plmn_id": ue.selected_cell.plmn_id,
            "cell_id": ue.selected_cell.cell_id,
            "signal_strength": ue.selected_cell.signal_strength,
            "frequency": ue.selected_cell.frequency,
            "network_configuration": "Configured for high-speed data"
        }
        self.state = "RRC Connection Setup Sent"
        return setup_data
    
    def rrc_connection_setup_complete(self, ue):
        """Simulate gNB completing the RRC connection setup"""
        print(f"gNB: Sending RRC connection setup to UE with configuration: {ue.selected_cell.frequency} Hz")
        ue.rrc_connection_setup_complete()
