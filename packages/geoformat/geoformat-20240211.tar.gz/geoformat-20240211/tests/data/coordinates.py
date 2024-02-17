coordinates_with_tuple = [
    [
        (650942.200000008, 6857645.800000944),
        (645325.1000000088, 6859675.200000941),
        (643644.0000000091, 6863500.900000929),
    ],
    [(670055.5000000049, 6856451.100000947), (671600.3000000048, 6851282.800000963)],
]

coordinates_with_list = (
    (
        [650942.200000008, 6857645.800000944],
        [645325.1000000088, 6859675.200000941],
        [643644.0000000091, 6863500.900000929],
    ),
    ([670055.5000000049, 6856451.100000947], [671600.3000000048, 6851282.800000963]),
)

coordinates_with_duplicated_coordinates = [
    [
        [650942.200000008, 6857645.800000944],
        [645325.1000000088, 6859675.200000941],
        [645325.1000000088, 6859675.200000941],
        [643644.0000000091, 6863500.900000929],
    ],
    [
        [670055.5000000049, 6856451.100000947],
        [671600.3000000048, 6851282.800000963],
        [671600.3000000048, 6851282.800000963],
    ],
    [
        [799606.7999999593, 6263118.800002612],
        [799606.7999999593, 6263118.800002612],
        [825917.6999999485, 6262029.800002615],
    ],
    [
        [869889.3999999303, 6258065.200002626],
        [869889.3999999303, 6258065.200002626],
        [866898.8999999315, 6258271.7000026265],
        [866898.8999999315, 6258271.7000026265],
        [866898.8999999315, 6258271.7000026265],
        [866104.2999999323, 6264876.400002609],
        [862373.7999999337, 6265459.30000261],
        [862373.7999999337, 6265459.30000261],
        [862373.7999999337, 6265459.30000261],
        [862373.7999999337, 6265459.30000261],
    ],
]

point_coordinates = [-115.81, 37.24]

linestring_coordinates = [[8.919, 44.4074], [8.923, 44.4075]]

polygon_coordinates = [
    [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
    [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]],
]

multipoint_coordinates = [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]]

multilinestring_coordinates = [
    [[3.75, 9.25], [-130.95, 1.52]],
    [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]],
]

multipolygon_coordinates = [
    [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]],
    [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]],
]

point_coordinates_3d = [-115.81, 37.24, -38.654]

linestring_coordinates_3d = [[8.919, 44.4074, 254.8], [8.923, 44.4075, -98]]

polygon_coordinates_3d = [
    [
        [2.38, 57.322, -76.65],
        [23.194, -20.28, 145],
        [-120.43, 19.15, 0.146],
        [2.38, 57.322, 78.89],
    ],
    [
        [-5.21, 23.51, 154.4],
        [15.21, -10.81],
        [-20.51, 1.51, -32.6],
        [-5.21, 23.51, 45.6],
    ],
]

multipoint_coordinates_3d = [
    [-155.52, 19.61, 78.45],
    [-156.22, 20.74, 12.65],
    [-157.97, 21.46, -75.15],
]

multilinestring_coordinates_3d = [
    [[3.75, 9.25, -65.45], [-130.95, 1.52, 45.54]],
    [[23.15, -34.25, 15.584], [-1.35, -4.65, -98.45], [3.45, 77.95, 78.14]],
]

multipolygon_coordinates_3d = [
    [
        [
            [3.78, 9.28, 123],
            [-130.91, 1.52, 15.54],
            [35.12, 72.234, 78.6],
            [3.78, 9.28, 87.878],
        ]
    ],
    [
        [
            [23.18, -34.29, -45.1515],
            [-1.31, -4.61, -3.245],
            [3.41, 77.91, -41.0],
            [23.18, -34.29, -87.89],
        ]
    ],
]

