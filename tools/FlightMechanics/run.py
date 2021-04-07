from lxml import etree
import math
from util import write_value

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
    span = float(tree.find("./airfoilWingParameters/span").text)
    l = float(tree.find("./airfoilWingParameters/chordLength").text)
    S = span * l

    m = float(tree.find("./airfoilWingParameters/mass").text)
    dcl_dalpha_airfoil = float(tree.find("./airfoilWingParameters/dcl_dalpha_airfoil").text)

    alpha_0_airfoil = float(tree.find("./airfoilWingParameters/alpha_0_airfoil").text)

    rho = float(tree.find("./aerodynamics/rho").text)
    V = float(tree.find("./aerodynamics/V").text)
    q = 0.5 * rho * V ** 2.
    g = float(tree.find("./airfoilWingParameters/gravityConstant").text)

    alpha_elastic = float(tree.find("./aerodynamics/alpha_elastic").text)

    # =============================================
    # Compute angle of attack
    # =============================================
    alpha_stiff = m * g * 180. / math.pi / q / S / dcl_dalpha_airfoil + alpha_0_airfoil - alpha_elastic

    # =============================================
    # Write variables
    # =============================================
    write_value("alpha_stiff", "./aerodynamics", alpha_stiff, tree)

    # =============================================
    # Write output file
    # =============================================
    etree.ElementTree(tree.getroot()).write(OUT_FILE, pretty_print=True)


if __name__ == "__main__":
    main()

