import yfinance as yf
import pandas_ta as ta
import pandas as pd

df = yf.download("AAPL", start="2021-01-01", end="2022-01-01")

def getIchimoku(data):

   df = yf.download("AAPL", start="2021-01-01", end="2022-01-01")

   high_candles = []
   low_candles = []
   close_candles = []
   for candle in data:

      high_candles.append(candle[2])
      low_candles.append(candle[3])
      close_candles.append(candle[4])

   ichimoku = ta.ichimoku(high_candles, low_candles, close_candles)
   df = pd.concat([df, ichimoku[0], ichimoku[1]], axis=1)
   df.head()


def calculate_ichimoku(dataArray, ):
   global dataArray,ichimokuStatus, current_high, current_low
   highs = np.append(dataArray[:, 0][:-1], current_high)
   lows = np.append(dataArray[:, 1][:-1], current_low)
   tenkan_sen = (float(highs[-self.params[0]:].max()) + float(lows[-self.params[0]:].min())) / 2
   kijun_sen = (float(highs[-self.params[1]:].max()) + float(lows[-self.params[1]:].min())) / 2
   senkou_span_A = float(tenkan_sen + kijun_sen) / 2
   senkou_span_B = (float(highs[-self.params[2]:].max()) + float(lows[-self.params[2]:].min())) / 2
   print ("Symbol   " + self.symbol + "   A: " + str(senkou_span_A) + " B: " + str(senkou_span_B) )
   if(ichimokuStatus == True & (senkou_span_A <= senkou_span_B)):
       #create alert here
       print("alert " + self.symbol + " from true to false in interval " + self.interval  + " where A : "  + str(senkou_span_A) + " B : " + str(senkou_span_B))
       ichimokuStatus = False
   if(ichimokuStatus == False & (senkou_span_A > senkou_span_B)):
       ichimokuStatus = True
       print("alert " + self.symbol + " from false to true in interval " + self.interval + " where A : "  + str(senkou_span_A) + " B : " + str(senkou_span_B))


import numpy as np

