import entities
import initial_access  # Importamos la clase `Cell` de `initial_access`
import rrc

def main():
    # Create the base station (gNB)
    gnb = entities.gNB()
    
    # Create a UE with supported PLMN IDs
    ue = entities.UE(supported_plmn_ids=["310260", "40006"])
    
    # Add cells to gNB
    gnb.add_cell(initial_access.Cell(cell_id=1, plmn_id="310260", signal_strength=75, frequency=2100, cell_type="Macro"))
    gnb.add_cell(initial_access.Cell(cell_id=2, plmn_id="310260", signal_strength=85, frequency=2600, cell_type="Small"))
    gnb.add_cell(initial_access.Cell(cell_id=3, plmn_id="310560", signal_strength=50, frequency=1800, cell_type="Macro"))

    # UE searches for available cells
    available_cells = ue.search_cells(gnb.cells)
    
    # UE selects the best cell based on signal strength
    best_cell = ue.select_cell(available_cells)
    if not best_cell:
        print("No suitable cell found, aborting RRC setup.")
        return
    
    # Initialize RRC handler
    rrc_handler = rrc.RRC()
    
    # Simulate the RRC connection request
    rrc_request = rrc_handler.rrc_connection_request(ue)
    
    # Simulate the RRC connection setup process by gNB
    rrc_response = rrc_handler.rrc_connection_setup(gnb, ue)
    
    # Complete the RRC connection setup process
    rrc_handler.rrc_connection_setup_complete(ue)

if __name__ == "__main__":
    main()
