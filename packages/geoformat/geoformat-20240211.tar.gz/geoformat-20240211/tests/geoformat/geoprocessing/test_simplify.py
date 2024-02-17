from tests.utils.tests_utils import test_function

from tests.data.geometries import (
    POINT_paris_3857,
    MULTIPOINT_paris_tokyo_3857,
    LINESTRING_loire_3857,
    MULTILINESTRING_loire_katsuragawa_river_3857,
    POLYGON_france_3857,
    MULTIPOLYGON_france_japan_3857,
    GEOMETRYCOLLECTION_paris_tokyo_loire_katsuragawa_river_france_japan_3857,
)

from geoformat.geoprocessing.simplify import simplify

simplify_parameters = {
    0: {
        "geometry": LINESTRING_loire_3857,
        "tolerance": 5000,
        "algo": 'RDP',
        "return_value": {'type': 'LineString', 'coordinates': [[-237872.03, 5988382.54], [-174276.42, 5974318.13], [-145536.1, 5998777.98], [-37301.27, 6009173.42], [9172.44, 5977987.11], [48919.7, 5996943.49], [116184.28, 6010396.41], [149205.08, 6032410.27], [194455.8, 6079495.48], [218915.65, 6089890.92], [245209.99, 6084387.45], [295352.68, 6051978.15], [328984.97, 6018957.36], [317366.54, 5998166.48], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [426824.37, 5861802.83], [447615.24, 5848961.4], [448838.23, 5766409.41], [469017.61, 5738280.59], [465348.63, 5710151.76], [473298.08, 5695475.85], [461068.15, 5656951.59], [437066.93, 5651753.87], [435232.44, 5604821.54]]}
    },
    1: {
        "geometry": LINESTRING_loire_3857,
        "tolerance": 500000000,
        "algo": 'VW',
        "return_value": {'type': 'LineString', 'coordinates': [[-237872.03, 5988382.54], [-209743.21, 5987159.55], [-154097.05, 5986548.06], [-88055.46, 6004281.45], [-4891.97, 5983490.57], [48919.7, 5996943.49], [91724.43, 6009784.91], [149205.08, 6032410.27], [181002.88, 6060539.1], [245209.99, 6084387.45], [295352.68, 6051978.15], [328984.97, 6018957.36], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [409702.47, 5892377.64], [426824.37, 5861802.83], [451284.21, 5812271.63], [452507.21, 5782919.81], [465348.63, 5710151.76], [461068.15, 5656951.59], [435232.44, 5604821.54]]}
    },
    2: {
        "geometry": POLYGON_france_3857,
        "tolerance": 30000,
        "algo": 'RDP',
        "return_value": {'type': 'Polygon', 'coordinates': [[[273950.31, 6643295.0], [190786.82, 6599267.27], [190786.82, 6467184.09], [4891.97, 6364452.72], [39135.76, 6335100.9], [-122299.25, 6315533.03], [-141867.12, 6388912.57], [-200570.76, 6388912.57], [-151651.06, 6207909.69], [-513656.83, 6217693.63], [-528332.74, 6163881.96], [-469629.1, 6134530.14], [-513656.83, 6119854.23], [-484305.01, 6061150.59], [-450061.22, 6105178.32], [-313086.07, 6056258.63], [-136975.15, 5826336.04], [-73379.55, 5640441.19], [-127191.22, 5699144.83], [-127191.22, 5523033.92], [-195678.79, 5356706.94], [63595.61, 5258867.55], [73379.55, 5293111.33], [362005.77, 5214839.82], [327761.98, 5307787.24], [464737.13, 5390950.73], [665307.89, 5327355.12], [841418.81, 5420302.55], [748471.38, 5625765.28], [768039.26, 5836119.98], [684875.77, 5782308.32], [679983.8, 5860579.83], [841418.81, 6031798.78], [914798.35, 6271505.3], [635956.08, 6344884.84], [322870.01, 6555239.55], [273950.31, 6643295.0]]]}
    },
    3: {
        "geometry": POLYGON_france_3857,
        "tolerance": 3000000000,
        "algo": 'VW',
        "return_value": {'type': 'Polygon', 'coordinates': [[[273950.31, 6643295.0], [190786.82, 6599267.27], [190786.82, 6467184.09], [44027.73, 6408480.45], [39135.76, 6335100.9], [-122299.25, 6315533.03], [-151651.06, 6207909.69], [-288626.22, 6183449.84], [-337545.92, 6237261.51], [-513656.83, 6217693.63], [-469629.1, 6134530.14], [-313086.07, 6056258.63], [-225030.61, 5953527.26], [-136975.15, 5826336.04], [-127191.22, 5699144.83], [-127191.22, 5523033.92], [-195678.79, 5356706.94], [63595.61, 5258867.55], [210354.7, 5229515.73], [362005.77, 5214839.82], [327761.98, 5307787.24], [464737.13, 5390950.73], [547900.62, 5386058.76], [665307.89, 5327355.12], [719119.56, 5342031.03], [841418.81, 5420302.55], [782715.17, 5488790.13], [748471.38, 5625765.28], [777823.2, 5718712.71], [768039.26, 5836119.98], [684875.77, 5782308.32], [679983.8, 5860579.83], [758255.32, 5938851.35], [841418.81, 6031798.78], [851202.75, 6114962.26], [914798.35, 6271505.3], [748471.38, 6291073.18], [635956.08, 6344884.84], [513656.83, 6447616.21], [322870.01, 6555239.55], [273950.31, 6643295.0]]]}
    },
    4: {
        "geometry": MULTILINESTRING_loire_katsuragawa_river_3857,
        "tolerance": 5000,
        "algo": 'RDP',
        "return_value": {'type': 'MultiLineString', 'coordinates': [[[-237872.03, 5988382.54], [-174276.42, 5974318.13], [-145536.1, 5998777.98], [-37301.27, 6009173.42], [9172.44, 5977987.11], [48919.7, 5996943.49], [116184.28, 6010396.41], [149205.08, 6032410.27], [194455.8, 6079495.48], [218915.65, 6089890.92], [245209.99, 6084387.45], [295352.68, 6051978.15], [328984.97, 6018957.36], [317366.54, 5998166.48], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [426824.37, 5861802.83], [447615.24, 5848961.4], [448838.23, 5766409.41], [469017.61, 5738280.59], [465348.63, 5710151.76], [473298.08, 5695475.85], [461068.15, 5656951.59], [437066.93, 5651753.87], [435232.44, 5604821.54]], [[15075140.03, 4120873.07], [15110262.84, 4155919.45], [15082974.82, 4181449.41], [15099141.26, 4182901.72], [15114743.96, 4195962.89]]]}
    },
    5: {
        "geometry": MULTILINESTRING_loire_katsuragawa_river_3857,
        "tolerance": 50000000,
        "algo": 'VW',
        "return_value": {'type': 'MultiLineString', 'coordinates': [[[-237872.03, 5988382.54], [-209743.21, 5987159.55], [-198124.78, 5976152.62], [-174276.42, 5974318.13], [-154097.05, 5986548.06], [-145536.1, 5998777.98], [-119241.76, 6002446.96], [-104565.85, 6003669.95], [-88055.46, 6004281.45], [-78271.52, 6004281.45], [-66653.09, 6009173.42], [-52588.68, 6009173.42], [-37301.27, 6009173.42], [-23236.86, 5996331.99], [-4891.97, 5983490.57], [9172.44, 5977987.11], [18344.89, 5980433.09], [48919.7, 5996943.49], [67264.58, 6001223.96], [91724.43, 6009784.91], [116184.28, 6010396.41], [149205.08, 6032410.27], [155320.04, 6045863.19], [181002.88, 6060539.1], [182225.88, 6071546.03], [194455.8, 6079495.48], [204851.24, 6083775.96], [218915.65, 6089890.92], [245209.99, 6084387.45], [257439.91, 6077049.5], [295352.68, 6051978.15], [307582.6, 6038525.23], [328984.97, 6018957.36], [317366.54, 5998166.48], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [409702.47, 5892377.64], [412759.95, 5881982.2], [426824.37, 5861802.83], [447615.24, 5848961.4], [451284.21, 5812271.63], [452507.21, 5782919.81], [448838.23, 5766409.41], [457399.18, 5755402.48], [469017.61, 5738280.59], [465348.63, 5710151.76], [473298.08, 5695475.85], [468406.11, 5678965.45], [461068.15, 5656951.59], [448838.23, 5654811.35], [437066.93, 5651753.87], [435385.31, 5636772.21], [434468.07, 5621943.43], [435232.44, 5604821.54]], [[15075140.03, 4120873.07], [15084083.16, 4126223.66], [15096313.09, 4135243.23], [15104262.54, 4148543.27], [15106899.61, 4163639.59], [15092644.11, 4166888.16], [15084637.33, 4184449.57], [15114743.96, 4195962.89]]]}
    },
    6: {
        "geometry": MULTIPOLYGON_france_japan_3857,
        "tolerance": 30000,
        "algo": 'RDP',
        "return_value": {'type': 'MultiPolygon', 'coordinates': [[[[273950.31, 6643295.0], [190786.82, 6599267.27], [190786.82, 6467184.09], [4891.97, 6364452.72], [39135.76, 6335100.9], [-122299.25, 6315533.03], [-141867.12, 6388912.57], [-200570.76, 6388912.57], [-151651.06, 6207909.69], [-513656.83, 6217693.63], [-528332.74, 6163881.96], [-469629.1, 6134530.14], [-513656.83, 6119854.23], [-484305.01, 6061150.59], [-450061.22, 6105178.32], [-313086.07, 6056258.63], [-136975.15, 5826336.04], [-73379.55, 5640441.19], [-127191.22, 5699144.83], [-127191.22, 5523033.92], [-195678.79, 5356706.94], [63595.61, 5258867.55], [73379.55, 5293111.33], [362005.77, 5214839.82], [327761.98, 5307787.24], [464737.13, 5390950.73], [665307.89, 5327355.12], [841418.81, 5420302.55], [748471.38, 5625765.28], [768039.26, 5836119.98], [684875.77, 5782308.32], [679983.8, 5860579.83], [841418.81, 6031798.78], [914798.35, 6271505.3], [635956.08, 6344884.84], [322870.01, 6555239.55], [273950.31, 6643295.0]]], [[[15683655.21, 5090094.59], [15574808.88, 4961680.38], [15589484.79, 4786792.46], [15546680.06, 4662047.23], [15280067.7, 4402772.83], [15240931.94, 4446800.56], [15294743.61, 4505504.2], [15214026.11, 4493274.27], [15226256.03, 4407664.8], [15128416.64, 4297595.48], [15143092.55, 4251121.77], [15079496.94, 4226661.92], [15052591.11, 4278027.6], [14763964.89, 4229107.9], [14773748.83, 4194864.11], [14568286.09, 4075010.85], [14585407.99, 4023645.17], [14732167.08, 4004077.29], [14732167.08, 4084794.79], [14900940.04, 4077456.84], [14969427.62, 4131268.5], [15072158.99, 4131268.5], [15099064.82, 3955157.59], [15236039.97, 4092132.75], [15216472.09, 4182634.19], [15377907.1, 4121484.57], [15461070.59, 4194864.11], [15441502.71, 4116592.6], [15573585.89, 4258459.72], [15605383.69, 4241337.83], [15568693.92, 4155728.35], [15634735.51, 4194864.11], [15678763.24, 4265797.67], [15634735.51, 4329393.28], [15688547.18, 4593559.65], [15715453.02, 4647371.32], [15761926.73, 4630249.43], [15810846.43, 4806360.34], [15747250.82, 5080310.65], [15683655.21, 5090094.59]]]]}
    },
    7: {
        "geometry": MULTIPOLYGON_france_japan_3857,
        "tolerance": 3000000000,
        "algo": 'VW',
        "return_value": {'type': 'MultiPolygon', 'coordinates': [[[[273950.31, 6643295.0], [190786.82, 6599267.27], [190786.82, 6467184.09], [44027.73, 6408480.45], [39135.76, 6335100.9], [-122299.25, 6315533.03], [-151651.06, 6207909.69], [-288626.22, 6183449.84], [-337545.92, 6237261.51], [-513656.83, 6217693.63], [-469629.1, 6134530.14], [-313086.07, 6056258.63], [-225030.61, 5953527.26], [-136975.15, 5826336.04], [-127191.22, 5699144.83], [-127191.22, 5523033.92], [-195678.79, 5356706.94], [63595.61, 5258867.55], [210354.7, 5229515.73], [362005.77, 5214839.82], [327761.98, 5307787.24], [464737.13, 5390950.73], [547900.62, 5386058.76], [665307.89, 5327355.12], [719119.56, 5342031.03], [841418.81, 5420302.55], [782715.17, 5488790.13], [748471.38, 5625765.28], [777823.2, 5718712.71], [768039.26, 5836119.98], [684875.77, 5782308.32], [679983.8, 5860579.83], [758255.32, 5938851.35], [841418.81, 6031798.78], [851202.75, 6114962.26], [914798.35, 6271505.3], [748471.38, 6291073.18], [635956.08, 6344884.84], [513656.83, 6447616.21], [322870.01, 6555239.55], [273950.31, 6643295.0]]], [[[15683655.21, 5090094.59], [15574808.88, 4961680.38], [15589484.79, 4786792.46], [15546680.06, 4662047.23], [15451286.65, 4551977.91], [15280067.7, 4402772.83], [15226256.03, 4407664.8], [15128416.64, 4297595.48], [15052591.11, 4278027.6], [14856912.31, 4229107.9], [14773748.83, 4194864.11], [14626989.73, 4087240.78], [14732167.08, 4084794.79], [14847128.37, 4087240.78], [14969427.62, 4131268.5], [15055037.09, 4075010.85], [15099064.82, 3955157.59], [15182228.31, 4052996.99], [15236039.97, 4092132.75], [15216472.09, 4182634.19], [15304527.55, 4119038.58], [15377907.1, 4121484.57], [15461070.59, 4194864.11], [15573585.89, 4258459.72], [15634735.51, 4329393.28], [15673871.27, 4432124.65], [15688547.18, 4593559.65], [15761926.73, 4715858.9], [15810846.43, 4806360.34], [15776602.64, 4933551.55], [15747250.82, 5080310.65], [15683655.21, 5090094.59]]]]}
    },
    8: {
        "geometry": GEOMETRYCOLLECTION_paris_tokyo_loire_katsuragawa_river_france_japan_3857,
        "tolerance": 5000,
        "algo": 'RDP',
        "return_value": {'type': 'GeometryCollection', 'geometries': [{'type': 'MultiPoint', 'coordinates': [[261473.94, 6250010.11], [15557242.85, 4257415.09]]}, {'type': 'MultiLineString', 'coordinates': [[[-237872.03, 5988382.54], [-174276.42, 5974318.13], [-145536.1, 5998777.98], [-37301.27, 6009173.42], [9172.44, 5977987.11], [48919.7, 5996943.49], [116184.28, 6010396.41], [149205.08, 6032410.27], [194455.8, 6079495.48], [218915.65, 6089890.92], [245209.99, 6084387.45], [295352.68, 6051978.15], [328984.97, 6018957.36], [317366.54, 5998166.48], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [426824.37, 5861802.83], [447615.24, 5848961.4], [448838.23, 5766409.41], [469017.61, 5738280.59], [465348.63, 5710151.76], [473298.08, 5695475.85], [461068.15, 5656951.59], [437066.93, 5651753.87], [435232.44, 5604821.54]], [[15075140.03, 4120873.07], [15110262.84, 4155919.45], [15082974.82, 4181449.41], [15099141.26, 4182901.72], [15114743.96, 4195962.89]]]}, {'type': 'MultiPolygon', 'coordinates': [[[[2.4609375, 51.12421276], [2.4609375, 51.12421276]]], [[[140.88867188, 41.52502957], [140.88867188, 41.52502957]]]]}]}
    },
    9: {
        "geometry": GEOMETRYCOLLECTION_paris_tokyo_loire_katsuragawa_river_france_japan_3857,
        "tolerance": 500000000,
        "algo": 'VW',
        "return_value": {'type': 'GeometryCollection', 'geometries': [{'type': 'MultiPoint', 'coordinates': [[261473.94, 6250010.11], [15557242.85, 4257415.09]]}, {'type': 'MultiLineString', 'coordinates': [[[-237872.03, 5988382.54], [-209743.21, 5987159.55], [-154097.05, 5986548.06], [-88055.46, 6004281.45], [-4891.97, 5983490.57], [48919.7, 5996943.49], [91724.43, 6009784.91], [149205.08, 6032410.27], [181002.88, 6060539.1], [245209.99, 6084387.45], [295352.68, 6051978.15], [328984.97, 6018957.36], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [409702.47, 5892377.64], [426824.37, 5861802.83], [451284.21, 5812271.63], [452507.21, 5782919.81], [465348.63, 5710151.76], [461068.15, 5656951.59], [435232.44, 5604821.54]], [[15075140.03, 4120873.07], [15114743.96, 4195962.89]]]}, {'type': 'MultiPolygon', 'coordinates': [[[[2.4609375, 51.12421276], [2.4609375, 51.12421276]]], [[[140.88867188, 41.52502957], [140.88867188, 41.52502957]]]]}]}
    },
    10: {
        "geometry": POINT_paris_3857,
        "tolerance": 5000,
        "algo": 'RDP',
        "return_value": POINT_paris_3857
    },
    11: {
        "geometry": POINT_paris_3857,
        "tolerance": 500000000,
        "algo": 'VW',
        "return_value": POINT_paris_3857
    },
    12: {
        "geometry": MULTIPOINT_paris_tokyo_3857,
        "tolerance": 5000,
        "algo": 'RDP',
        "return_value": MULTIPOINT_paris_tokyo_3857
    },
    13: {
        "geometry": MULTIPOINT_paris_tokyo_3857,
        "tolerance": 500000000,
        "algo": 'VW',
        "return_value": MULTIPOINT_paris_tokyo_3857
    },
}

def test_all():

    # simplify
    print(test_function(simplify, simplify_parameters))
