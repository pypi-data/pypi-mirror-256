from fastkml import kml

bads = None
goods = None

with open("good_m104_bond_2019-08-28-14_41_38.kml", 'rt', encoding="utf-8") as badf:
    bads = badf.read()
with open("good_m104_bond_2019-08-28-14_41_38.kml", 'rt', encoding="utf-8") as goodf:
    goods = goodf.read()

bad = kml.KML()
good = kml.KML()

bad.from_string(bads.encode('utf8'))
good.from_string(goods.encode('utf8'))

print('foo')