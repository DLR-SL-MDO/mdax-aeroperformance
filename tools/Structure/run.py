from lxml import etree
import math
from tools.util import write_value

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
    chord_length = float(tree.find("./airfoilWingParameters/chordLength").text)

    rho = float(tree.find("./aerodynamics/rho").text)
    velocity = float(tree.find("./aerodynamics/V").text)

    K_alpha = float(tree.find("./airfoilWingParameters/K_alpha").text)

    cl = float(tree.find("./aerodynamics/cl").text)
    cm_0 = float(tree.find("./airfoilWingParameters/cm_0").text)

    m = float(tree.find("./airfoilWingParameters/mass").text)
    g = float(tree.find("./airfoilWingParameters/gravityConstant").text)
    s = float(tree.find("./airfoilWingParameters/relDistElasticAxisToCenterOfGravity").text)
    eps = float(tree.find("./airfoilWingParameters/relDistQuarterPointElasticAxis").text)

    # =============================================
    # Compute lift and drag
    # =============================================
    S = span * chord_length
    q = 0.5 * rho * velocity ** 2.

    L = q * S * cl
    M0 = q * S * chord_length * cm_0

    alpha_elastic = 1. / K_alpha * (m * g * s * chord_length + L * eps * chord_length + M0)
    alpha_elastic *= 180.0 / math.pi

    # =============================================
    # Write variables
    # =============================================
    write_value("alpha_elastic", "./aerodynamics", alpha_elastic, tree)

    # =============================================
    # Write output file
    # =============================================
    etree.ElementTree(tree.getroot()).write(OUT_FILE, pretty_print=True)


if __name__ == "__main__":
    main()