class ichmimokuCalculator:
    example =  [
        #beginning      Open            High            Low         Close           Volume          Close Time     quote a. v.  #trades   tbbav           tbqav          i
        [1517619600000, '0.10464900', '0.10528000', '0.10435000', '0.10448400', '4827.04100000', 1517623199999, '506.43531938', 15764, '2082.57500000', '218.56378168', '0'],
        [1517623200000, '0.10456600', '0.10518000', '0.10427400', '0.10504000', '4043.45500000', 1517626799999, '423.01771298', 12305, '1593.06000000', '166.73108823', '0'],
        [1517626800000, '0.10504000', '0.10520400', '0.10300000', '0.10338800', '6933.54300000', 1517630399999, '721.28357688', 19727, '3158.81300000', '328.69726366', '0'],
        [1517630400000, '0.10338800', '0.10512000', '0.10331100', '0.10452500', '4504.96100000', 1517633999999, '469.65952019', 15095, '2178.70300000', '227.20125476', '0'],
        [1517634000000, '0.10453000', '0.10502400', '0.10407400', '0.10470700', '3705.81500000', 1517637599999, '387.72240716', 11806, '1806.67800000', '189.09642863', '0'],
        [1517637600000, '0.10470600', '0.10671000', '0.10450100', '0.10660000', '4869.39400000', 1517641199999, '513.58036569', 18576, '2322.06600000', '244.95902996', '0'],
        [1517641200000, '0.10659400', '0.10682300', '0.10579400', '0.10612400', '3717.98000000', 1517644799999, '394.49871205', 15251, '1778.18400000', '188.77565488', '0'],
        [1517644800000, '0.10600100', '0.10651800', '0.10534000', '0.10608400', '4345.44800000', 1517648399999, '460.89394633', 15048, '2085.68600000', '221.26407117', '0'],
        [1517648400000, '0.10608300', '0.10644900', '0.10575200', '0.10623800', '4677.53800000', 1517651999999, '496.56292174', 18029, '2222.67500000', '236.03897206', '0'],
        [1517652000000, '0.10623900', '0.10712400', '0.10580000', '0.10711000', '3809.01100000', 1517655599999, '405.47868337', 14537, '1628.88600000', '173.48354481', '0'],
        [1517655600000, '0.10708200', '0.10750000', '0.10654000', '0.10667700', '4315.31800000', 1517659199999, '461.46855642', 17109, '2012.60800000', '215.28676683', '0'],
        [1517659200000, '0.10667700', '0.10696200', '0.10616600', '0.10630600', '5430.29800000', 1517662799999, '578.51056647', 19491, '2440.19400000', '260.07493254', '0'],
        [1517662800000, '0.10630600', '0.10687400', '0.10589300', '0.10610000', '6665.42600000', 1517666399999, '709.30360851', 24255, '3194.74300000', '340.07428128', '0'],
        [1517666400000, '0.10619000', '0.10630000', '0.10519300', '0.10540200', '8082.35800000', 1517669999999, '854.46377810', 30450, '3969.05800000', '419.74002017', '0'],
        [1517670000000, '0.10557500', '0.10565100', '0.10401300', '0.10437400', '9234.02800000', 1517673599999, '968.47375630', 30473, '4437.50700000', '465.72639582', '0'],
        [1517673600000, '0.10427100', '0.10527400', '0.10400100', '0.10524500', '6396.20300000', 1517677199999, '669.03151799', 23454, '3170.77200000', '331.71108842', '0'],
        [1517677200000, '0.10524500', '0.10550000', '0.10488600', '0.10495700', '3443.81900000', 1517680799999, '361.96943590', 14663, '1396.91000000', '146.89655509', '0'],
        [1517680800000, '0.10495700', '0.10525400', '0.10475000', '0.10497500', '4352.23500000', 1517684399999, '456.86476417', 15264, '2416.40700000', '253.74802170', '0'],
        [1517684400000, '0.10497600', '0.10517900', '0.10404900', '0.10499000', '4844.12500000', 1517687999999, '507.94057684', 17198, '2178.64900000', '228.54276611', '0'],
        [1517688000000, '0.10499000', '0.10504800', '0.10400100', '0.10487000', '4071.26000000', 1517691599999, '426.56030256', 16217, '2076.98700000', '217.71705003', '0'],
        [1517691600000, '0.10487000', '0.10526000', '0.10472800', '0.10502600', '3888.30800000', 1517695199999, '408.17666027', 13940, '2198.55400000', '230.89488119', '0'],
        [1517695200000, '0.10505000', '0.10590000', '0.10489600', '0.10554200', '3662.05700000', 1517698799999, '386.23424776', 12540, '1667.37500000', '175.92741339', '0'],
        [1517698800000, '0.10554200', '0.10580000', '0.10537800', '0.10551600', '3613.42300000', 1517702399999, '381.44263728', 14458, '1738.92700000', '183.63787066', '0'],
        [1517702400000, '0.10551600', '0.10600000', '0.10510200', '0.10518300', '4541.61900000', 1517705999999, '479.82524878', 16176, '2253.59500000', '238.18930899', '0'],
        [1517706000000, '0.10518400', '0.10599000', '0.10426400', '0.10496600', '6681.23200000', 1517709599999, '703.46867466', 25547, '3346.26200000', '352.49725636', '0'],
        [1517709600000, '0.10506500', '0.10550900', '0.10435800', '0.10505000', '3088.93600000', 1517713199999, '324.75516786', 14775, '1544.08200000', '162.38076877', '0'],
        [1517713200000, '0.10506000', '0.10538700', '0.10459700', '0.10465000', '3967.92900000', 1517716799999, '416.42013169', 17230, '1808.07800000', '189.81141904', '0'],
        [1517716800000, '0.10474400', '0.10490000', '0.10435900', '0.10464800', '3853.18400000', 1517720399999, '403.13670631', 15804, '1462.81800000', '153.11509334', '0'],
        [1517720400000, '0.10464800', '0.10476200', '0.10361000', '0.10412000', '4615.23400000', 1517723999999, '480.47116230', 19832, '1874.01000000', '195.16444056', '0'],
        [1517724000000, '0.10424300', '0.10424400', '0.10373100', '0.10384600', '4578.12900000', 1517727599999, '475.77655562', 17560, '2083.57000000', '216.59444942', '0'],
        [1517727600000, '0.10394700', '0.10423900', '0.10351300', '0.10353400', '4525.42900000', 1517731199999, '469.50537197', 18224, '1804.02600000', '187.25529950', '0'],
        [1517731200000, '0.10363800', '0.10401500', '0.10280100', '0.10304000', '4465.57900000', 1517734799999, '462.56544895', 15030, '1967.23300000', '203.90726262', '0'],
        [1517734800000, '0.10283800', '0.10339900', '0.10244700', '0.10254200', '7513.37800000', 1517738399999, '773.32618813', 32739, '3375.53300000', '347.55811073', '0'],
        [1517738400000, '0.10254200', '0.10286500', '0.10210100', '0.10227800', '5851.16200000', 1517741999999, '599.44026975', 25258, '2701.13000000', '276.83321165', '0'],
        [1517742000000, '0.10227700', '0.10277000', '0.10169100', '0.10193700', '5001.27600000', 1517745599999, '511.61473627', 23262, '2287.75700000', '234.07927715', '0'],
        [1517745600000, '0.10193800', '0.10278100', '0.10122300', '0.10263200', '8031.57200000', 1517749199999, '818.16186269', 34658, '3756.96400000', '382.90107574', '0'],
        [1517749200000, '0.10274700', '0.10278100', '0.10130000', '0.10147200', '4160.22400000', 1517752799999, '423.23057384', 18624, '2030.19200000', '206.57215955', '0'],
        [1517752800000, '0.10150000', '0.10203500', '0.10130100', '0.10192600', '3716.08400000', 1517756399999, '378.08078958', 17085, '1899.90200000', '193.36546304', '0'],
        [1517756400000, '0.10182400', '0.10241200', '0.10170200', '0.10202500', '5111.36600000', 1517759999999, '521.10391200', 18612, '2069.41600000', '211.04426911', '0'],
        [1517760000000, '0.10192700', '0.10330100', '0.10182000', '0.10297800', '5134.24300000', 1517763599999, '527.11937633', 18391, '2616.89000000', '268.81411449', '0'],
        [1517763600000, '0.10297700', '0.10330000', '0.10267400', '0.10302500', '3630.71200000', 1517767199999, '374.04378249', 14426, '1850.48900000', '190.70540241', '0'],
        [1517767200000, '0.10302500', '0.10329200', '0.10264500', '0.10288700', '3207.57600000', 1517770799999, '330.41243255', 13526, '1613.26400000', '166.23448636', '0'],
        [1517770800000, '0.10288100', '0.10320000', '0.10211800', '0.10230000', '4761.17900000', 1517774399999, '488.98108330', 16173, '2310.65800000', '237.40649487', '0'],
        [1517774400000, '0.10229700', '0.10250000', '0.09875300', '0.10198800', '11506.86100000', 1517777999999, '1162.29390403', 35339, '4881.81900000', '493.38899132', '0'],
        [1517778000000, '0.10197800', '0.10223300', '0.10031900', '0.10066000', '6125.70900000', 1517781599999, '620.47559396', 20153, '2873.64300000', '291.16091311', '0'],
        [1517781600000, '0.10056100', '0.10150000', '0.10009400', '0.10116700', '5256.23500000', 1517785199999, '529.88041652', 17431, '2577.26800000', '259.96018620', '0'],
        [1517785200000, '0.10107400', '0.10141900', '0.10020000', '0.10087000', '3650.51700000', 1517788799999, '369.06709829', 11399, '1643.37600000', '166.21403121', '0'],
        [1517788800000, '0.10086900', '0.10189100', '0.10049000', '0.10188600', '4519.79500000', 1517792399999, '457.50889002', 12219, '2249.03500000', '227.74137676', '0'],
        [1517792400000, '0.10174900', '0.10250000', '0.10139900', '0.10197800', '7656.61900000', 1517795999999, '780.93749510', 18437, '3447.23300000', '351.68188958', '0'],
        [1517796000000, '0.10197800', '0.10239000', '0.10145400', '0.10174600', '4514.72500000', 1517799599999, '459.76370915', 12499, '2058.99800000', '209.77560406', '0'],
        [1517799600000, '0.10178200', '0.10250000', '0.10155800', '0.10240100', '4750.01900000', 1517803199999, '485.29583228', 12379, '2655.66600000', '271.50194444', '0'],
        [1517803200000, '0.10240100', '0.10291300', '0.10224200', '0.10244000', '3375.59500000', 1517806799999, '346.40664790', 12820, '1721.61700000', '176.69648518', '0'],
        [1517806800000, '0.10250000', '0.10280100', '0.10225500', '0.10258900', '3530.58800000', 1517810399999, '362.21801727', 15102, '1816.41000000', '186.42810240', '0'],
        [1517810400000, '0.10258900', '0.10367200', '0.10229100', '0.10287900', '3477.79600000', 1517813999999, '357.54678858', 12800, '1734.47300000', '178.40352206', '0'],
        [1517814000000, '0.10287900', '0.10330000', '0.10220000', '0.10288200', '4790.27100000', 1517817599999, '492.59501666', 15905, '1959.76600000', '201.63618626', '0'],
        [1517817600000, '0.10288200', '0.10318000', '0.10211500', '0.10229500', '5013.03400000', 1517821199999, '514.69615079', 19425, '2550.94200000', '262.01937446', '0'],
        [1517821200000, '0.10230000', '0.10274700', '0.10200000', '0.10216400', '4673.60900000', 1517824799999, '478.15783918', 18353, '2581.17100000', '264.16471906', '0'],
        [1517824800000, '0.10216400', '0.10300000', '0.10130600', '0.10143000', '3715.07300000', 1517828399999, '379.32649450', 15619, '1785.38900000', '182.36999567', '0'],
        [1517828400000, '0.10143000', '0.10197900', '0.10100000', '0.10100000', '7202.87200000', 1517831999999, '731.28134844', 19930, '3290.96200000', '334.20919759', '0'],
        [1517832000000, '0.10100000', '0.10180800', '0.10075000', '0.10084800', '6044.22300000', 1517835599999, '610.98233199', 16834, '2788.24600000', '281.95013061', '0'],
        [1517835600000, '0.10084800', '0.10160000', '0.10000000', '0.10111000', '5355.93900000', 1517839199999, '540.42144759', 15308, '2489.63600000', '251.42996370', '0'],
        [1517839200000, '0.10111000', '0.10112400', '0.09886400', '0.09889100', '10412.50500000', 1517842799999, '1040.01342283', 33629, '4542.29600000', '453.68493959', '0'],
        [1517842800000, '0.09889000', '0.10093800', '0.09850100', '0.09934100', '12788.36300000', 1517846399999, '1268.69441522', 40455, '5296.43400000', '525.80215941', '0'],
        [1517846400000, '0.09934100', '0.09972900', '0.09869700', '0.09886600', '6039.14400000', 1517849999999, '598.93663659', 22394, '3075.34800000', '305.05042769', '0'],
        [1517850000000, '0.09877100', '0.09990000', '0.09836400', '0.09881500', '8377.50700000', 1517853599999, '828.86943772', 32724, '4475.20100000', '442.96943474', '0'],
        [1517853600000, '0.09885100', '0.09990000', '0.09760700', '0.09788000', '11417.25200000', 1517857199999, '1124.42282183', 38913, '5921.24900000', '583.33072165', '0'],
        [1517857200000, '0.09788000', '0.09826000', '0.09609700', '0.09630900', '12090.87300000', 1517860799999, '1170.84166292', 37117, '5820.19500000', '563.71644462', '0'],
        [1517860800000, '0.09631000', '0.10180000', '0.09563200', '0.09963000', '18021.34100000', 1517864399999, '1782.72870479', 49025, '8900.19600000', '880.30260167', '0'],
        [1517864400000, '0.09964300', '0.10060000', '0.09769300', '0.10046600', '8526.67100000', 1517867999999, '847.11706534', 25029, '4103.81100000', '407.70552375', '0'],
        [1517868000000, '0.10046600', '0.10167000', '0.09972300', '0.10029300', '8021.89900000', 1517871599999, '809.62075332', 25967, '3689.89000000', '372.62592177', '0'],
        [1517871600000, '0.10029300', '0.10228300', '0.09940000', '0.10080900', '6711.39400000', 1517875199999, '676.61470319', 20811, '3426.69900000', '345.64907301', '0'],
        [1517875200000, '0.10078700', '0.10149000', '0.10009800', '0.10071400', '5323.95100000', 1517878799999, '536.83484927', 15791, '2319.09300000', '233.88052907', '0'],
        [1517878800000, '0.10071800', '0.10100000', '0.09940600', '0.09958300', '8485.90700000', 1517882399999, '848.88355411', 31059, '4056.12400000', '405.91674639', '0'],
        [1517882400000, '0.09970200', '0.10039200', '0.09930000', '0.10000100', '11650.19500000', 1517885999999, '1163.07273012', 31323, '4079.47300000', '407.29554908', '0'],
        [1517886000000, '0.10011200', '0.10027400', '0.09835000', '0.09851100', '11665.07600000', 1517889599999, '1158.58794290', 33707, '4334.20100000', '430.61010763', '0'],
        [1517889600000, '0.09851100', '0.09916200', '0.09650000', '0.09650100', '9593.86600000', 1517893199999, '939.58965029', 33411, '4825.90500000', '472.83712508', '0'],
        [1517893200000, '0.09650100', '0.09788400', '0.09499900', '0.09638400', '16410.87600000', 1517896799999, '1577.80319915', 49161, '7649.56600000', '736.24457066', '0'],
        [1517896800000, '0.09628000', '0.09642900', '0.09470000', '0.09556000', '8104.96600000', 1517900399999, '773.77978047', 28896, '3579.07600000', '341.86761362', '0'],
        [1517900400000, '0.09546000', '0.09600000', '0.09505200', '0.09569400', '10184.79200000', 1517903999999, '971.00935882', 21769, '3322.06900000', '317.00001990', '0'],
        [1517904000000, '0.09555200', '0.09595800', '0.09443100', '0.09540800', '8164.59600000', 1517907599999, '776.01291721', 26355, '4432.14000000', '421.33714394', '0'],
        [1517907600000, '0.09540800', '0.09788700', '0.09458200', '0.09675900', '14423.63600000', 1517911199999, '1387.52779865', 44069, '7170.49000000', '690.57600887', '0'],
        [1517911200000, '0.09660100', '0.09739000', '0.09600500', '0.09687000', '7319.94800000', 1517914799999, '708.97984961', 22215, '3707.26800000', '359.23559635', '0'],
        [1517914800000, '0.09681900', '0.09764100', '0.09600000', '0.09652200', '7447.89000000', 1517918399999, '719.59286393', 19552, '3994.08100000', '386.07691395', '0'],
        [1517918400000, '0.09652200', '0.09873200', '0.09592500', '0.09831600', '7525.12800000', 1517921999999, '733.00376368', 18643, '3359.25100000', '327.18614456', '0'],
        [1517922000000, '0.09843900', '0.10139900', '0.09811400', '0.10118700', '12597.15700000', 1517925599999, '1259.16279470', 29368, '6067.73000000', '606.56866866', '0'],
        [1517925600000, '0.10118600', '0.10198900', '0.09894200', '0.10165500', '12116.54000000', 1517929199999, '1218.76699625', 32482, '5784.50700000', '581.81175897', '0'],
        [1517929200000, '0.10164900', '0.10200000', '0.10001300', '0.10172800', '13292.88300000', 1517932799999, '1346.54322188', 37841, '5226.64100000', '529.32165825', '0'],
        [1517932800000, '0.10162400', '0.10197100', '0.10010100', '0.10094400', '9580.75500000', 1517936399999, '970.80225321', 32449, '4070.19200000', '412.14941659', '0'],
        [1517936400000, '0.10094400', '0.10171900', '0.09974500', '0.10075600', '6569.02200000', 1517939999999, '662.12538184', 22874, '2799.19600000', '282.10348945', '0'],
        [1517940000000, '0.10075600', '0.10119000', '0.10033400', '0.10059800', '4915.61800000', 1517943599999, '495.55911314', 20273, '2616.07100000', '263.84512816', '0'],
        [1517943600000, '0.10059800', '0.10110000', '0.09964000', '0.10019600', '8425.09100000', 1517947199999, '846.06725281', 28185, '4499.29000000', '451.92926542', '0'],
        [1517947200000, '0.10005400', '0.10173300', '0.09981300', '0.10105100', '9934.24100000', 1517950799999, '1002.00535440', 27940, '4712.58500000', '475.52177782', '0'],
        [1517950800000, '0.10123100', '0.10226200', '0.10085200', '0.10155000', '7361.05800000', 1517954399999, '747.21734510', 19786, '3542.49000000', '359.75886427', '0'],
        [1517954400000, '0.10167300', '0.10219900', '0.10065700', '0.10117900', '6203.70800000', 1517957999999, '629.55141805', 15080, '2839.00900000', '288.03061907', '0'],
        [1517958000000, '0.10117900', '0.10231300', '0.10104600', '0.10189600', '4986.92400000', 1517961599999, '507.17202529', 12054, '2571.27600000', '261.55703397', '0'],
        [1517961600000, '0.10177000', '0.10205000', '0.10115900', '0.10141600', '5850.61600000', 1517965199999, '594.73560845', 14093, '2899.08100000', '294.78214766', '0'],
        [1517965200000, '0.10141500', '0.10210000', '0.10108000', '0.10147900', '3182.36300000', 1517968799999, '323.49964761', 8339, '1626.90000000', '165.42446238', '0'],
        [1517968800000, '0.10147800', '0.10195500', '0.09951500', '0.09982200', '4786.59300000', 1517972399999, '483.37217023', 13740, '2178.21900000', '220.01920119', '0'],
        [1517972400000, '0.09993700', '0.10193400', '0.09950000', '0.10021400', '3415.50000000', 1517975999999, '342.35046512', 8331, '1757.72500000', '176.33872566', '0'],
        [1517976000000, '0.10020500', '0.10088000', '0.09905600', '0.10021900', '3511.89400000', 1517979599999, '351.21161259', 8961, '1679.59900000', '167.98871288', '0'],
        [1517979600000, '0.10021900', '0.10132900', '0.09997900', '0.10076800', '2647.50300000', 1517983199999, '266.36337079', 7762, '1320.80500000', '132.94312465', '0'],
        [1517983200000, '0.10067500', '0.10081100', '0.10010100', '0.10044800', '2385.11600000', 1517986799999, '239.51386995', 5887, '1326.78500000', '133.27287743', '0'],
        [1517986800000, '0.10037000', '0.10079900', '0.10024600', '0.10058100', '2619.12800000', 1517990399999, '263.32017404', 7603, '1087.57200000', '109.37817711', '0'],
        [1517990400000, '0.10067700', '0.10120000', '0.10025100', '0.10117200', '3520.59500000', 1517993999999, '355.21991716', 9535, '1538.90900000', '155.34659454', '0'],
        [1517994000000, '0.10117200', '0.10199900', '0.10071800', '0.10172300', '5331.00100000', 1517997599999, '539.60485771', 13081, '2875.64300000', '291.18667607', '0'],
        [1517997600000, '0.10172400', '0.10220100', '0.10119800', '0.10133900', '5172.96200000', 1518001199999, '525.73486305', 14594, '2420.71000000', '246.13905158', '0'],
        [1518001200000, '0.10133800', '0.10257100', '0.10000000', '0.10084500', '6400.61100000', 1518004799999, '646.45546002', 15711, '2862.15600000', '289.37392662', '0'],
        [1518004800000, '0.10084000', '0.10141700', '0.09970200', '0.10013500', '4918.55900000', 1518008399999, '493.99939715', 12186, '1932.68200000', '194.19719938', '0'],
        [1518008400000, '0.10023000', '0.10100000', '0.09920000', '0.10010200', '7041.71500000', 1518011999999, '704.11746908', 18957, '3359.07100000', '336.10225039', '0'],
        [1518012000000, '0.10009100', '0.10100100', '0.09950300', '0.10013000', '6347.21300000', 1518015599999, '636.27463837', 16475, '3048.74600000', '305.88760438', '0'],
        [1518015600000, '0.10013000', '0.10111400', '0.09967300', '0.10001300', '5033.04700000', 1518019199999, '504.33378946', 11517, '2087.05800000', '209.32183585', '0'],
        [1518019200000, '0.10010000', '0.10119900', '0.09953100', '0.10088300', '5293.36000000', 1518022799999, '531.08265232', 15004, '2815.26800000', '282.58338640', '0'],
        [1518022800000, '0.10088300', '0.10139900', '0.10073100', '0.10126300', '3294.71400000', 1518026399999, '332.78925978', 11241, '1763.24200000', '178.16401959', '0'],
        [1518026400000, '0.10126000', '0.10140900', '0.10050100', '0.10083500', '3709.05000000', 1518029999999, '374.46606901', 11765, '1726.59000000', '174.37135311', '0'],
        [1518030000000, '0.10083500', '0.10130100', '0.10010000', '0.10109500', '4661.99600000', 1518033599999, '469.66668867', 14192, '2523.04500000', '254.28755287', '0'],
        [1518033600000, '0.10109500', '0.10130000', '0.10070000', '0.10105600', '3078.39000000', 1518037199999, '310.99309693', 9376, '1746.97100000', '176.52433570', '0'],
        [1518037200000, '0.10105300', '0.10113000', '0.10050000', '0.10112600', '2810.07600000', 1518040799999, '283.39628629', 8365, '1354.25700000', '136.60493461', '0'],
        [1518040800000, '0.10102200', '0.10190000', '0.10064600', '0.10104600', '4440.62000000', 1518044399999, '449.56038502', 16344, '2043.29100000', '206.95479044', '0'],
        [1518044400000, '0.10091700', '0.10117700', '0.09904500', '0.09935900', '6656.60900000', 1518047999999, '663.76323556', 23660, '3027.30000000', '301.99912493', '0'],
        [1518048000000, '0.09931100', '0.10067900', '0.09885000', '0.10029800', '3008.81000000', 1518049694651, '300.18848364', 12561, '1478.18000000', '147.68866787', '0']
    ]



    def __init__(self, symbol, api, params,interval):
        self.symbol = symbol
        self.api = api
        self.params = params
        self.interval = interval

    dataArray = np.array([0])
    ichimokuStatus = False
    current_high, current_low = 0, 0

    def get_neccesaries(self, datalist):
        returndata = []
        for window in datalist:
            returndata.append(list(map(float, window[2:4])))
        return np.array(returndata)

    def get_symbol(self):
        return self.symbol


    def setInitialData (self, data):
        global dataArray, ichimokuStatus, current_low,current_high
        dataArray = self.get_neccesaries(data)
        ichimokuStatus = False
        self.tenkan_sen = ((dataArray[:,0][-self.params[0]:].max()) + (dataArray[:,1][-self.params[0]:].min()))/2
        self.kijun_sen = ((dataArray[:,0][-self.params[1]:].max()) + (dataArray[:,1][-self.params[1]:].min()))/2
        self.senkou_span_A = (self.tenkan_sen + self.kijun_sen) / 2
        self.senkou_span_B = ((dataArray[:,0][-self.params[2]:].max()) + (dataArray[:,1][-self.params[2]:].min()))/2
        if(self.senkou_span_A > self.senkou_span_B):
            ichimokuStatus = True
        else:
            ichimokuStatus = False
        current_high = dataArray[:,0][-1]
        current_low = dataArray[:,1][-1]
        print("initialized " + self.symbol + " with current high " + str(current_high) + " low " + str(current_low))
    def get_data(self):
        return self.data

    def calculateChange(self,currentPrice):
        global current_high, current_low
        if (currentPrice > current_high):
            current_high = currentPrice
            self.calculate_ichimoku()
        if (currentPrice < current_low):
            current_low = currentPrice
            self.calculate_ichimoku()

    
