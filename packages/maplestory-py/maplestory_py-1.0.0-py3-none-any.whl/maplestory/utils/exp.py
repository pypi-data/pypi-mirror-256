from rich import print

exp_table = [
    {"level": 1, "required_exp": 15, "cumulative_exp": 15},
    {"level": 2, "required_exp": 34, "cumulative_exp": 49},
    {"level": 3, "required_exp": 57, "cumulative_exp": 106},
    {"level": 4, "required_exp": 92, "cumulative_exp": 198},
    {"level": 5, "required_exp": 135, "cumulative_exp": 333},
    {"level": 6, "required_exp": 372, "cumulative_exp": 705},
    {"level": 7, "required_exp": 560, "cumulative_exp": 1265},
    {"level": 8, "required_exp": 840, "cumulative_exp": 2105},
    {"level": 9, "required_exp": 1242, "cumulative_exp": 3347},
    {"level": 10, "required_exp": 1242, "cumulative_exp": 4589},
    {"level": 11, "required_exp": 1242, "cumulative_exp": 5831},
    {"level": 12, "required_exp": 1242, "cumulative_exp": 7073},
    {"level": 13, "required_exp": 1242, "cumulative_exp": 8315},
    {"level": 14, "required_exp": 1242, "cumulative_exp": 9557},
    {"level": 15, "required_exp": 1490, "cumulative_exp": 11047},
    {"level": 16, "required_exp": 1788, "cumulative_exp": 12835},
    {"level": 17, "required_exp": 2145, "cumulative_exp": 14980},
    {"level": 18, "required_exp": 2574, "cumulative_exp": 17554},
    {"level": 19, "required_exp": 3088, "cumulative_exp": 20642},
    {"level": 20, "required_exp": 3705, "cumulative_exp": 24347},
    {"level": 21, "required_exp": 4446, "cumulative_exp": 28793},
    {"level": 22, "required_exp": 5335, "cumulative_exp": 34128},
    {"level": 23, "required_exp": 6402, "cumulative_exp": 40530},
    {"level": 24, "required_exp": 7682, "cumulative_exp": 48212},
    {"level": 25, "required_exp": 9218, "cumulative_exp": 57430},
    {"level": 26, "required_exp": 11061, "cumulative_exp": 68491},
    {"level": 27, "required_exp": 13273, "cumulative_exp": 81764},
    {"level": 28, "required_exp": 15927, "cumulative_exp": 97691},
    {"level": 29, "required_exp": 19112, "cumulative_exp": 116803},
    {"level": 30, "required_exp": 19112, "cumulative_exp": 135915},
    {"level": 31, "required_exp": 19112, "cumulative_exp": 155027},
    {"level": 32, "required_exp": 19112, "cumulative_exp": 174139},
    {"level": 33, "required_exp": 19112, "cumulative_exp": 193251},
    {"level": 34, "required_exp": 19112, "cumulative_exp": 212363},
    {"level": 35, "required_exp": 22934, "cumulative_exp": 235297},
    {"level": 36, "required_exp": 27520, "cumulative_exp": 262817},
    {"level": 37, "required_exp": 33024, "cumulative_exp": 295841},
    {"level": 38, "required_exp": 39628, "cumulative_exp": 335469},
    {"level": 39, "required_exp": 47553, "cumulative_exp": 383022},
    {"level": 40, "required_exp": 51357, "cumulative_exp": 434379},
    {"level": 41, "required_exp": 55465, "cumulative_exp": 489844},
    {"level": 42, "required_exp": 59902, "cumulative_exp": 549746},
    {"level": 43, "required_exp": 64694, "cumulative_exp": 614440},
    {"level": 44, "required_exp": 69869, "cumulative_exp": 684309},
    {"level": 45, "required_exp": 75458, "cumulative_exp": 759767},
    {"level": 46, "required_exp": 81494, "cumulative_exp": 841261},
    {"level": 47, "required_exp": 88013, "cumulative_exp": 929274},
    {"level": 48, "required_exp": 95054, "cumulative_exp": 1024328},
    {"level": 49, "required_exp": 102658, "cumulative_exp": 1126986},
    {"level": 50, "required_exp": 110870, "cumulative_exp": 1237856},
    {"level": 51, "required_exp": 119739, "cumulative_exp": 1357595},
    {"level": 52, "required_exp": 129318, "cumulative_exp": 1486913},
    {"level": 53, "required_exp": 139663, "cumulative_exp": 1626576},
    {"level": 54, "required_exp": 150836, "cumulative_exp": 1777412},
    {"level": 55, "required_exp": 162902, "cumulative_exp": 1940314},
    {"level": 56, "required_exp": 175934, "cumulative_exp": 2116248},
    {"level": 57, "required_exp": 190008, "cumulative_exp": 2306256},
    {"level": 58, "required_exp": 205208, "cumulative_exp": 2511464},
    {"level": 59, "required_exp": 221624, "cumulative_exp": 2733088},
    {"level": 60, "required_exp": 221624, "cumulative_exp": 2954712},
    {"level": 61, "required_exp": 221624, "cumulative_exp": 3176336},
    {"level": 62, "required_exp": 221624, "cumulative_exp": 3397960},
    {"level": 63, "required_exp": 221624, "cumulative_exp": 3619584},
    {"level": 64, "required_exp": 221624, "cumulative_exp": 3841208},
    {"level": 65, "required_exp": 238245, "cumulative_exp": 4079453},
    {"level": 66, "required_exp": 256113, "cumulative_exp": 4335566},
    {"level": 67, "required_exp": 275321, "cumulative_exp": 4610887},
    {"level": 68, "required_exp": 295970, "cumulative_exp": 4906857},
    {"level": 69, "required_exp": 318167, "cumulative_exp": 5225024},
    {"level": 70, "required_exp": 342029, "cumulative_exp": 5567053},
    {"level": 71, "required_exp": 367681, "cumulative_exp": 5934734},
    {"level": 72, "required_exp": 395257, "cumulative_exp": 6329991},
    {"level": 73, "required_exp": 424901, "cumulative_exp": 6754892},
    {"level": 74, "required_exp": 456768, "cumulative_exp": 7211660},
    {"level": 75, "required_exp": 488741, "cumulative_exp": 7700401},
    {"level": 76, "required_exp": 522952, "cumulative_exp": 8223353},
    {"level": 77, "required_exp": 559558, "cumulative_exp": 8782911},
    {"level": 78, "required_exp": 598727, "cumulative_exp": 9381638},
    {"level": 79, "required_exp": 640637, "cumulative_exp": 10022275},
    {"level": 80, "required_exp": 685481, "cumulative_exp": 10707756},
    {"level": 81, "required_exp": 733464, "cumulative_exp": 11441220},
    {"level": 82, "required_exp": 784806, "cumulative_exp": 12226026},
    {"level": 83, "required_exp": 839742, "cumulative_exp": 13065768},
    {"level": 84, "required_exp": 898523, "cumulative_exp": 13964291},
    {"level": 85, "required_exp": 961419, "cumulative_exp": 14925710},
    {"level": 86, "required_exp": 1028718, "cumulative_exp": 15954428},
    {"level": 87, "required_exp": 1100728, "cumulative_exp": 17055156},
    {"level": 88, "required_exp": 1177778, "cumulative_exp": 18232934},
    {"level": 89, "required_exp": 1260222, "cumulative_exp": 19493156},
    {"level": 90, "required_exp": 1342136, "cumulative_exp": 20835292},
    {"level": 91, "required_exp": 1429374, "cumulative_exp": 22264666},
    {"level": 92, "required_exp": 1522283, "cumulative_exp": 23786949},
    {"level": 93, "required_exp": 1621231, "cumulative_exp": 25408180},
    {"level": 94, "required_exp": 1726611, "cumulative_exp": 27134791},
    {"level": 95, "required_exp": 1838840, "cumulative_exp": 28973631},
    {"level": 96, "required_exp": 1958364, "cumulative_exp": 30931995},
    {"level": 97, "required_exp": 2085657, "cumulative_exp": 33017652},
    {"level": 98, "required_exp": 2221224, "cumulative_exp": 35238876},
    {"level": 99, "required_exp": 2365603, "cumulative_exp": 37604479},
    {"level": 100, "required_exp": 2365603, "cumulative_exp": 39970082},
    {"level": 101, "required_exp": 2365603, "cumulative_exp": 42335685},
    {"level": 102, "required_exp": 2365603, "cumulative_exp": 44701288},
    {"level": 103, "required_exp": 2365603, "cumulative_exp": 47066891},
    {"level": 104, "required_exp": 2365603, "cumulative_exp": 49432494},
    {"level": 105, "required_exp": 2519367, "cumulative_exp": 51951861},
    {"level": 106, "required_exp": 2683125, "cumulative_exp": 54634986},
    {"level": 107, "required_exp": 2857528, "cumulative_exp": 57492514},
    {"level": 108, "required_exp": 3043267, "cumulative_exp": 60535781},
    {"level": 109, "required_exp": 3241079, "cumulative_exp": 63776860},
    {"level": 110, "required_exp": 3451749, "cumulative_exp": 67228609},
    {"level": 111, "required_exp": 3676112, "cumulative_exp": 70904721},
    {"level": 112, "required_exp": 3915059, "cumulative_exp": 74819780},
    {"level": 113, "required_exp": 4169537, "cumulative_exp": 78989317},
    {"level": 114, "required_exp": 4440556, "cumulative_exp": 83429873},
    {"level": 115, "required_exp": 4729192, "cumulative_exp": 88159065},
    {"level": 116, "required_exp": 5036589, "cumulative_exp": 93195654},
    {"level": 117, "required_exp": 5363967, "cumulative_exp": 98559621},
    {"level": 118, "required_exp": 5712624, "cumulative_exp": 104272245},
    {"level": 119, "required_exp": 6083944, "cumulative_exp": 110356189},
    {"level": 120, "required_exp": 6479400, "cumulative_exp": 116835589},
    {"level": 121, "required_exp": 6900561, "cumulative_exp": 123736150},
    {"level": 122, "required_exp": 7349097, "cumulative_exp": 131085247},
    {"level": 123, "required_exp": 7826788, "cumulative_exp": 138912035},
    {"level": 124, "required_exp": 8335529, "cumulative_exp": 147247564},
    {"level": 125, "required_exp": 8877338, "cumulative_exp": 156124902},
    {"level": 126, "required_exp": 9454364, "cumulative_exp": 165579266},
    {"level": 127, "required_exp": 10068897, "cumulative_exp": 175648163},
    {"level": 128, "required_exp": 10723375, "cumulative_exp": 186371538},
    {"level": 129, "required_exp": 11420394, "cumulative_exp": 197791932},
    {"level": 130, "required_exp": 12162719, "cumulative_exp": 209954651},
    {"level": 131, "required_exp": 12953295, "cumulative_exp": 222907946},
    {"level": 132, "required_exp": 13795259, "cumulative_exp": 236703205},
    {"level": 133, "required_exp": 14691950, "cumulative_exp": 251395155},
    {"level": 134, "required_exp": 15646926, "cumulative_exp": 267042081},
    {"level": 135, "required_exp": 16663976, "cumulative_exp": 283706057},
    {"level": 136, "required_exp": 17747134, "cumulative_exp": 301453191},
    {"level": 137, "required_exp": 18900697, "cumulative_exp": 320353888},
    {"level": 138, "required_exp": 20129242, "cumulative_exp": 340483130},
    {"level": 139, "required_exp": 21437642, "cumulative_exp": 361920772},
    {"level": 140, "required_exp": 22777494, "cumulative_exp": 384698266},
    {"level": 141, "required_exp": 24201087, "cumulative_exp": 408899353},
    {"level": 142, "required_exp": 25713654, "cumulative_exp": 434613007},
    {"level": 143, "required_exp": 27320757, "cumulative_exp": 461933764},
    {"level": 144, "required_exp": 29028304, "cumulative_exp": 490962068},
    {"level": 145, "required_exp": 30842573, "cumulative_exp": 521804641},
    {"level": 146, "required_exp": 32770233, "cumulative_exp": 554574874},
    {"level": 147, "required_exp": 34818372, "cumulative_exp": 589393246},
    {"level": 148, "required_exp": 36994520, "cumulative_exp": 626387766},
    {"level": 149, "required_exp": 39306677, "cumulative_exp": 665694443},
    {"level": 150, "required_exp": 41763344, "cumulative_exp": 707457787},
    {"level": 151, "required_exp": 44373553, "cumulative_exp": 751831340},
    {"level": 152, "required_exp": 47146900, "cumulative_exp": 798978240},
    {"level": 153, "required_exp": 50093581, "cumulative_exp": 849071821},
    {"level": 154, "required_exp": 53224429, "cumulative_exp": 902296250},
    {"level": 155, "required_exp": 56550955, "cumulative_exp": 958847205},
    {"level": 156, "required_exp": 60085389, "cumulative_exp": 1018932594},
    {"level": 157, "required_exp": 63840725, "cumulative_exp": 1082773319},
    {"level": 158, "required_exp": 67830770, "cumulative_exp": 1150604089},
    {"level": 159, "required_exp": 72070193, "cumulative_exp": 1222674282},
    {"level": 160, "required_exp": 76574580, "cumulative_exp": 1299248862},
    {"level": 161, "required_exp": 81360491, "cumulative_exp": 1380609353},
    {"level": 162, "required_exp": 86445521, "cumulative_exp": 1467054874},
    {"level": 163, "required_exp": 91848366, "cumulative_exp": 1558903240},
    {"level": 164, "required_exp": 97588888, "cumulative_exp": 1656492128},
    {"level": 165, "required_exp": 103688193, "cumulative_exp": 1760180321},
    {"level": 166, "required_exp": 110168705, "cumulative_exp": 1870349026},
    {"level": 167, "required_exp": 117054249, "cumulative_exp": 1987403275},
    {"level": 168, "required_exp": 124370139, "cumulative_exp": 2111773414},
    {"level": 169, "required_exp": 132143272, "cumulative_exp": 2243916686},
    {"level": 170, "required_exp": 138750435, "cumulative_exp": 2382667121},
    {"level": 171, "required_exp": 145687956, "cumulative_exp": 2528355077},
    {"level": 172, "required_exp": 152972353, "cumulative_exp": 2681327430},
    {"level": 173, "required_exp": 160620970, "cumulative_exp": 2841948400},
    {"level": 174, "required_exp": 168652018, "cumulative_exp": 3010600418},
    {"level": 175, "required_exp": 177084618, "cumulative_exp": 3187685036},
    {"level": 176, "required_exp": 185938848, "cumulative_exp": 3373623884},
    {"level": 177, "required_exp": 195235790, "cumulative_exp": 3568859674},
    {"level": 178, "required_exp": 204997579, "cumulative_exp": 3773857253},
    {"level": 179, "required_exp": 215247457, "cumulative_exp": 3989104710},
    {"level": 180, "required_exp": 226009829, "cumulative_exp": 4215114539},
    {"level": 181, "required_exp": 237310320, "cumulative_exp": 4452424859},
    {"level": 182, "required_exp": 249175836, "cumulative_exp": 4701600695},
    {"level": 183, "required_exp": 261634627, "cumulative_exp": 4963235322},
    {"level": 184, "required_exp": 274716358, "cumulative_exp": 5237951680},
    {"level": 185, "required_exp": 288452175, "cumulative_exp": 5526403855},
    {"level": 186, "required_exp": 302874783, "cumulative_exp": 5829278638},
    {"level": 187, "required_exp": 318018522, "cumulative_exp": 6147297160},
    {"level": 188, "required_exp": 333919448, "cumulative_exp": 6481216608},
    {"level": 189, "required_exp": 350615420, "cumulative_exp": 6831832028},
    {"level": 190, "required_exp": 368146191, "cumulative_exp": 7199978219},
    {"level": 191, "required_exp": 386553500, "cumulative_exp": 7586531719},
    {"level": 192, "required_exp": 405881175, "cumulative_exp": 7992412894},
    {"level": 193, "required_exp": 426175233, "cumulative_exp": 8418588127},
    {"level": 194, "required_exp": 447483994, "cumulative_exp": 8866072121},
    {"level": 195, "required_exp": 469858193, "cumulative_exp": 9335930314},
    {"level": 196, "required_exp": 493351102, "cumulative_exp": 9829281416},
    {"level": 197, "required_exp": 518018657, "cumulative_exp": 10347300073},
    {"level": 198, "required_exp": 543919589, "cumulative_exp": 10891219662},
    {"level": 199, "required_exp": 571115568, "cumulative_exp": 11462335230},
    {"level": 200, "required_exp": 2207026470, "cumulative_exp": 13669361700},
    {"level": 201, "required_exp": 2471869646, "cumulative_exp": 16141231346},
    {"level": 202, "required_exp": 2768494003, "cumulative_exp": 18909725349},
    {"level": 203, "required_exp": 3100713283, "cumulative_exp": 22010438632},
    {"level": 204, "required_exp": 3472798876, "cumulative_exp": 25483237508},
    {"level": 205, "required_exp": 3889534741, "cumulative_exp": 29372772249},
    {"level": 206, "required_exp": 4356278909, "cumulative_exp": 33729051158},
    {"level": 207, "required_exp": 4879032378, "cumulative_exp": 38608083536},
    {"level": 208, "required_exp": 5464516263, "cumulative_exp": 44072599799},
    {"level": 209, "required_exp": 6120258214, "cumulative_exp": 50192858013},
    {"level": 210, "required_exp": 7956335678, "cumulative_exp": 58149193691},
    {"level": 211, "required_exp": 8831532602, "cumulative_exp": 66980726293},
    {"level": 212, "required_exp": 9803001188, "cumulative_exp": 76783727481},
    {"level": 213, "required_exp": 10881331318, "cumulative_exp": 87665058799},
    {"level": 214, "required_exp": 12078277762, "cumulative_exp": 99743336561},
    {"level": 215, "required_exp": 15701761090, "cumulative_exp": 115445097651},
    {"level": 216, "required_exp": 17114919588, "cumulative_exp": 132560017239},
    {"level": 217, "required_exp": 18655262350, "cumulative_exp": 151215279589},
    {"level": 218, "required_exp": 20334235961, "cumulative_exp": 171549515550},
    {"level": 219, "required_exp": 22164317197, "cumulative_exp": 193713832747},
    {"level": 220, "required_exp": 28813612356, "cumulative_exp": 222527445103},
    {"level": 221, "required_exp": 30830565220, "cumulative_exp": 253358010323},
    {"level": 222, "required_exp": 32988704785, "cumulative_exp": 286346715108},
    {"level": 223, "required_exp": 35297914119, "cumulative_exp": 321644629227},
    {"level": 224, "required_exp": 37768768107, "cumulative_exp": 359413397334},
    {"level": 225, "required_exp": 49099398539, "cumulative_exp": 408512795873},
    {"level": 226, "required_exp": 52536356436, "cumulative_exp": 461049152309},
    {"level": 227, "required_exp": 56213901386, "cumulative_exp": 517263053695},
    {"level": 228, "required_exp": 60148874483, "cumulative_exp": 577411928178},
    {"level": 229, "required_exp": 64359295696, "cumulative_exp": 641771223874},
    {"level": 230, "required_exp": 83667084404, "cumulative_exp": 725438308278},
    {"level": 231, "required_exp": 86177096936, "cumulative_exp": 811615405214},
    {"level": 232, "required_exp": 88762409844, "cumulative_exp": 900377815058},
    {"level": 233, "required_exp": 91425282139, "cumulative_exp": 991803097197},
    {"level": 234, "required_exp": 94168040603, "cumulative_exp": 1085971137800},
    {"level": 235, "required_exp": 122418452783, "cumulative_exp": 1208389590583},
    {"level": 236, "required_exp": 126091006366, "cumulative_exp": 1334480596949},
    {"level": 237, "required_exp": 129873736556, "cumulative_exp": 1464354333505},
    {"level": 238, "required_exp": 133769948652, "cumulative_exp": 1598124282157},
    {"level": 239, "required_exp": 137783047111, "cumulative_exp": 1735907329268},
    {"level": 240, "required_exp": 179117961244, "cumulative_exp": 1915025290512},
    {"level": 241, "required_exp": 184491500081, "cumulative_exp": 2099516790593},
    {"level": 242, "required_exp": 190026245083, "cumulative_exp": 2289543035676},
    {"level": 243, "required_exp": 195727032435, "cumulative_exp": 2485270068111},
    {"level": 244, "required_exp": 201598843408, "cumulative_exp": 2686868911519},
    {"level": 245, "required_exp": 262078496430, "cumulative_exp": 2948947407949},
    {"level": 246, "required_exp": 269940851322, "cumulative_exp": 3218888259271},
    {"level": 247, "required_exp": 278039076861, "cumulative_exp": 3496927336132},
    {"level": 248, "required_exp": 286380249166, "cumulative_exp": 3783307585298},
    {"level": 249, "required_exp": 294971656640, "cumulative_exp": 4078279241938},
    {"level": 250, "required_exp": 442457484960, "cumulative_exp": 4520736726898},
    {"level": 251, "required_exp": 455731209508, "cumulative_exp": 4976467936406},
    {"level": 252, "required_exp": 469403145793, "cumulative_exp": 5445871082199},
    {"level": 253, "required_exp": 483485240166, "cumulative_exp": 5929356322365},
    {"level": 254, "required_exp": 497989797370, "cumulative_exp": 6427346119735},
    {"level": 255, "required_exp": 512929491291, "cumulative_exp": 6940275611026},
    {"level": 256, "required_exp": 528317376029, "cumulative_exp": 7468592987055},
    {"level": 257, "required_exp": 544166897309, "cumulative_exp": 8012759884364},
    {"level": 258, "required_exp": 560491904228, "cumulative_exp": 8573251788592},
    {"level": 259, "required_exp": 577306661354, "cumulative_exp": 9150558449946},
    {"level": 260, "required_exp": 1731919984062, "cumulative_exp": 10882478434008},
    {"level": 261, "required_exp": 1749239183902, "cumulative_exp": 12631717617910},
    {"level": 262, "required_exp": 1766731575741, "cumulative_exp": 14398449193651},
    {"level": 263, "required_exp": 1784398891498, "cumulative_exp": 16182848085149},
    {"level": 264, "required_exp": 1802242880412, "cumulative_exp": 17985090965561},
    {"level": 265, "required_exp": 2342915744535, "cumulative_exp": 20328006710096},
    {"level": 266, "required_exp": 2366344901980, "cumulative_exp": 22694351612076},
    {"level": 267, "required_exp": 2390008350999, "cumulative_exp": 25084359963075},
    {"level": 268, "required_exp": 2413908434508, "cumulative_exp": 27498268397583},
    {"level": 269, "required_exp": 2438047518853, "cumulative_exp": 29936315916436},
    {"level": 270, "required_exp": 5412465491853, "cumulative_exp": 35348781408289},
    {"level": 271, "required_exp": 5466590146771, "cumulative_exp": 40815371555060},
    {"level": 272, "required_exp": 5521256048238, "cumulative_exp": 46336627603298},
    {"level": 273, "required_exp": 5576468608720, "cumulative_exp": 51913096212018},
    {"level": 274, "required_exp": 5632233294807, "cumulative_exp": 57545329506825},
    {"level": 275, "required_exp": 11377111255510, "cumulative_exp": 68922440762335},
    {"level": 276, "required_exp": 12514822381061, "cumulative_exp": 81437263143396},
    {"level": 277, "required_exp": 13766304619167, "cumulative_exp": 95203567762563},
    {"level": 278, "required_exp": 15142935081083, "cumulative_exp": 110346502843646},
    {"level": 279, "required_exp": 16657228589191, "cumulative_exp": 127003731432837},
    {"level": 280, "required_exp": 33647601750165, "cumulative_exp": 160651333183002},
    {"level": 281, "required_exp": 37012361925181, "cumulative_exp": 197663695108183},
    {"level": 282, "required_exp": 40713598117699, "cumulative_exp": 238377293225882},
    {"level": 283, "required_exp": 44784957929468, "cumulative_exp": 283162251155350},
    {"level": 284, "required_exp": 49263453722414, "cumulative_exp": 332425704877764},
    {"level": 285, "required_exp": 99512176519276, "cumulative_exp": 431937881397040},
    {"level": 286, "required_exp": 109463394171203, "cumulative_exp": 541401275568243},
    {"level": 287, "required_exp": 120409733588323, "cumulative_exp": 661811009156566},
    {"level": 288, "required_exp": 132450706947155, "cumulative_exp": 794261716103721},
    {"level": 289, "required_exp": 145695777641870, "cumulative_exp": 939957493745591},
    {"level": 290, "required_exp": 294305470836577, "cumulative_exp": 1234262964582168},
    {"level": 291, "required_exp": 323736017920234, "cumulative_exp": 1557998982502402},
    {"level": 292, "required_exp": 356109619712257, "cumulative_exp": 1914108602214659},
    {"level": 293, "required_exp": 391720581683482, "cumulative_exp": 2305829183898141},
    {"level": 294, "required_exp": 430892639851830, "cumulative_exp": 2736721823749971},
    {"level": 295, "required_exp": 870403132500696, "cumulative_exp": 3607124956250667},
    {"level": 296, "required_exp": 957443445750765, "cumulative_exp": 4564568402001432},
    {
        "level": 297,
        "required_exp": 1053187790325841,
        "cumulative_exp": 5617756192327273,
    },
    {
        "level": 298,
        "required_exp": 1158506569358425,
        "cumulative_exp": 6776262761685698,
    },
    {
        "level": 299,
        "required_exp": 1737759854037637,
        "cumulative_exp": 8514022615723335,
    },
]