loire_4326 = [[-2.13684082, 47.28295558], [-1.88415527, 47.27550217], [-1.77978516, 47.20837421], [-1.56555176, 47.19717795], [-1.38427734, 47.27177507], [-1.30737305, 47.34626718], [-1.07116699, 47.36859435], [-0.93933105, 47.37603463], [-0.79101562, 47.37975438], [-0.703125, 47.37975438], [-0.59875488, 47.40950294], [-0.47241211, 47.40950294], [-0.33508301, 47.40950294], [-0.2911377, 47.40578529], [-0.20874023, 47.33137716], [-0.04394531, 47.25313563], [0.08239746, 47.21956811], [0.16479492, 47.23448964], [0.43945312, 47.33510006], [0.60424805, 47.36115301], [0.82397461, 47.41322033], [1.04370117, 47.41693746], [1.34033203, 47.55057928], [1.39526367, 47.63208194], [1.62597656, 47.72084919], [1.63696289, 47.78732554], [1.74682617, 47.83528342], [1.84020996, 47.86108856], [1.96655273, 47.89793076], [2.20275879, 47.86477396], [2.31262207, 47.82053187], [2.65319824, 47.66908665], [2.76306152, 47.58764168], [2.95532227, 47.46894968], [2.85095215, 47.34254507], [3.07617188, 47.1673097], [3.09814453, 46.99524111], [3.49914551, 46.81885779], [3.68041992, 46.69466731], [3.70788574, 46.63057868], [3.83422852, 46.50595445], [4.02099609, 46.42649902], [4.05395508, 46.19884438], [4.06494141, 46.01603874], [4.03198242, 45.91294413], [4.10888672, 45.8441078], [4.21325684, 45.73685955], [4.18029785, 45.56021796], [4.25170898, 45.46783598], [4.20776367, 45.36372498], [4.1418457, 45.22461173], [4.03198242, 45.21106863], [3.92623901, 45.19171575], [3.92211914, 45.13943008], [3.91113281, 45.09679146], [3.95782471, 45.0201558], [3.90289307, 45.00268015], [3.9125061, 44.97645666], [3.93310547, 44.94730539], [3.90975952, 44.89382291]]

loire_3857 = [[-237872.03, 5988382.54], [-209743.21, 5987159.55], [-198124.78, 5976152.62], [-174276.42, 5974318.13], [-154097.05, 5986548.06], [-145536.1, 5998777.98], [-119241.76, 6002446.96], [-104565.85, 6003669.95], [-88055.46, 6004281.45], [-78271.52, 6004281.45], [-66653.09, 6009173.42], [-52588.68, 6009173.42], [-37301.27, 6009173.42], [-32409.3, 6008561.92], [-23236.86, 5996331.99], [-4891.97, 5983490.57], [9172.44, 5977987.11], [18344.89, 5980433.09], [48919.7, 5996943.49], [67264.58, 6001223.96], [91724.43, 6009784.91], [116184.28, 6010396.41], [149205.08, 6032410.27], [155320.04, 6045863.19], [181002.88, 6060539.1], [182225.88, 6071546.03], [194455.8, 6079495.48], [204851.24, 6083775.96], [218915.65, 6089890.92], [245209.99, 6084387.45], [257439.91, 6077049.5], [295352.68, 6051978.15], [307582.6, 6038525.23], [328984.97, 6018957.36], [317366.54, 5998166.48], [342437.89, 5969426.16], [344883.87, 5941297.33], [389523.1, 5912557.01], [409702.47, 5892377.64], [412759.95, 5881982.2], [426824.37, 5861802.83], [447615.24, 5848961.4], [451284.21, 5812271.63], [452507.21, 5782919.81], [448838.23, 5766409.41], [457399.18, 5755402.48], [469017.61, 5738280.59], [465348.63, 5710151.76], [473298.08, 5695475.85], [468406.11, 5678965.45], [461068.15, 5656951.59], [448838.23, 5654811.35], [437066.93, 5651753.87], [436608.31, 5643498.67], [435385.31, 5636772.21], [440583.03, 5624695.16], [434468.07, 5621943.43], [435538.19, 5617815.83], [437831.3, 5613229.61], [435232.44, 5604821.54]]

