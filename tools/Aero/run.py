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
    alpha_stiff = float(tree.find("./aerodynamics/alpha_stiff").text)
    alpha_elastic = float(tree.find("./aerodynamics/alpha_elastic").text)
    alpha = alpha_stiff + alpha_elastic

    span = float(tree.find("./airfoilWingParameters/span").text)
    l = float(tree.find("./airfoilWingParameters/chordLength").text)
    S = span * l
    AR = span / S ** 2.
    e = 0.7

    dcl_dalpha_airfoil = float(tree.find("./airfoilWingParameters/dcl_dalpha_airfoil").text)
    alpha_0_airfoil = float(tree.find("./airfoilWingParameters/alpha_0_airfoil").text)
    cd_0 = float(tree.find("./airfoilWingParameters/cd_0").text)

    # =============================================
    # Compute lift and drag
    # =============================================
    cl = dcl_dalpha_airfoil * (alpha - alpha_0_airfoil) * math.pi / 180.
    cd = cd_0 + cl ** 2. / math.pi / AR / e

    # =============================================
    # Write variables
    # =============================================
    write_value("cl", "./aerodynamics", cl, tree)
    write_value("cd", "./aerodynamics", cd, tree)

    # =============================================
    # Write output file
    # =============================================
    etree.ElementTree(tree.getroot()).write(OUT_FILE, pretty_print=True)


if __name__ == "__main__":
    main()
