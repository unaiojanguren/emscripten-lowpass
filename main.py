import entities
import initial_access

def turnON(ue,gnb_cells):
    scanned_cells = ue.search_cells(gnb_cells)
    return ue.select_cell(scanned_cells)

def main():
    gnb = entities.gNB()
    ue = entities.UE(supported_plmn_ids=["310260","40006"])

    gnb.add_cell(initial_access.Cell(cell_id=1, signal_strength=initial_access.random.randint(60, 100), plmn_id="310260"))
    gnb.add_cell(initial_access.Cell(cell_id=2, signal_strength=initial_access.random.randint(60, 100), plmn_id="310260"))
    gnb.add_cell(initial_access.Cell(cell_id=3, signal_strength=initial_access.random.randint(60, 100), plmn_id="310560"))

    #Turn on UE
    cell = turnON(ue,gnb.cells)
    
    #RACH
    ue.rach_procedure(cell)
    


if __name__  == "__main__":
    main()