# LEVEL_1 = (0, 0)
# LEVEL_2 = (1, 1)
# LEVEL_3 = (2, 3)
# LEVEL_4 = (2, 5)
# LEVEL_5 = (3, 8)

# for exp in exp_table:
#     print(f"LEVEL_{exp['level']} = ({exp['required_exp']:,} / {exp['cumulative_exp']:,})")

new_exp_table = [
    {"level": 0, "required_exp": 0, "cumulative_exp": 0},
    {"level": 1, "required_exp": 15, "cumulative_exp": 0},
]
for i, exp in enumerate(exp_table[1:]):
    prev_exp = exp_table[i]
    new_exp_table.append(
        {
            "level": exp["level"],
            "required_exp": exp["required_exp"],
            "cumulative_exp": prev_exp["cumulative_exp"],
        }
    )
new_exp_table.append(
    {
        "level": 300,
        "required_exp": 0,
        "cumulative_exp": 8514022615723335,
    }
)
print(new_exp_table)

new_exp_table2 = [
    {"level": 0, "required_exp": 0, "cumulative_exp": 0},
    {"level": 1, "required_exp": 15, "cumulative_exp": 0},
    {"level": 2, "required_exp": 34, "cumulative_exp": 15},
    {"level": 3, "required_exp": 57, "cumulative_exp": 49},
    {"level": 4, "required_exp": 92, "cumulative_exp": 106},
    {"level": 5, "required_exp": 135, "cumulative_exp": 198},
    {"level": 6, "required_exp": 372, "cumulative_exp": 333},
    {"level": 7, "required_exp": 560, "cumulative_exp": 705},
    {"level": 8, "required_exp": 840, "cumulative_exp": 1265},
    {"level": 9, "required_exp": 1242, "cumulative_exp": 2105},
    {"level": 10, "required_exp": 1242, "cumulative_exp": 3347},
    {"level": 11, "required_exp": 1242, "cumulative_exp": 4589},
    {"level": 12, "required_exp": 1242, "cumulative_exp": 5831},
    {"level": 13, "required_exp": 1242, "cumulative_exp": 7073},
    {"level": 14, "required_exp": 1242, "cumulative_exp": 8315},
    {"level": 15, "required_exp": 1490, "cumulative_exp": 9557},
    {"level": 16, "required_exp": 1788, "cumulative_exp": 11047},
    {"level": 17, "required_exp": 2145, "cumulative_exp": 12835},
    {"level": 18, "required_exp": 2574, "cumulative_exp": 14980},
    {"level": 19, "required_exp": 3088, "cumulative_exp": 17554},
    {"level": 20, "required_exp": 3705, "cumulative_exp": 20642},
    {"level": 21, "required_exp": 4446, "cumulative_exp": 24347},
    {"level": 22, "required_exp": 5335, "cumulative_exp": 28793},
    {"level": 23, "required_exp": 6402, "cumulative_exp": 34128},
    {"level": 24, "required_exp": 7682, "cumulative_exp": 40530},
    {"level": 25, "required_exp": 9218, "cumulative_exp": 48212},
    {"level": 26, "required_exp": 11061, "cumulative_exp": 57430},
    {"level": 27, "required_exp": 13273, "cumulative_exp": 68491},
    {"level": 28, "required_exp": 15927, "cumulative_exp": 81764},
    {"level": 29, "required_exp": 19112, "cumulative_exp": 97691},
    {"level": 30, "required_exp": 19112, "cumulative_exp": 116803},
    {"level": 31, "required_exp": 19112, "cumulative_exp": 135915},
    {"level": 32, "required_exp": 19112, "cumulative_exp": 155027},
    {"level": 33, "required_exp": 19112, "cumulative_exp": 174139},
    {"level": 34, "required_exp": 19112, "cumulative_exp": 193251},
    {"level": 35, "required_exp": 22934, "cumulative_exp": 212363},
    {"level": 36, "required_exp": 27520, "cumulative_exp": 235297},
    {"level": 37, "required_exp": 33024, "cumulative_exp": 262817},
    {"level": 38, "required_exp": 39628, "cumulative_exp": 295841},
    {"level": 39, "required_exp": 47553, "cumulative_exp": 335469},
    {"level": 40, "required_exp": 51357, "cumulative_exp": 383022},
    {"level": 41, "required_exp": 55465, "cumulative_exp": 434379},
    {"level": 42, "required_exp": 59902, "cumulative_exp": 489844},
    {"level": 43, "required_exp": 64694, "cumulative_exp": 549746},
    {"level": 44, "required_exp": 69869, "cumulative_exp": 614440},
    {"level": 45, "required_exp": 75458, "cumulative_exp": 684309},
    {"level": 46, "required_exp": 81494, "cumulative_exp": 759767},
    {"level": 47, "required_exp": 88013, "cumulative_exp": 841261},
    {"level": 48, "required_exp": 95054, "cumulative_exp": 929274},
    {"level": 49, "required_exp": 102658, "cumulative_exp": 1024328},
    {"level": 50, "required_exp": 110870, "cumulative_exp": 1126986},
    {"level": 51, "required_exp": 119739, "cumulative_exp": 1237856},
    {"level": 52, "required_exp": 129318, "cumulative_exp": 1357595},
    {"level": 53, "required_exp": 139663, "cumulative_exp": 1486913},
    {"level": 54, "required_exp": 150836, "cumulative_exp": 1626576},
    {"level": 55, "required_exp": 162902, "cumulative_exp": 1777412},
    {"level": 56, "required_exp": 175934, "cumulative_exp": 1940314},
    {"level": 57, "required_exp": 190008, "cumulative_exp": 2116248},
    {"level": 58, "required_exp": 205208, "cumulative_exp": 2306256},
    {"level": 59, "required_exp": 221624, "cumulative_exp": 2511464},
    {"level": 60, "required_exp": 221624, "cumulative_exp": 2733088},
    {"level": 61, "required_exp": 221624, "cumulative_exp": 2954712},
    {"level": 62, "required_exp": 221624, "cumulative_exp": 3176336},
    {"level": 63, "required_exp": 221624, "cumulative_exp": 3397960},
    {"level": 64, "required_exp": 221624, "cumulative_exp": 3619584},
    {"level": 65, "required_exp": 238245, "cumulative_exp": 3841208},
    {"level": 66, "required_exp": 256113, "cumulative_exp": 4079453},
    {"level": 67, "required_exp": 275321, "cumulative_exp": 4335566},
    {"level": 68, "required_exp": 295970, "cumulative_exp": 4610887},
    {"level": 69, "required_exp": 318167, "cumulative_exp": 4906857},
    {"level": 70, "required_exp": 342029, "cumulative_exp": 5225024},
    {"level": 71, "required_exp": 367681, "cumulative_exp": 5567053},
    {"level": 72, "required_exp": 395257, "cumulative_exp": 5934734},
    {"level": 73, "required_exp": 424901, "cumulative_exp": 6329991},
    {"level": 74, "required_exp": 456768, "cumulative_exp": 6754892},
    {"level": 75, "required_exp": 488741, "cumulative_exp": 7211660},
    {"level": 76, "required_exp": 522952, "cumulative_exp": 7700401},
    {"level": 77, "required_exp": 559558, "cumulative_exp": 8223353},
    {"level": 78, "required_exp": 598727, "cumulative_exp": 8782911},
    {"level": 79, "required_exp": 640637, "cumulative_exp": 9381638},
    {"level": 80, "required_exp": 685481, "cumulative_exp": 10022275},
    {"level": 81, "required_exp": 733464, "cumulative_exp": 10707756},
    {"level": 82, "required_exp": 784806, "cumulative_exp": 11441220},
    {"level": 83, "required_exp": 839742, "cumulative_exp": 12226026},
    {"level": 84, "required_exp": 898523, "cumulative_exp": 13065768},
    {"level": 85, "required_exp": 961419, "cumulative_exp": 13964291},
    {"level": 86, "required_exp": 1028718, "cumulative_exp": 14925710},
    {"level": 87, "required_exp": 1100728, "cumulative_exp": 15954428},
    {"level": 88, "required_exp": 1177778, "cumulative_exp": 17055156},
    {"level": 89, "required_exp": 1260222, "cumulative_exp": 18232934},
    {"level": 90, "required_exp": 1342136, "cumulative_exp": 19493156},
    {"level": 91, "required_exp": 1429374, "cumulative_exp": 20835292},
    {"level": 92, "required_exp": 1522283, "cumulative_exp": 22264666},
    {"level": 93, "required_exp": 1621231, "cumulative_exp": 23786949},
    {"level": 94, "required_exp": 1726611, "cumulative_exp": 25408180},
    {"level": 95, "required_exp": 1838840, "cumulative_exp": 27134791},
    {"level": 96, "required_exp": 1958364, "cumulative_exp": 28973631},
    {"level": 97, "required_exp": 2085657, "cumulative_exp": 30931995},
    {"level": 98, "required_exp": 2221224, "cumulative_exp": 33017652},
    {"level": 99, "required_exp": 2365603, "cumulative_exp": 35238876},
    {"level": 100, "required_exp": 2365603, "cumulative_exp": 37604479},
    {"level": 101, "required_exp": 2365603, "cumulative_exp": 39970082},
    {"level": 102, "required_exp": 2365603, "cumulative_exp": 42335685},
    {"level": 103, "required_exp": 2365603, "cumulative_exp": 44701288},
    {"level": 104, "required_exp": 2365603, "cumulative_exp": 47066891},
    {"level": 105, "required_exp": 2519367, "cumulative_exp": 49432494},
    {"level": 106, "required_exp": 2683125, "cumulative_exp": 51951861},
    {"level": 107, "required_exp": 2857528, "cumulative_exp": 54634986},
    {"level": 108, "required_exp": 3043267, "cumulative_exp": 57492514},
    {"level": 109, "required_exp": 3241079, "cumulative_exp": 60535781},
    {"level": 110, "required_exp": 3451749, "cumulative_exp": 63776860},
    {"level": 111, "required_exp": 3676112, "cumulative_exp": 67228609},
    {"level": 112, "required_exp": 3915059, "cumulative_exp": 70904721},
    {"level": 113, "required_exp": 4169537, "cumulative_exp": 74819780},
    {"level": 114, "required_exp": 4440556, "cumulative_exp": 78989317},
    {"level": 115, "required_exp": 4729192, "cumulative_exp": 83429873},
    {"level": 116, "required_exp": 5036589, "cumulative_exp": 88159065},
    {"level": 117, "required_exp": 5363967, "cumulative_exp": 93195654},
    {"level": 118, "required_exp": 5712624, "cumulative_exp": 98559621},
    {"level": 119, "required_exp": 6083944, "cumulative_exp": 104272245},
    {"level": 120, "required_exp": 6479400, "cumulative_exp": 110356189},
    {"level": 121, "required_exp": 6900561, "cumulative_exp": 116835589},
    {"level": 122, "required_exp": 7349097, "cumulative_exp": 123736150},
    {"level": 123, "required_exp": 7826788, "cumulative_exp": 131085247},
    {"level": 124, "required_exp": 8335529, "cumulative_exp": 138912035},
    {"level": 125, "required_exp": 8877338, "cumulative_exp": 147247564},
    {"level": 126, "required_exp": 9454364, "cumulative_exp": 156124902},
    {"level": 127, "required_exp": 10068897, "cumulative_exp": 165579266},
    {"level": 128, "required_exp": 10723375, "cumulative_exp": 175648163},
    {"level": 129, "required_exp": 11420394, "cumulative_exp": 186371538},
    {"level": 130, "required_exp": 12162719, "cumulative_exp": 197791932},
    {"level": 131, "required_exp": 12953295, "cumulative_exp": 209954651},
    {"level": 132, "required_exp": 13795259, "cumulative_exp": 222907946},
    {"level": 133, "required_exp": 14691950, "cumulative_exp": 236703205},
    {"level": 134, "required_exp": 15646926, "cumulative_exp": 251395155},
    {"level": 135, "required_exp": 16663976, "cumulative_exp": 267042081},
    {"level": 136, "required_exp": 17747134, "cumulative_exp": 283706057},
    {"level": 137, "required_exp": 18900697, "cumulative_exp": 301453191},
    {"level": 138, "required_exp": 20129242, "cumulative_exp": 320353888},
    {"level": 139, "required_exp": 21437642, "cumulative_exp": 340483130},
    {"level": 140, "required_exp": 22777494, "cumulative_exp": 361920772},
    {"level": 141, "required_exp": 24201087, "cumulative_exp": 384698266},
    {"level": 142, "required_exp": 25713654, "cumulative_exp": 408899353},
    {"level": 143, "required_exp": 27320757, "cumulative_exp": 434613007},
    {"level": 144, "required_exp": 29028304, "cumulative_exp": 461933764},
    {"level": 145, "required_exp": 30842573, "cumulative_exp": 490962068},
    {"level": 146, "required_exp": 32770233, "cumulative_exp": 521804641},
    {"level": 147, "required_exp": 34818372, "cumulative_exp": 554574874},
    {"level": 148, "required_exp": 36994520, "cumulative_exp": 589393246},
    {"level": 149, "required_exp": 39306677, "cumulative_exp": 626387766},
    {"level": 150, "required_exp": 41763344, "cumulative_exp": 665694443},
    {"level": 151, "required_exp": 44373553, "cumulative_exp": 707457787},
    {"level": 152, "required_exp": 47146900, "cumulative_exp": 751831340},
    {"level": 153, "required_exp": 50093581, "cumulative_exp": 798978240},
    {"level": 154, "required_exp": 53224429, "cumulative_exp": 849071821},
    {"level": 155, "required_exp": 56550955, "cumulative_exp": 902296250},
    {"level": 156, "required_exp": 60085389, "cumulative_exp": 958847205},
    {"level": 157, "required_exp": 63840725, "cumulative_exp": 1018932594},
    {"level": 158, "required_exp": 67830770, "cumulative_exp": 1082773319},
    {"level": 159, "required_exp": 72070193, "cumulative_exp": 1150604089},
    {"level": 160, "required_exp": 76574580, "cumulative_exp": 1222674282},
    {"level": 161, "required_exp": 81360491, "cumulative_exp": 1299248862},
    {"level": 162, "required_exp": 86445521, "cumulative_exp": 1380609353},
    {"level": 163, "required_exp": 91848366, "cumulative_exp": 1467054874},
    {"level": 164, "required_exp": 97588888, "cumulative_exp": 1558903240},
    {"level": 165, "required_exp": 103688193, "cumulative_exp": 1656492128},
    {"level": 166, "required_exp": 110168705, "cumulative_exp": 1760180321},
    {"level": 167, "required_exp": 117054249, "cumulative_exp": 1870349026},
    {"level": 168, "required_exp": 124370139, "cumulative_exp": 1987403275},
    {"level": 169, "required_exp": 132143272, "cumulative_exp": 2111773414},
    {"level": 170, "required_exp": 138750435, "cumulative_exp": 2243916686},
    {"level": 171, "required_exp": 145687956, "cumulative_exp": 2382667121},
    {"level": 172, "required_exp": 152972353, "cumulative_exp": 2528355077},
    {"level": 173, "required_exp": 160620970, "cumulative_exp": 2681327430},
    {"level": 174, "required_exp": 168652018, "cumulative_exp": 2841948400},
    {"level": 175, "required_exp": 177084618, "cumulative_exp": 3010600418},
    {"level": 176, "required_exp": 185938848, "cumulative_exp": 3187685036},
    {"level": 177, "required_exp": 195235790, "cumulative_exp": 3373623884},
    {"level": 178, "required_exp": 204997579, "cumulative_exp": 3568859674},
    {"level": 179, "required_exp": 215247457, "cumulative_exp": 3773857253},
    {"level": 180, "required_exp": 226009829, "cumulative_exp": 3989104710},
    {"level": 181, "required_exp": 237310320, "cumulative_exp": 4215114539},
    {"level": 182, "required_exp": 249175836, "cumulative_exp": 4452424859},
    {"level": 183, "required_exp": 261634627, "cumulative_exp": 4701600695},
    {"level": 184, "required_exp": 274716358, "cumulative_exp": 4963235322},
    {"level": 185, "required_exp": 288452175, "cumulative_exp": 5237951680},
    {"level": 186, "required_exp": 302874783, "cumulative_exp": 5526403855},
    {"level": 187, "required_exp": 318018522, "cumulative_exp": 5829278638},
    {"level": 188, "required_exp": 333919448, "cumulative_exp": 6147297160},
    {"level": 189, "required_exp": 350615420, "cumulative_exp": 6481216608},
    {"level": 190, "required_exp": 368146191, "cumulative_exp": 6831832028},
    {"level": 191, "required_exp": 386553500, "cumulative_exp": 7199978219},
    {"level": 192, "required_exp": 405881175, "cumulative_exp": 7586531719},
    {"level": 193, "required_exp": 426175233, "cumulative_exp": 7992412894},
    {"level": 194, "required_exp": 447483994, "cumulative_exp": 8418588127},
    {"level": 195, "required_exp": 469858193, "cumulative_exp": 8866072121},
    {"level": 196, "required_exp": 493351102, "cumulative_exp": 9335930314},
    {"level": 197, "required_exp": 518018657, "cumulative_exp": 9829281416},
    {"level": 198, "required_exp": 543919589, "cumulative_exp": 10347300073},
    {"level": 199, "required_exp": 571115568, "cumulative_exp": 10891219662},
    {"level": 200, "required_exp": 2207026470, "cumulative_exp": 11462335230},
    {"level": 201, "required_exp": 2471869646, "cumulative_exp": 13669361700},
    {"level": 202, "required_exp": 2768494003, "cumulative_exp": 16141231346},
    {"level": 203, "required_exp": 3100713283, "cumulative_exp": 18909725349},
    {"level": 204, "required_exp": 3472798876, "cumulative_exp": 22010438632},
    {"level": 205, "required_exp": 3889534741, "cumulative_exp": 25483237508},
    {"level": 206, "required_exp": 4356278909, "cumulative_exp": 29372772249},
    {"level": 207, "required_exp": 4879032378, "cumulative_exp": 33729051158},
    {"level": 208, "required_exp": 5464516263, "cumulative_exp": 38608083536},
    {"level": 209, "required_exp": 6120258214, "cumulative_exp": 44072599799},
    {"level": 210, "required_exp": 7956335678, "cumulative_exp": 50192858013},
    {"level": 211, "required_exp": 8831532602, "cumulative_exp": 58149193691},
    {"level": 212, "required_exp": 9803001188, "cumulative_exp": 66980726293},
    {"level": 213, "required_exp": 10881331318, "cumulative_exp": 76783727481},
    {"level": 214, "required_exp": 12078277762, "cumulative_exp": 87665058799},
    {"level": 215, "required_exp": 15701761090, "cumulative_exp": 99743336561},
    {"level": 216, "required_exp": 17114919588, "cumulative_exp": 115445097651},
    {"level": 217, "required_exp": 18655262350, "cumulative_exp": 132560017239},
    {"level": 218, "required_exp": 20334235961, "cumulative_exp": 151215279589},
    {"level": 219, "required_exp": 22164317197, "cumulative_exp": 171549515550},
    {"level": 220, "required_exp": 28813612356, "cumulative_exp": 193713832747},
    {"level": 221, "required_exp": 30830565220, "cumulative_exp": 222527445103},
    {"level": 222, "required_exp": 32988704785, "cumulative_exp": 253358010323},
    {"level": 223, "required_exp": 35297914119, "cumulative_exp": 286346715108},
    {"level": 224, "required_exp": 37768768107, "cumulative_exp": 321644629227},
    {"level": 225, "required_exp": 49099398539, "cumulative_exp": 359413397334},
    {"level": 226, "required_exp": 52536356436, "cumulative_exp": 408512795873},
    {"level": 227, "required_exp": 56213901386, "cumulative_exp": 461049152309},
    {"level": 228, "required_exp": 60148874483, "cumulative_exp": 517263053695},
    {"level": 229, "required_exp": 64359295696, "cumulative_exp": 577411928178},
    {"level": 230, "required_exp": 83667084404, "cumulative_exp": 641771223874},
    {"level": 231, "required_exp": 86177096936, "cumulative_exp": 725438308278},
    {"level": 232, "required_exp": 88762409844, "cumulative_exp": 811615405214},
    {"level": 233, "required_exp": 91425282139, "cumulative_exp": 900377815058},
    {"level": 234, "required_exp": 94168040603, "cumulative_exp": 991803097197},
    {"level": 235, "required_exp": 122418452783, "cumulative_exp": 1085971137800},
    {"level": 236, "required_exp": 126091006366, "cumulative_exp": 1208389590583},
    {"level": 237, "required_exp": 129873736556, "cumulative_exp": 1334480596949},
    {"level": 238, "required_exp": 133769948652, "cumulative_exp": 1464354333505},
    {"level": 239, "required_exp": 137783047111, "cumulative_exp": 1598124282157},
    {"level": 240, "required_exp": 179117961244, "cumulative_exp": 1735907329268},
    {"level": 241, "required_exp": 184491500081, "cumulative_exp": 1915025290512},
    {"level": 242, "required_exp": 190026245083, "cumulative_exp": 2099516790593},
    {"level": 243, "required_exp": 195727032435, "cumulative_exp": 2289543035676},
    {"level": 244, "required_exp": 201598843408, "cumulative_exp": 2485270068111},
    {"level": 245, "required_exp": 262078496430, "cumulative_exp": 2686868911519},
    {"level": 246, "required_exp": 269940851322, "cumulative_exp": 2948947407949},
    {"level": 247, "required_exp": 278039076861, "cumulative_exp": 3218888259271},
    {"level": 248, "required_exp": 286380249166, "cumulative_exp": 3496927336132},
    {"level": 249, "required_exp": 294971656640, "cumulative_exp": 3783307585298},
    {"level": 250, "required_exp": 442457484960, "cumulative_exp": 4078279241938},
    {"level": 251, "required_exp": 455731209508, "cumulative_exp": 4520736726898},
    {"level": 252, "required_exp": 469403145793, "cumulative_exp": 4976467936406},
    {"level": 253, "required_exp": 483485240166, "cumulative_exp": 5445871082199},
    {"level": 254, "required_exp": 497989797370, "cumulative_exp": 5929356322365},
    {"level": 255, "required_exp": 512929491291, "cumulative_exp": 6427346119735},
    {"level": 256, "required_exp": 528317376029, "cumulative_exp": 6940275611026},
    {"level": 257, "required_exp": 544166897309, "cumulative_exp": 7468592987055},
    {"level": 258, "required_exp": 560491904228, "cumulative_exp": 8012759884364},
    {"level": 259, "required_exp": 577306661354, "cumulative_exp": 8573251788592},
    {"level": 260, "required_exp": 1731919984062, "cumulative_exp": 9150558449946},
    {"level": 261, "required_exp": 1749239183902, "cumulative_exp": 10882478434008},
    {"level": 262, "required_exp": 1766731575741, "cumulative_exp": 12631717617910},
    {"level": 263, "required_exp": 1784398891498, "cumulative_exp": 14398449193651},
    {"level": 264, "required_exp": 1802242880412, "cumulative_exp": 16182848085149},
    {"level": 265, "required_exp": 2342915744535, "cumulative_exp": 17985090965561},
    {"level": 266, "required_exp": 2366344901980, "cumulative_exp": 20328006710096},
    {"level": 267, "required_exp": 2390008350999, "cumulative_exp": 22694351612076},
    {"level": 268, "required_exp": 2413908434508, "cumulative_exp": 25084359963075},
    {"level": 269, "required_exp": 2438047518853, "cumulative_exp": 27498268397583},
    {"level": 270, "required_exp": 5412465491853, "cumulative_exp": 29936315916436},
    {"level": 271, "required_exp": 5466590146771, "cumulative_exp": 35348781408289},
    {"level": 272, "required_exp": 5521256048238, "cumulative_exp": 40815371555060},
    {"level": 273, "required_exp": 5576468608720, "cumulative_exp": 46336627603298},
    {"level": 274, "required_exp": 5632233294807, "cumulative_exp": 51913096212018},
    {"level": 275, "required_exp": 11377111255510, "cumulative_exp": 57545329506825},
    {"level": 276, "required_exp": 12514822381061, "cumulative_exp": 68922440762335},
    {"level": 277, "required_exp": 13766304619167, "cumulative_exp": 81437263143396},
    {"level": 278, "required_exp": 15142935081083, "cumulative_exp": 95203567762563},
    {"level": 279, "required_exp": 16657228589191, "cumulative_exp": 110346502843646},
    {"level": 280, "required_exp": 33647601750165, "cumulative_exp": 127003731432837},
    {"level": 281, "required_exp": 37012361925181, "cumulative_exp": 160651333183002},
    {"level": 282, "required_exp": 40713598117699, "cumulative_exp": 197663695108183},
    {"level": 283, "required_exp": 44784957929468, "cumulative_exp": 238377293225882},
    {"level": 284, "required_exp": 49263453722414, "cumulative_exp": 283162251155350},
    {"level": 285, "required_exp": 99512176519276, "cumulative_exp": 332425704877764},
    {"level": 286, "required_exp": 109463394171203, "cumulative_exp": 431937881397040},
    {"level": 287, "required_exp": 120409733588323, "cumulative_exp": 541401275568243},
    {"level": 288, "required_exp": 132450706947155, "cumulative_exp": 661811009156566},
    {"level": 289, "required_exp": 145695777641870, "cumulative_exp": 794261716103721},
    {"level": 290, "required_exp": 294305470836577, "cumulative_exp": 939957493745591},
    {"level": 291, "required_exp": 323736017920234, "cumulative_exp": 1234262964582168},
    {"level": 292, "required_exp": 356109619712257, "cumulative_exp": 1557998982502402},
    {"level": 293, "required_exp": 391720581683482, "cumulative_exp": 1914108602214659},
    {"level": 294, "required_exp": 430892639851830, "cumulative_exp": 2305829183898141},
    {"level": 295, "required_exp": 870403132500696, "cumulative_exp": 2736721823749971},
    {"level": 296, "required_exp": 957443445750765, "cumulative_exp": 3607124956250667},
    {
        "level": 297,
        "required_exp": 1053187790325841,
        "cumulative_exp": 4564568402001432,
    },
    {
        "level": 298,
        "required_exp": 1158506569358425,
        "cumulative_exp": 5617756192327273,
    },
    {
        "level": 299,
        "required_exp": 1737759854037637,
        "cumulative_exp": 6776262761685698,
    },
    {"level": 300, "required_exp": 0, "cumulative_exp": 8514022615723335},
]


