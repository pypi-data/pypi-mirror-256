from geoformat.driver.common_driver import load_data
from pathlib import Path

from tests.utils.tests_utils import test_function

# declare path
file_path_base = Path(__file__).parent.parent.parent.parent.joinpath

loire_path = file_path_base("data/geojson/loire.geojson")

gares_csv_path = file_path_base("data/csv/GARES_EXTRACT_ISO_8859_15.csv")

load_data_parameters = {
    0: {
        "path": loire_path,
        "http_headers": None,
        "encoding": None,
        "return_value": (
            """{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            -2.1368408203125,
            47.28295557691231
          ],
          [
            -1.8841552734374998,
            47.27550216573706
          ],
          [
            -1.77978515625,
            47.20837421346631
          ],
          [
            -1.5655517578125,
            47.19717795172789
          ],
          [
            -1.3842773437499998,
            47.27177506640828
          ],
          [
            -1.307373046875,
            47.34626718205302
          ],
          [
            -1.0711669921875,
            47.368594345213374
          ],
          [
            -0.9393310546875,
            47.37603463349758
          ],
          [
            -0.791015625,
            47.37975438400816
          ],
          [
            -0.703125,
            47.37975438400816
          ],
          [
            -0.5987548828125,
            47.409502941311075
          ],
          [
            -0.472412109375,
            47.409502941311075
          ],
          [
            -0.3350830078125,
            47.409502941311075
          ],
          [
            -0.2911376953125,
            47.4057852900587
          ],
          [
            -0.208740234375,
            47.331377157798244
          ],
          [
            -0.0439453125,
            47.253135632244216
          ],
          [
            0.0823974609375,
            47.21956811231547
          ],
          [
            0.164794921875,
            47.234489635299184
          ],
          [
            0.439453125,
            47.33510005753559
          ],
          [
            0.6042480468749999,
            47.36115300722623
          ],
          [
            0.823974609375,
            47.41322033016902
          ],
          [
            1.043701171875,
            47.416937456635445
          ],
          [
            1.34033203125,
            47.55057928124212
          ],
          [
            1.395263671875,
            47.632081940263305
          ],
          [
            1.6259765625,
            47.720849190702324
          ],
          [
            1.636962890625,
            47.787325537803106
          ],
          [
            1.746826171875,
            47.83528342275264
          ],
          [
            1.8402099609375,
            47.86108855623179
          ],
          [
            1.966552734375,
            47.897930761804965
          ],
          [
            2.2027587890625,
            47.864773955792245
          ],
          [
            2.3126220703125,
            47.82053186746053
          ],
          [
            2.6531982421875,
            47.669086647137576
          ],
          [
            2.7630615234375,
            47.58764167941513
          ],
          [
            2.955322265625,
            47.468949677672484
          ],
          [
            2.8509521484375,
            47.342545069660225
          ],
          [
            3.076171875,
            47.16730970131578
          ],
          [
            3.09814453125,
            46.99524110694593
          ],
          [
            3.4991455078125,
            46.81885778879603
          ],
          [
            3.680419921875,
            46.694667307773116
          ],
          [
            3.7078857421874996,
            46.63057868059483
          ],
          [
            3.834228515625,
            46.50595444552049
          ],
          [
            4.02099609375,
            46.426499019253
          ],
          [
            4.053955078125,
            46.198844376182535
          ],
          [
            4.06494140625,
            46.01603873833416
          ],
          [
            4.031982421875,
            45.91294412737392
          ],
          [
            4.10888671875,
            45.84410779560204
          ],
          [
            4.2132568359375,
            45.73685954736049
          ],
          [
            4.1802978515625,
            45.56021795715051
          ],
          [
            4.251708984375,
            45.46783598133375
          ],
          [
            4.207763671875,
            45.36372498305678
          ],
          [
            4.141845703125,
            45.22461173085719
          ],
          [
            4.031982421875,
            45.2110686297804
          ],
          [
            3.9262390136718754,
            45.19171574701543
          ],
          [
            3.922119140625,
            45.1394300814679
          ],
          [
            3.9111328125000004,
            45.09679146394738
          ],
          [
            3.9578247070312496,
            45.02015580433459
          ],
          [
            3.90289306640625,
            45.002680147135955
          ],
          [
            3.9125061035156246,
            44.97645666320777
          ],
          [
            3.93310546875,
            44.94730538740607
          ],
          [
            3.909759521484375,
            44.89382291168926
          ]
        ]
      }
    }
  ]
}
""",
            "loire",
        ),
    },
    1: {
        "path": gares_csv_path,
        "http_headers": None,
        "encoding": None,
        "return_value": "'utf-8' codec can't decode byte 0xe9 in position 324: invalid continuation byte",
    },
    2: {
        "path": gares_csv_path,
        "http_headers": None,
        "encoding": "iso-8859-15",
        "return_value": (
            """code_uic,libelle_gare,fret,voyageurs,code_ligne,rang,pk,x_lambert,y_lambert,x_wgs84,y_wgs84,commune,departement
87471185,Messac-Guipry,N,O,463000,1,398+272,339653,6757878,-202440,6077344,Messac,Ille-et-Vilaine
87471029,Vern,N,O,466000,1,50+491,357685,6781809,-177731,6114673,Vern-sur-Seiche,Ille-et-Vilaine
87476317,Quimperlé,O,O,470000,1,639+694,210637,6772419,-395516,6085140,Quimperlé,Finistère
87474031,Hanvec,N,N,470000,1,740+360,171994,6828441,-460348,6163846,Hanvec,Finistère
87476671,Questembert,O,O,470000,1,540+326,291464,6745525,-272690,6054309,Questembert,Morbihan
87476648,Ste-Anne,N,O,470000,1,581+996,253190,6747773,-329570,6053535,Pluneret,Morbihan
87471243,St-Méen,O,N,472000,1,68+200,315077,6800114,-243043,6138128,St-Méen-le-Grand,Ille-et-Vilaine
87476200,Auray,O,O,473000,1,584+946,250286,6748188,-333913,6053823,Auray,Morbihan
87476408,Belz-Ploemel,N,O,473000,1,591+597,244616,6745536,-341998,6049244,Ploemel,Morbihan
87473330,Quintin,O,O,475000,1,492+810,264298,6827046,-321902,6173216,St-Brandan,Côte-d'Armor
87473389,Loudéac,O,O,475000,1,523+646,272034,6802276,-307584,6136890,Loudéac,Côte-d'Armor
87473520,Pont-Melvez,N,O,485000,1,523+525,233973,6837507,-368620,6185426,Pont-Melvez,Côte-d'Armor
87473546,Callac,N,O,485000,1,537+640,225505,6831132,-380551,6174805,Callac,Côte-d'Armor
87473504,Carhaix,O,O,485000,1,557+991,213580,6817576,-396733,6152971,Carhaix-Plouguer,Finistère
87322347,Traou-Nez,N,O,486000,1,533+580,249361,6867342,-349003,6232303,Plourivo,Côte-d'Armor
87491290,Loulay,N,O,500000,1,450+644,429297,6555301,-55846,5787313,Loulay,Charente-Maritime
87491357,St-Jean-d'Angély,O,O,500000,1,463+049,428167,6543942,-56744,5770867,St-Jean-d'Angély,Charente-Maritime
87491001,Saintes,O,O,500000,1,488+553,418839,6522913,-68749,5740032,Saintes,Charente-Maritime
""",
            "GARES_EXTRACT_ISO_8859_15",
        ),
    },
    3: {
        "path": gares_csv_path,
        "http_headers": None,
        "encoding": "iso-8859-15",
        "return_value": (
            """code_uic,libelle_gare,fret,voyageurs,code_ligne,rang,pk,x_lambert,y_lambert,x_wgs84,y_wgs84,commune,departement
87471185,Messac-Guipry,N,O,463000,1,398+272,339653,6757878,-202440,6077344,Messac,Ille-et-Vilaine
87471029,Vern,N,O,466000,1,50+491,357685,6781809,-177731,6114673,Vern-sur-Seiche,Ille-et-Vilaine
87476317,Quimperlé,O,O,470000,1,639+694,210637,6772419,-395516,6085140,Quimperlé,Finistère
87474031,Hanvec,N,N,470000,1,740+360,171994,6828441,-460348,6163846,Hanvec,Finistère
87476671,Questembert,O,O,470000,1,540+326,291464,6745525,-272690,6054309,Questembert,Morbihan
87476648,Ste-Anne,N,O,470000,1,581+996,253190,6747773,-329570,6053535,Pluneret,Morbihan
87471243,St-Méen,O,N,472000,1,68+200,315077,6800114,-243043,6138128,St-Méen-le-Grand,Ille-et-Vilaine
87476200,Auray,O,O,473000,1,584+946,250286,6748188,-333913,6053823,Auray,Morbihan
87476408,Belz-Ploemel,N,O,473000,1,591+597,244616,6745536,-341998,6049244,Ploemel,Morbihan
87473330,Quintin,O,O,475000,1,492+810,264298,6827046,-321902,6173216,St-Brandan,Côte-d'Armor
87473389,Loudéac,O,O,475000,1,523+646,272034,6802276,-307584,6136890,Loudéac,Côte-d'Armor
87473520,Pont-Melvez,N,O,485000,1,523+525,233973,6837507,-368620,6185426,Pont-Melvez,Côte-d'Armor
87473546,Callac,N,O,485000,1,537+640,225505,6831132,-380551,6174805,Callac,Côte-d'Armor
87473504,Carhaix,O,O,485000,1,557+991,213580,6817576,-396733,6152971,Carhaix-Plouguer,Finistère
87322347,Traou-Nez,N,O,486000,1,533+580,249361,6867342,-349003,6232303,Plourivo,Côte-d'Armor
87491290,Loulay,N,O,500000,1,450+644,429297,6555301,-55846,5787313,Loulay,Charente-Maritime
87491357,St-Jean-d'Angély,O,O,500000,1,463+049,428167,6543942,-56744,5770867,St-Jean-d'Angély,Charente-Maritime
87491001,Saintes,O,O,500000,1,488+553,418839,6522913,-68749,5740032,Saintes,Charente-Maritime
""",
            "GARES_EXTRACT_ISO_8859_15",
        ),
    },
    4: {
        "path": "https://framagit.org/Guilhain/Geoformat/-/raw/925196e7335f7743531a963f0617d25052b9462d/data/geojson/loire.geojson",
        "http_headers": None,
        "encoding": "utf8",
        "return_value": (
            """{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            -2.1368408203125,
            47.28295557691231
          ],
          [
            -1.8841552734374998,
            47.27550216573706
          ],
          [
            -1.77978515625,
            47.20837421346631
          ],
          [
            -1.5655517578125,
            47.19717795172789
          ],
          [
            -1.3842773437499998,
            47.27177506640828
          ],
          [
            -1.307373046875,
            47.34626718205302
          ],
          [
            -1.0711669921875,
            47.368594345213374
          ],
          [
            -0.9393310546875,
            47.37603463349758
          ],
          [
            -0.791015625,
            47.37975438400816
          ],
          [
            -0.703125,
            47.37975438400816
          ],
          [
            -0.5987548828125,
            47.409502941311075
          ],
          [
            -0.472412109375,
            47.409502941311075
          ],
          [
            -0.3350830078125,
            47.409502941311075
          ],
          [
            -0.2911376953125,
            47.4057852900587
          ],
          [
            -0.208740234375,
            47.331377157798244
          ],
          [
            -0.0439453125,
            47.253135632244216
          ],
          [
            0.0823974609375,
            47.21956811231547
          ],
          [
            0.164794921875,
            47.234489635299184
          ],
          [
            0.439453125,
            47.33510005753559
          ],
          [
            0.6042480468749999,
            47.36115300722623
          ],
          [
            0.823974609375,
            47.41322033016902
          ],
          [
            1.043701171875,
            47.416937456635445
          ],
          [
            1.34033203125,
            47.55057928124212
          ],
          [
            1.395263671875,
            47.632081940263305
          ],
          [
            1.6259765625,
            47.720849190702324
          ],
          [
            1.636962890625,
            47.787325537803106
          ],
          [
            1.746826171875,
            47.83528342275264
          ],
          [
            1.8402099609375,
            47.86108855623179
          ],
          [
            1.966552734375,
            47.897930761804965
          ],
          [
            2.2027587890625,
            47.864773955792245
          ],
          [
            2.3126220703125,
            47.82053186746053
          ],
          [
            2.6531982421875,
            47.669086647137576
          ],
          [
            2.7630615234375,
            47.58764167941513
          ],
          [
            2.955322265625,
            47.468949677672484
          ],
          [
            2.8509521484375,
            47.342545069660225
          ],
          [
            3.076171875,
            47.16730970131578
          ],
          [
            3.09814453125,
            46.99524110694593
          ],
          [
            3.4991455078125,
            46.81885778879603
          ],
          [
            3.680419921875,
            46.694667307773116
          ],
          [
            3.7078857421874996,
            46.63057868059483
          ],
          [
            3.834228515625,
            46.50595444552049
          ],
          [
            4.02099609375,
            46.426499019253
          ],
          [
            4.053955078125,
            46.198844376182535
          ],
          [
            4.06494140625,
            46.01603873833416
          ],
          [
            4.031982421875,
            45.91294412737392
          ],
          [
            4.10888671875,
            45.84410779560204
          ],
          [
            4.2132568359375,
            45.73685954736049
          ],
          [
            4.1802978515625,
            45.56021795715051
          ],
          [
            4.251708984375,
            45.46783598133375
          ],
          [
            4.207763671875,
            45.36372498305678
          ],
          [
            4.141845703125,
            45.22461173085719
          ],
          [
            4.031982421875,
            45.2110686297804
          ],
          [
            3.9262390136718754,
            45.19171574701543
          ],
          [
            3.922119140625,
            45.1394300814679
          ],
          [
            3.9111328125000004,
            45.09679146394738
          ],
          [
            3.9578247070312496,
            45.02015580433459
          ],
          [
            3.90289306640625,
            45.002680147135955
          ],
          [
            3.9125061035156246,
            44.97645666320777
          ],
          [
            3.93310546875,
            44.94730538740607
          ],
          [
            3.909759521484375,
            44.89382291168926
          ]
        ]
      }
    }
  ]
}
""",
            "loire",
        ),
    },
    5: {
        "path": 'foo/bar.csv',
        "encoding": 'utf8',
        "http_headers": None,
        "return_value": 'cannot load data file or http address does not exists'
    }
}


def test_all():

    # load_data
    print(test_function(load_data, load_data_parameters))


if __name__ == "__main__":
    test_all()
    # print(load_data(**{
    #     "path": 'https://framagit.org/Guilhain/Geoformat/-/raw/925196e7335f7743531a963f0617d25052b9462d/data/geojson/loire.geojson',
    #     "http_headers": None,
    #     "encoding": 'utf8',
    # }))
    # a = load_data(**{
    #     "path": 'https://france-geojson.gregoiredavid.fr/repo/regions.geojson',
    #     "http_headers": None,
    #     "encoding": 'utf8',
    # })
    # with open(a[0].name, 'r') as tmp:
    #     print(tmp.read())
    #     print('fin')