katsuragawa_river_4326 = [[135.42228699, 34.68291097], [135.50262451, 34.7224262], [135.61248779, 34.78899485], [135.68389893, 34.88705743], [135.73471069, 34.92422302], [135.7378006, 34.94139234], [135.7075882, 34.99822246], [135.6911087, 34.99822246], [135.65402985, 35.02999637], [135.57952881, 35.02212434], [135.54905891, 35.05262423], [135.51189423, 35.0926644], [135.51695824, 35.11653865], [135.49266815, 35.12917513], [135.50760269, 35.15121407], [135.51644325, 35.15345974], [135.51738739, 35.14665236], [135.53704262, 35.14430122], [135.54309368, 35.13215846], [135.56824207, 35.12829766], [135.57761908, 35.13886177], [135.57173967, 35.14558208], [135.583992, 35.14419595], [135.60270309, 35.13844064], [135.60956955, 35.13212336], [135.63789368, 35.13984441], [135.63274384, 35.15409133], [135.64982414, 35.17079144], [135.6748867, 35.18664635], [135.68166733, 35.19667684], [135.70218086, 35.19836016], [135.7095623, 35.19302953], [135.71187973, 35.2025683], [135.71685791, 35.21161507], [135.72526932, 35.20130588], [135.73608398, 35.21035279], [135.74762821, 35.2038307], [135.75419426, 35.20873985], [135.75912952, 35.20183189], [135.76183319, 35.20453203], [135.77406406, 35.205584], [135.77968597, 35.22199307], [135.77805519, 35.23573486]]

katsuragawa_river_3857 = [[15075140.03, 4120873.07], [15084083.16, 4126223.66], [15096313.09, 4135243.23], [15104262.54, 4148543.27], [15109918.88, 4153588.12], [15110262.84, 4155919.45], [15106899.61, 4163639.59], [15105065.13, 4163639.59], [15100937.53, 4167958.28], [15092644.11, 4166888.16], [15089252.22, 4171034.87], [15085115.06, 4176481.01], [15085678.78, 4179729.58], [15082974.82, 4181449.41], [15084637.33, 4184449.57], [15085621.46, 4184755.32], [15085726.56, 4183828.52], [15087914.57, 4183508.44], [15088588.17, 4181855.49], [15091387.68, 4181329.98], [15092431.52, 4182767.95], [15091777.03, 4183682.81], [15093140.95, 4183494.1], [15095223.86, 4182710.62], [15095988.23, 4181850.71], [15099141.26, 4182901.72], [15098567.98, 4184841.31], [15100469.35, 4187115.31], [15103259.3, 4189274.65], [15104014.12, 4190640.97], [15106297.67, 4190870.28], [15107119.37, 4190144.13], [15107377.35, 4191443.56], [15107931.51, 4192676.1], [15108867.87, 4191271.57], [15110071.75, 4192504.12], [15111356.85, 4191615.54], [15112087.78, 4192284.36], [15112637.17, 4191343.23], [15112938.14, 4191711.08], [15114299.67, 4191854.4], [15114925.5, 4194090.19], [15114743.96, 4195962.89]]

paris_4326 = [2.34886039, 48.85332408]

paris_3857 = [261473.94, 6250010.11]

tokyo_4326 = [139.75309029, 35.68537297]

tokyo_3857 = [15557242.85, 4257415.09]

