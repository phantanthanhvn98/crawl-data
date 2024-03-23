def parse_gtin(gtin):
    gtin = gtin.split("gtin")[1]
    gtin = gtin.split(":")[1]
    gtin = gtin.split("\\")[1].replace("\"", "")
    return gtin