for exp in new_exp_table:
    print(
        f"LEVEL_{exp['level']} = ({exp['required_exp']:,} / {exp['cumulative_exp']:,})"
    )

LEVEL_0 = (0, 0)
LEVEL_1 = (15, 0)
LEVEL_2 = (34, 15)
LEVEL_3 = (57, 49)
LEVEL_4 = (92, 106)
LEVEL_5 = (135, 198)
LEVEL_6 = (372, 333)
LEVEL_7 = (560, 705)
LEVEL_8 = (840, 1_265)
LEVEL_9 = (1_242, 2_105)
LEVEL_10 = (1_242, 3_347)
LEVEL_11 = (1_242, 4_589)
LEVEL_12 = (1_242, 5_831)
LEVEL_13 = (1_242, 7_073)
LEVEL_14 = (1_242, 8_315)
LEVEL_15 = (1_490, 9_557)
LEVEL_16 = (1_788, 11_047)
LEVEL_17 = (2_145, 12_835)
LEVEL_18 = (2_574, 14_980)
LEVEL_19 = (3_088, 17_554)
LEVEL_20 = (3_705, 20_642)
LEVEL_21 = (4_446, 24_347)
LEVEL_22 = (5_335, 28_793)
LEVEL_23 = (6_402, 34_128)
LEVEL_24 = (7_682, 40_530)
LEVEL_25 = (9_218, 48_212)
LEVEL_26 = (11_061, 57_430)
LEVEL_27 = (13_273, 68_491)
LEVEL_28 = (15_927, 81_764)
LEVEL_29 = (19_112, 97_691)
LEVEL_30 = (19_112, 116_803)
LEVEL_31 = (19_112, 135_915)
LEVEL_32 = (19_112, 155_027)
LEVEL_33 = (19_112, 174_139)
LEVEL_34 = (19_112, 193_251)
LEVEL_35 = (22_934, 212_363)
LEVEL_36 = (27_520, 235_297)
LEVEL_37 = (33_024, 262_817)
LEVEL_38 = (39_628, 295_841)
LEVEL_39 = (47_553, 335_469)
LEVEL_40 = (51_357, 383_022)
LEVEL_41 = (55_465, 434_379)
LEVEL_42 = (59_902, 489_844)
LEVEL_43 = (64_694, 549_746)
LEVEL_44 = (69_869, 614_440)
LEVEL_45 = (75_458, 684_309)
LEVEL_46 = (81_494, 759_767)
LEVEL_47 = (88_013, 841_261)
LEVEL_48 = (95_054, 929_274)
LEVEL_49 = (102_658, 1_024_328)
LEVEL_50 = (110_870, 1_126_986)
LEVEL_51 = (119_739, 1_237_856)
LEVEL_52 = (129_318, 1_357_595)
LEVEL_53 = (139_663, 1_486_913)
LEVEL_54 = (150_836, 1_626_576)
LEVEL_55 = (162_902, 1_777_412)
LEVEL_56 = (175_934, 1_940_314)
LEVEL_57 = (190_008, 2_116_248)
LEVEL_58 = (205_208, 2_306_256)
LEVEL_59 = (221_624, 2_511_464)
LEVEL_60 = (221_624, 2_733_088)
LEVEL_61 = (221_624, 2_954_712)
LEVEL_62 = (221_624, 3_176_336)
LEVEL_63 = (221_624, 3_397_960)
LEVEL_64 = (221_624, 3_619_584)
LEVEL_65 = (238_245, 3_841_208)
LEVEL_66 = (256_113, 4_079_453)
LEVEL_67 = (275_321, 4_335_566)
LEVEL_68 = (295_970, 4_610_887)
LEVEL_69 = (318_167, 4_906_857)
LEVEL_70 = (342_029, 5_225_024)
LEVEL_71 = (367_681, 5_567_053)
LEVEL_72 = (395_257, 5_934_734)
LEVEL_73 = (424_901, 6_329_991)
LEVEL_74 = (456_768, 6_754_892)
LEVEL_75 = (488_741, 7_211_660)
LEVEL_76 = (522_952, 7_700_401)
LEVEL_77 = (559_558, 8_223_353)
LEVEL_78 = (598_727, 8_782_911)
LEVEL_79 = (640_637, 9_381_638)
LEVEL_80 = (685_481, 10_022_275)
LEVEL_81 = (733_464, 10_707_756)
LEVEL_82 = (784_806, 11_441_220)
LEVEL_83 = (839_742, 12_226_026)
LEVEL_84 = (898_523, 13_065_768)
LEVEL_85 = (961_419, 13_964_291)
LEVEL_86 = (1_028_718, 14_925_710)
LEVEL_87 = (1_100_728, 15_954_428)
LEVEL_88 = (1_177_778, 17_055_156)
LEVEL_89 = (1_260_222, 18_232_934)
LEVEL_90 = (1_342_136, 19_493_156)
LEVEL_91 = (1_429_374, 20_835_292)
LEVEL_92 = (1_522_283, 22_264_666)
LEVEL_93 = (1_621_231, 23_786_949)
LEVEL_94 = (1_726_611, 25_408_180)
LEVEL_95 = (1_838_840, 27_134_791)
LEVEL_96 = (1_958_364, 28_973_631)
LEVEL_97 = (2_085_657, 30_931_995)
LEVEL_98 = (2_221_224, 33_017_652)
LEVEL_99 = (2_365_603, 35_238_876)
LEVEL_100 = (2_365_603, 37_604_479)
LEVEL_101 = (2_365_603, 39_970_082)
LEVEL_102 = (2_365_603, 42_335_685)
LEVEL_103 = (2_365_603, 44_701_288)
LEVEL_104 = (2_365_603, 47_066_891)
LEVEL_105 = (2_519_367, 49_432_494)
LEVEL_106 = (2_683_125, 51_951_861)
LEVEL_107 = (2_857_528, 54_634_986)
LEVEL_108 = (3_043_267, 57_492_514)
LEVEL_109 = (3_241_079, 60_535_781)
LEVEL_110 = (3_451_749, 63_776_860)
LEVEL_111 = (3_676_112, 67_228_609)
LEVEL_112 = (3_915_059, 70_904_721)
LEVEL_113 = (4_169_537, 74_819_780)
LEVEL_114 = (4_440_556, 78_989_317)
LEVEL_115 = (4_729_192, 83_429_873)
LEVEL_116 = (5_036_589, 88_159_065)
LEVEL_117 = (5_363_967, 93_195_654)
LEVEL_118 = (5_712_624, 98_559_621)
LEVEL_119 = (6_083_944, 104_272_245)
LEVEL_120 = (6_479_400, 110_356_189)
LEVEL_121 = (6_900_561, 116_835_589)
LEVEL_122 = (7_349_097, 123_736_150)
LEVEL_123 = (7_826_788, 131_085_247)
LEVEL_124 = (8_335_529, 138_912_035)
LEVEL_125 = (8_877_338, 147_247_564)
LEVEL_126 = (9_454_364, 156_124_902)
LEVEL_127 = (10_068_897, 165_579_266)
LEVEL_128 = (10_723_375, 175_648_163)
LEVEL_129 = (11_420_394, 186_371_538)
LEVEL_130 = (12_162_719, 197_791_932)
LEVEL_131 = (12_953_295, 209_954_651)
LEVEL_132 = (13_795_259, 222_907_946)
LEVEL_133 = (14_691_950, 236_703_205)
LEVEL_134 = (15_646_926, 251_395_155)
LEVEL_135 = (16_663_976, 267_042_081)
LEVEL_136 = (17_747_134, 283_706_057)
LEVEL_137 = (18_900_697, 301_453_191)
LEVEL_138 = (20_129_242, 320_353_888)
LEVEL_139 = (21_437_642, 340_483_130)
LEVEL_140 = (22_777_494, 361_920_772)
LEVEL_141 = (24_201_087, 384_698_266)
LEVEL_142 = (25_713_654, 408_899_353)
LEVEL_143 = (27_320_757, 434_613_007)
LEVEL_144 = (29_028_304, 461_933_764)
LEVEL_145 = (30_842_573, 490_962_068)
LEVEL_146 = (32_770_233, 521_804_641)
LEVEL_147 = (34_818_372, 554_574_874)
LEVEL_148 = (36_994_520, 589_393_246)
LEVEL_149 = (39_306_677, 626_387_766)
LEVEL_150 = (41_763_344, 665_694_443)
LEVEL_151 = (44_373_553, 707_457_787)
LEVEL_152 = (47_146_900, 751_831_340)
LEVEL_153 = (50_093_581, 798_978_240)
LEVEL_154 = (53_224_429, 849_071_821)
LEVEL_155 = (56_550_955, 902_296_250)
LEVEL_156 = (60_085_389, 958_847_205)
LEVEL_157 = (63_840_725, 1_018_932_594)
LEVEL_158 = (67_830_770, 1_082_773_319)
LEVEL_159 = (72_070_193, 1_150_604_089)
LEVEL_160 = (76_574_580, 1_222_674_282)
LEVEL_161 = (81_360_491, 1_299_248_862)
LEVEL_162 = (86_445_521, 1_380_609_353)
LEVEL_163 = (91_848_366, 1_467_054_874)
LEVEL_164 = (97_588_888, 1_558_903_240)
LEVEL_165 = (103_688_193, 1_656_492_128)
LEVEL_166 = (110_168_705, 1_760_180_321)
LEVEL_167 = (117_054_249, 1_870_349_026)
LEVEL_168 = (124_370_139, 1_987_403_275)
LEVEL_169 = (132_143_272, 2_111_773_414)
LEVEL_170 = (138_750_435, 2_243_916_686)
LEVEL_171 = (145_687_956, 2_382_667_121)
LEVEL_172 = (152_972_353, 2_528_355_077)
LEVEL_173 = (160_620_970, 2_681_327_430)
LEVEL_174 = (168_652_018, 2_841_948_400)
LEVEL_175 = (177_084_618, 3_010_600_418)
LEVEL_176 = (185_938_848, 3_187_685_036)
LEVEL_177 = (195_235_790, 3_373_623_884)
LEVEL_178 = (204_997_579, 3_568_859_674)
LEVEL_179 = (215_247_457, 3_773_857_253)
LEVEL_180 = (226_009_829, 3_989_104_710)
LEVEL_181 = (237_310_320, 4_215_114_539)
LEVEL_182 = (249_175_836, 4_452_424_859)
LEVEL_183 = (261_634_627, 4_701_600_695)
LEVEL_184 = (274_716_358, 4_963_235_322)
LEVEL_185 = (288_452_175, 5_237_951_680)
LEVEL_186 = (302_874_783, 5_526_403_855)
LEVEL_187 = (318_018_522, 5_829_278_638)
LEVEL_188 = (333_919_448, 6_147_297_160)
LEVEL_189 = (350_615_420, 6_481_216_608)
LEVEL_190 = (368_146_191, 6_831_832_028)
LEVEL_191 = (386_553_500, 7_199_978_219)
LEVEL_192 = (405_881_175, 7_586_531_719)
LEVEL_193 = (426_175_233, 7_992_412_894)
LEVEL_194 = (447_483_994, 8_418_588_127)
LEVEL_195 = (469_858_193, 8_866_072_121)
LEVEL_196 = (493_351_102, 9_335_930_314)
LEVEL_197 = (518_018_657, 9_829_281_416)
LEVEL_198 = (543_919_589, 10_347_300_073)
LEVEL_199 = (571_115_568, 10_891_219_662)
LEVEL_200 = (2_207_026_470, 11_462_335_230)
LEVEL_201 = (2_471_869_646, 13_669_361_700)
LEVEL_202 = (2_768_494_003, 16_141_231_346)
LEVEL_203 = (3_100_713_283, 18_909_725_349)
LEVEL_204 = (3_472_798_876, 22_010_438_632)
LEVEL_205 = (3_889_534_741, 25_483_237_508)
LEVEL_206 = (4_356_278_909, 29_372_772_249)
LEVEL_207 = (4_879_032_378, 33_729_051_158)
LEVEL_208 = (5_464_516_263, 38_608_083_536)
LEVEL_209 = (6_120_258_214, 44_072_599_799)
LEVEL_210 = (7_956_335_678, 50_192_858_013)
LEVEL_211 = (8_831_532_602, 58_149_193_691)
LEVEL_212 = (9_803_001_188, 66_980_726_293)
LEVEL_213 = (10_881_331_318, 76_783_727_481)
LEVEL_214 = (12_078_277_762, 87_665_058_799)
LEVEL_215 = (15_701_761_090, 99_743_336_561)
LEVEL_216 = (17_114_919_588, 115_445_097_651)
LEVEL_217 = (18_655_262_350, 132_560_017_239)
LEVEL_218 = (20_334_235_961, 151_215_279_589)
LEVEL_219 = (22_164_317_197, 171_549_515_550)
LEVEL_220 = (28_813_612_356, 193_713_832_747)
LEVEL_221 = (30_830_565_220, 222_527_445_103)
LEVEL_222 = (32_988_704_785, 253_358_010_323)
LEVEL_223 = (35_297_914_119, 286_346_715_108)
LEVEL_224 = (37_768_768_107, 321_644_629_227)
LEVEL_225 = (49_099_398_539, 359_413_397_334)
LEVEL_226 = (52_536_356_436, 408_512_795_873)
LEVEL_227 = (56_213_901_386, 461_049_152_309)
LEVEL_228 = (60_148_874_483, 517_263_053_695)
LEVEL_229 = (64_359_295_696, 577_411_928_178)
LEVEL_230 = (83_667_084_404, 641_771_223_874)
LEVEL_231 = (86_177_096_936, 725_438_308_278)
LEVEL_232 = (88_762_409_844, 811_615_405_214)
LEVEL_233 = (91_425_282_139, 900_377_815_058)
LEVEL_234 = (94_168_040_603, 991_803_097_197)
LEVEL_235 = (122_418_452_783, 1_085_971_137_800)
LEVEL_236 = (126_091_006_366, 1_208_389_590_583)
LEVEL_237 = (129_873_736_556, 1_334_480_596_949)
LEVEL_238 = (133_769_948_652, 1_464_354_333_505)
LEVEL_239 = (137_783_047_111, 1_598_124_282_157)
LEVEL_240 = (179_117_961_244, 1_735_907_329_268)
LEVEL_241 = (184_491_500_081, 1_915_025_290_512)
LEVEL_242 = (190_026_245_083, 2_099_516_790_593)
LEVEL_243 = (195_727_032_435, 2_289_543_035_676)
LEVEL_244 = (201_598_843_408, 2_485_270_068_111)
LEVEL_245 = (262_078_496_430, 2_686_868_911_519)
LEVEL_246 = (269_940_851_322, 2_948_947_407_949)
LEVEL_247 = (278_039_076_861, 3_218_888_259_271)
LEVEL_248 = (286_380_249_166, 3_496_927_336_132)
LEVEL_249 = (294_971_656_640, 3_783_307_585_298)
LEVEL_250 = (442_457_484_960, 4_078_279_241_938)
LEVEL_251 = (455_731_209_508, 4_520_736_726_898)
LEVEL_252 = (469_403_145_793, 4_976_467_936_406)
LEVEL_253 = (483_485_240_166, 5_445_871_082_199)
LEVEL_254 = (497_989_797_370, 5_929_356_322_365)
LEVEL_255 = (512_929_491_291, 6_427_346_119_735)
LEVEL_256 = (528_317_376_029, 6_940_275_611_026)
LEVEL_257 = (544_166_897_309, 7_468_592_987_055)
LEVEL_258 = (560_491_904_228, 8_012_759_884_364)
LEVEL_259 = (577_306_661_354, 8_573_251_788_592)
LEVEL_260 = (1_731_919_984_062, 9_150_558_449_946)
LEVEL_261 = (1_749_239_183_902, 10_882_478_434_008)
LEVEL_262 = (1_766_731_575_741, 12_631_717_617_910)
LEVEL_263 = (1_784_398_891_498, 14_398_449_193_651)
LEVEL_264 = (1_802_242_880_412, 16_182_848_085_149)
LEVEL_265 = (2_342_915_744_535, 17_985_090_965_561)
LEVEL_266 = (2_366_344_901_980, 20_328_006_710_096)
LEVEL_267 = (2_390_008_350_999, 22_694_351_612_076)
LEVEL_268 = (2_413_908_434_508, 25_084_359_963_075)
LEVEL_269 = (2_438_047_518_853, 27_498_268_397_583)
LEVEL_270 = (5_412_465_491_853, 29_936_315_916_436)
LEVEL_271 = (5_466_590_146_771, 35_348_781_408_289)
LEVEL_272 = (5_521_256_048_238, 40_815_371_555_060)
LEVEL_273 = (5_576_468_608_720, 46_336_627_603_298)
LEVEL_274 = (5_632_233_294_807, 51_913_096_212_018)
LEVEL_275 = (11_377_111_255_510, 57_545_329_506_825)
LEVEL_276 = (12_514_822_381_061, 68_922_440_762_335)
LEVEL_277 = (13_766_304_619_167, 81_437_263_143_396)
LEVEL_278 = (15_142_935_081_083, 95_203_567_762_563)
LEVEL_279 = (16_657_228_589_191, 110_346_502_843_646)
LEVEL_280 = (33_647_601_750_165, 127_003_731_432_837)
LEVEL_281 = (37_012_361_925_181, 160_651_333_183_002)
LEVEL_282 = (40_713_598_117_699, 197_663_695_108_183)
LEVEL_283 = (44_784_957_929_468, 238_377_293_225_882)
LEVEL_284 = (49_263_453_722_414, 283_162_251_155_350)
LEVEL_285 = (99_512_176_519_276, 332_425_704_877_764)
LEVEL_286 = (109_463_394_171_203, 431_937_881_397_040)
LEVEL_287 = (120_409_733_588_323, 541_401_275_568_243)
LEVEL_288 = (132_450_706_947_155, 661_811_009_156_566)
LEVEL_289 = (145_695_777_641_870, 794_261_716_103_721)
LEVEL_290 = (294_305_470_836_577, 939_957_493_745_591)
LEVEL_291 = (323_736_017_920_234, 1_234_262_964_582_168)
LEVEL_292 = (356_109_619_712_257, 1_557_998_982_502_402)
LEVEL_293 = (391_720_581_683_482, 1_914_108_602_214_659)
LEVEL_294 = (430_892_639_851_830, 2_305_829_183_898_141)
LEVEL_295 = (870_403_132_500_696, 2_736_721_823_749_971)
LEVEL_296 = (957_443_445_750_765, 3_607_124_956_250_667)
LEVEL_297 = (1_053_187_790_325_841, 4_564_568_402_001_432)
LEVEL_298 = (1_158_506_569_358_425, 5_617_756_192_327_273)
LEVEL_299 = (1_737_759_854_037_637, 6_776_262_761_685_698)
LEVEL_300 = (0, 8_514_022_615_723_335)