france_4326 = [[[2.4609375, 51.12421276], [1.71386719, 50.87531114], [1.71386719, 50.1205781], [0.39550781, 49.78126406], [0.04394531, 49.52520834], [0.3515625, 49.35375572], [-1.09863281, 49.23912083], [-1.27441406, 49.66762782], [-1.80175781, 49.66762782], [-1.58203125, 49.23912083], [-1.36230469, 48.60385761], [-2.59277344, 48.45835188], [-3.03222656, 48.77791276], [-4.61425781, 48.66194285], [-4.74609375, 48.34164617], [-4.39453125, 48.3708477], [-4.21875, 48.16608542], [-4.61425781, 48.07807894], [-4.35058594, 47.72454455], [-4.04296875, 47.98992167], [-2.8125, 47.69497434], [-2.02148438, 47.07012182], [-2.24121094, 46.92025532], [-1.23046875, 46.28622392], [-1.01074219, 45.76752296], [-0.65917969, 45.12005284], [-1.14257812, 45.49094569], [-1.14257812, 44.37098696], [-1.7578125, 43.29320031], [0.57128906, 42.65012181], [0.65917969, 42.8759641], [1.88964844, 42.45588764], [3.25195312, 42.35854392], [2.94433594, 42.97250159], [4.17480469, 43.51668854], [4.921875, 43.48481213], [5.9765625, 43.10098288], [6.45996094, 43.19716728], [7.55859375, 43.7075935], [7.60253906, 44.08758503], [7.03125, 44.15068116], [6.72363281, 45.02695045], [6.98730469, 45.61403741], [6.89941406, 46.34692761], [6.15234375, 46.01222384], [6.10839844, 46.49839226], [6.81152344, 46.98025236], [7.55859375, 47.5468716], [7.64648437, 48.04870994], [8.21777344, 48.98021699], [6.72363281, 49.09545216], [6.41601562, 49.46812407], [5.71289062, 49.4109732], [4.61425781, 50.00773901], [2.90039062, 50.62507306], [2.4609375, 51.12421276]]]

france_3857 = [[[273950.31, 6643295.0], [190786.82, 6599267.27], [190786.82, 6467184.09], [44027.73, 6408480.45], [4891.97, 6364452.72], [39135.76, 6335100.9], [-122299.25, 6315533.03], [-141867.12, 6388912.57], [-200570.76, 6388912.57], [-176110.91, 6315533.03], [-151651.06, 6207909.69], [-288626.22, 6183449.84], [-337545.92, 6237261.51], [-513656.83, 6217693.63], [-528332.74, 6163881.96], [-489196.98, 6168773.93], [-469629.1, 6134530.14], [-513656.83, 6119854.23], [-484305.01, 6061150.59], [-450061.22, 6105178.32], [-313086.07, 6056258.63], [-225030.61, 5953527.26], [-249490.46, 5929067.41], [-136975.15, 5826336.04], [-112515.31, 5743172.56], [-73379.55, 5640441.19], [-127191.22, 5699144.83], [-127191.22, 5523033.92], [-195678.79, 5356706.94], [63595.61, 5258867.55], [73379.55, 5293111.33], [210354.7, 5229515.73], [362005.77, 5214839.82], [327761.98, 5307787.24], [464737.13, 5390950.73], [547900.62, 5386058.76], [665307.89, 5327355.12], [719119.56, 5342031.03], [841418.81, 5420302.55], [846310.78, 5479006.19], [782715.17, 5488790.13], [748471.38, 5625765.28], [777823.2, 5718712.71], [768039.26, 5836119.98], [684875.77, 5782308.32], [679983.8, 5860579.83], [758255.32, 5938851.35], [841418.81, 6031798.78], [851202.75, 6114962.26], [914798.35, 6271505.3], [748471.38, 6291073.18], [714227.59, 6354668.78], [635956.08, 6344884.84], [513656.83, 6447616.21], [322870.01, 6555239.55], [273950.31, 6643295.0]]]

