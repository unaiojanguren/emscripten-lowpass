from initial_access import Cell  # Importamos la clase `Cell` correctamente

class UE:
    def __init__(self, supported_plmn_ids, identity):
        self.supported_plmn_ids = supported_plmn_ids
        self.state = "Idle"
        self.selected_cell = None
        self.rm_state = "RM-DEGISTERED"
        self.identity = identity

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
    
    def register(self,amf):
        print(f"UE: Sending REGISTRATION REQUEST to AMF with identity: {self.identity}")
        if amf.receive_registration_request(self.identity):
            self.state="RM-REGISTERED"
        else:
            print(f"UE: with identity: {self.identity} not authenticated")



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


class Core:
    def __init__(self):
        self.amf = AMF()

class AMF:
    def __init__(self):
        self.ausf = AUSF()
        self.udm = UDM()

    def receive_registration_request(self, ue_identity):
        print(f"AMF: Received REGISTRATION REQUEST from UE with identity: {ue_identity}")
        return self.authenticate(ue_identity)


    def authenticate(self, ue_identity):
        print(f"AMF: Initiating authentication with AUSF...")
        auth_data = self.ausf.authenticate(ue_identity,self.udm)
        if auth_data["authenticated"]:
            print(f"AMF: Authentication successful for UE: {ue_identity}")
            print("AMF: Sending SECURITY MODE COMMAND...")
            print("UE: SECURITY MODE COMPLETE received.")
            print("AMF: Requesting PEI from UE...")
            print("UE: Sending IDENTITY RESPONSE with PEI.")
            print("AMF: Checking PEI with 5G-EIR... (skipped)")

            print("AMF: Registering with UDM...")
            self.udm.register_ue(ue_identity)
            print("AMF: Getting subscription data from UDM...")
            self.udm.get_subscription_data(ue_identity)

            print("AMF: Sending REGISTRATION ACCEPT to UE...")
            print("UE: REGISTRATION COMPLETE sent.")
            return True
        else:
            print(f"AMF: Authentication failed for UE: {ue_identity}")
            return False



class AUSF:
    def authenticate(self, ue_identity,udm):
        print(f"AUSF: Authenticating UE identity: {ue_identity}")
        return {"authenticated": udm.authenticate(ue_identity), "algorithm": "5G-AKA"}

class UDM:

    def __init__(self):
        self.subscriber_data = {"imsi-001010123456789","imsi-001310123456789"}

    def authenticate(self, ue_identity):
        print(f"UDM: Authenticating UE {ue_identity}")
        if ue_identity in self.subscriber_data:
            return True
        else:
            return False

    def register_ue(self, ue_identity):
        print(f"UDM: UE registered: {ue_identity}")
    

    def get_subscription_data(self, ue_identity):
        print(f"UDM: Subscription data retrieved for UE: {ue_identity}")



