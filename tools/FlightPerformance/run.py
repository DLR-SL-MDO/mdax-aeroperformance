from lxml import etree
import math
from tools.util import write_value, write_node_path

IN_FILE = "./ToolInput/toolInput.xml"
OUT_FILE = "./ToolOutput/toolOutput.xml"


def main():
    # =============================================
    # Get input data
    # =============================================
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(IN_FILE, parser)

    # =============================================
    # Get variables
    # =============================================
    m = float(tree.find("./airfoilWingParameters/mass").text)
    fuel_fraction = float(tree.find("./airfoilWingParameters/fuelFraction").text)
    sfc = float(tree.find("./airfoilWingParameters/specificFuelConsumption").text)
    g = float(tree.find("./airfoilWingParameters/gravityConstant").text)

    cl = float(tree.find("./aerodynamics/cl").text)
    cd = float(tree.find("./aerodynamics/cd").text)

    V = float(tree.find("./aerodynamics/V").text)

    # =============================================
    # Compute lift and drag
    # =============================================
    m0 = m
    m1 = (1 - fuel_fraction) * m
    LD = cl / cd
    R = V * LD / sfc / g * math.log(m0 / m1)

    # =============================================
    # Write variables
    # =============================================
    write_node_path(["mission"], tree)
    write_value("range", "./mission", R, tree)

    # =============================================
    # Write output file
    # =============================================
    etree.ElementTree(tree.getroot()).write(OUT_FILE, pretty_print=True)


if __name__ == "__main__":
    main()
