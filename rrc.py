class RRC:
    def __init__(self):
        self.state = "Idle"
    
    def rrc_connection_request(self, ue):
        """ Simulate UE sending RRC connection request to gNB with data """
        request_data = ue.rrc_connection_request()
        print(f"UE: Sending RRC connection request to gNB with the following data:")
        print(f"    PLMN ID: {request_data['plmn_id']}, Cell ID: {request_data['cell_id']}, Signal Strength: {request_data['signal_strength']} dBm, Frequency: {request_data['frequency']} Hz")
        return request_data
    
    def rrc_connection_setup(self, gnb, ue):
        """ Simulate gNB sending RRC connection setup to UE with additional data """
        setup_data = gnb.process_rrc_connection_request(ue)
        print(f"gNB: Sending RRC connection setup with configuration:")
        print(f"    PLMN ID: {setup_data['plmn_id']}, Cell ID: {setup_data['cell_id']}, Signal Strength: {setup_data['signal_strength']} dBm, Frequency: {setup_data['frequency']} Hz")
        print(f"    Network Configuration: {setup_data['network_configuration']}")
        return setup_data

    def rrc_connection_setup_complete(self, ue):
        """ Simulate UE completing the RRC connection setup """
        print(f"UE: RRC connection setup complete. Configuration is confirmed and the UE is now connected.")
        return "RRC Connection Setup Complete"