japan_4326 = [[[140.88867188, 41.52502957], [139.91088867, 40.65563874], [140.04272461, 39.45316113], [139.65820312, 38.58252616], [138.80126953, 37.80544395], [137.26318359, 36.73888412], [136.91162109, 37.05517711], [137.39501953, 37.47485808], [136.66992188, 37.3876175], [136.77978516, 36.77409249], [135.90087891, 35.97800618], [136.03271484, 35.63944107], [135.46142578, 35.46066995], [135.21972656, 35.83562839], [133.46191406, 35.478565], [133.19824219, 35.58585159], [132.62695312, 35.478565], [132.71484375, 35.22767235], [131.39648438, 34.43409789], [130.86914062, 34.34343607], [131.02294922, 33.96158629], [131.70410156, 34.05265942], [132.34130859, 33.81566631], [132.34130859, 34.41597338], [132.71484375, 34.28899187], [133.37402344, 34.43409789], [133.85742188, 34.36157629], [134.47265625, 34.75966612], [135, 34.66935855], [135.39550781, 34.75966612], [135.24169922, 34.34343607], [135.63720703, 33.44977658], [136.38427734, 34.17999759], [136.86767578, 34.47033512], [136.69189453, 35.13787912], [137.48291016, 34.66935855], [138.14208984, 34.68742795], [138.88916016, 35.22767235], [138.71337891, 34.6512852], [139.19677734, 34.99400376], [139.48242188, 35.3532161], [139.89990234, 35.69299463], [140.18554687, 35.56798046], [139.87792969, 35.20972165], [139.85595703, 34.93998515], [140.44921875, 35.22767235], [140.53710938, 35.65729625], [140.84472656, 35.74651226], [140.44921875, 36.20882309], [140.80078125, 36.94989179], [140.93261719, 38.09998265], [141.17431641, 38.47939467], [141.59179688, 38.35888786], [141.59179688, 38.95940879], [142.03125, 39.58875728], [141.72363281, 40.46366632], [141.43798828, 40.69729901], [141.45996094, 41.45919538], [141.21826172, 41.29431726], [140.88867188, 41.52502957]]]

japan_3857 = [[[15683655.21, 5090094.59], [15574808.88, 4961680.38], [15589484.79, 4786792.46], [15546680.06, 4662047.23], [15451286.65, 4551977.91], [15280067.7, 4402772.83], [15240931.94, 4446800.56], [15294743.61, 4505504.2], [15214026.11, 4493274.27], [15226256.03, 4407664.8], [15128416.64, 4297595.48], [15143092.55, 4251121.77], [15079496.94, 4226661.92], [15052591.11, 4278027.6], [14856912.31, 4229107.9], [14827560.49, 4243783.81], [14763964.89, 4229107.9], [14773748.83, 4194864.11], [14626989.73, 4087240.78], [14568286.09, 4075010.85], [14585407.99, 4023645.17], [14661233.52, 4035875.09], [14732167.08, 4004077.29], [14732167.08, 4084794.79], [14773748.83, 4067672.9], [14847128.37, 4087240.78], [14900940.04, 4077456.84], [14969427.62, 4131268.5], [15028131.26, 4119038.58], [15072158.99, 4131268.5], [15055037.09, 4075010.85], [15099064.82, 3955157.59], [15182228.31, 4052996.99], [15236039.97, 4092132.75], [15216472.09, 4182634.19], [15304527.55, 4119038.58], [15377907.1, 4121484.57], [15461070.59, 4194864.11], [15441502.71, 4116592.6], [15495314.37, 4163066.31], [15527112.18, 4211986.01], [15573585.89, 4258459.72], [15605383.69, 4241337.83], [15571139.91, 4192418.13], [15568693.92, 4155728.35], [15634735.51, 4194864.11], [15644519.45, 4253567.75], [15678763.24, 4265797.67], [15634735.51, 4329393.28], [15673871.27, 4432124.65], [15688547.18, 4593559.65], [15715453.02, 4647371.32], [15761926.73, 4630249.43], [15761926.73, 4715858.9], [15810846.43, 4806360.34], [15776602.64, 4933551.55], [15744804.83, 4967795.34], [15747250.82, 5080310.65], [15720344.99, 5055850.8], [15683655.21, 5090094.59]]]
