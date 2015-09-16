#-*- coding: UTF-8 -*-  

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import connection
import models
import time

# Create your views here.

def index(req):
	return render_to_response('index.html', {'title':'Main',
											'winPlayer1':'',
											 'winPlayer2':'', 
											 'winPlayer3':'', 
											 'winPlayer4':''})

def viewHistoryData(req):
	content, tableList = ShowHistoryData(req)
	return render_to_response('viewHistoryData.html', {'title':'HisTory Data',
													   'content':content,
													   'tableList':tableList})

def newGame(req):
	currentID = req.REQUEST.get('currentID', 'None')
	pA = 'None'
	pB = 'None'
	pC = 'None'
	pD = 'None'
	if currentID == 'None':
		currentID = str(int(time.strftime('%Y%m%d%H%M%S')))
		pA = req.REQUEST.get('pA', 'None')
		pB = req.REQUEST.get('pB', 'None')
		pC = req.REQUEST.get('pC', 'None')
		pD = req.REQUEST.get('pD', 'None')
		bz = models.BanZhuang(banZhuangID=currentID, playerA=pA, playerB=pB, playerC=pC, playerD=pD, date=str(int(time.strftime('%Y%m%d'))))
		bz.save()
	else:
		bz = models.BanZhuang.objects.get(banZhuangID=currentID)
		pA = bz.playerA
		pB = bz.playerB
		pC = bz.playerC
		pD = bz.playerD
	table, djid = ShowTable(req)
	return render_to_response('newGame.html', {'title':'newGame', 
											   'currentID': currentID,
											   'playerName1':pA,
											   'playerName2':pB,
											   'playerName3':pC,
											   'playerName4':pD,
											   'table':table,
											   'djid':djid}) 

def newGame_input(req):
	currentID = req.REQUEST.get('currentID', 'None')
	bz = models.BanZhuang.objects.get(banZhuangID=currentID)
	return render_to_response('newGame_input.html', {'title':'newGame_input', 
											   'currentID':currentID,
											   'playerName1':bz.playerA,
											   'playerName2':bz.playerB,
											   'playerName3':bz.playerC,
											   'playerName4':bz.playerD})

def newGame_inputData(req):
	InsertData(req)
	table, djid = ShowTable(req)
	currentID = req.REQUEST.get('currentID', 'None')
	bz = models.BanZhuang.objects.get(banZhuangID=currentID)
	return render_to_response('newGame.html', {'title':'newGame', 
											   'currentID': currentID,
											   'playerName1':bz.playerA,
											   'playerName2':bz.playerB,
											   'playerName3':bz.playerC,
											   'playerName4':bz.playerD,
											   'table':table,
											   'djid':djid}) 

def newGame_over(req):
	return newGameOverInsertData(req)
	
def newGame_view(req):
	tableList = ShowTableList(req)
	currentID = req.REQUEST.get('currentID', 'None')
	bz = models.BanZhuang.objects.get(banZhuangID=currentID)
	return render_to_response('newGame_view.html', {'title':'newGame_input', 
											   'currentID':currentID,
											   'playerName1':bz.playerA,
											   'playerName2':bz.playerB,
											   'playerName3':bz.playerC,
											   'playerName4':bz.playerD,
											   'tableList':tableList})

def oldGame(req):
	return render_to_response('oldGame.html', {'title':'oldGame'})

def playerData(req):
	playerName = req.REQUEST.get('Text_playerName', 'None')
	table = ()
	if playerName != 'None':
		table = ShowPlayerData(playerName)
	return render_to_response('playerData.html', {'title':'playerData',
												  'table':table})

def playerRanking(req):
	select = int(req.REQUEST.get('rankingRadio', '100'))
	if 100 == select:
		return render_to_response('playerRanking.html', {'title':'playerRanking'})
	table = None
	rankTable = []
	if select == 0:
		table = models.PlayerDate.objects .order_by('-pt')
		rankTable.append({'a':'排名', 'b':'pt值', 'c':'姓名'})
	elif select == 1:
		table = models.PlayerDate.objects .order_by('-rank')
		rankTable.append({'a':'排名', 'b':'rank值', 'c':'姓名'})
	elif select == 2:
		table = models.PlayerDate.objects .order_by('-level')
		rankTable.append({'a':'排名', 'b':'段位', 'c':'姓名'})
	elif select == 3:
		table = models.PlayerDate.objects .order_by('-gameAllCount')
		rankTable.append({'a':'排名', 'b':'对局数', 'c':'姓名'})
	elif select == 4:
		table = models.PlayerDate.objects .order_by('-winAC_ratio')
		rankTable.append({'a':'排名', 'b':'获胜率', 'c':'姓名'})
	elif select == 5:
		table = models.PlayerDate.objects .order_by('-lAC_ratio')
		rankTable.append({'a':'排名', 'b':'失败率', 'c':'姓名'})
	elif select == 6:
		table = models.PlayerDate.objects .order_by('-flAC_ratio')
		rankTable.append({'a':'排名', 'b':'副露率', 'c':'姓名'})
	elif select == 7:
		table = models.PlayerDate.objects .order_by('-lzAC_ratio')
		rankTable.append({'a':'排名', 'b':'立直率', 'c':'姓名'})
	elif select == 8:
		table = models.PlayerDate.objects .order_by('-tpAC_ratio')
		rankTable.append({'a':'排名', 'b':'听牌率', 'c':'姓名'})
	elif select == 9:
		table = models.PlayerDate.objects .order_by('-top_ratio')
		rankTable.append({'a':'排名', 'b':'一位率', 'c':'姓名'})
	elif select == 10:
		table = models.PlayerDate.objects .order_by('-second_ratio')
		rankTable.append({'a':'排名', 'b':'二位率', 'c':'姓名'})
	elif select == 11:
		table = models.PlayerDate.objects .order_by('-three_ratio')
		rankTable.append({'a':'排名', 'b':'三位率', 'c':'姓名'})
	elif select == 12:
		table = models.PlayerDate.objects .order_by('-four_ratio')
		rankTable.append({'a':'排名', 'b':'四位率', 'c':'姓名'})
	elif select == 13:
		table = models.PlayerDate.objects .order_by('-fly_ratio')
		rankTable.append({'a':'排名', 'b':'被飞率', 'c':'姓名'})
	elif select == 14:
		table = models.PlayerDate.objects .order_by('-avgWinPoint')
		rankTable.append({'a':'排名', 'b':'平均得点', 'c':'姓名'})
	elif select == 15:
		table = models.PlayerDate.objects .order_by('-avgLosePoint')
		rankTable.append({'a':'排名', 'b':'平均失点', 'c':'姓名'})
	elif select == 16:
		table = models.PlayerDate.objects .order_by('-winPoint_allCount')
		rankTable.append({'a':'排名', 'b':'总得点', 'c':'姓名'})
	elif select == 17:
		table = models.PlayerDate.objects .order_by('-losePoint_allCount')
		rankTable.append({'a':'排名', 'b':'总失点', 'c':'姓名'})
	elif select == 18:
		table = models.PlayerDate.objects .order_by('-bzAllCount')
		rankTable.append({'a':'排名', 'b':'半庄数', 'c':'姓名'})

	
	for i in range(len(table)):
		dict_person = {'a':i+1, 'b':'', 'c':table[i].name}
		if select == 0:
			dict_person['b'] = table[i].pt
		elif select == 1:
			dict_person['b'] = table[i].rank
		elif select == 2:
			dict_person['b'] = table[i].level
		elif select == 3:
			dict_person['b'] = table[i].gameAllCount
		elif select == 4:
			dict_person['b'] = table[i].winAC_ratio
		elif select == 5:
			dict_person['b'] = table[i].lAC_ratio
		elif select == 6:
			dict_person['b'] = table[i].flAC_ratio
		elif select == 7:
			dict_person['b'] = table[i].lzAC_ratio
		elif select == 8:
			dict_person['b'] = table[i].tpAC_ratio
		elif select == 9:
			tdict_person['b'] = table[i].top_ratio
		elif select == 10:
			dict_person['b'] = table[i].second_ratio
		elif select == 11:
			dict_person['b'] = table[i].three_ratio
		elif select == 12:
			dict_person['b'] = table[i].four_ratio
		elif select == 13:
			dict_person['b'] = table[i].fly_ratio
		elif select == 14:
			dict_person['b'] = table[i].avgWinPoint
		elif select == 15:
			dict_person['b'] = table[i].avgLosePoint
		elif select == 16:
			dict_person['b'] = table[i].winPoint_allCount
		elif select == 17:
			dict_person['b'] = table[i].losePoint_allCount
		elif select == 18:
			dict_person['b'] = table[i].bzAllCount
		rankTable.append(dict_person)

	return render_to_response('playerRanking.html', {'title':'playerRanking',
													 'rankTable':tuple(rankTable)})


def InsertData(req):
	cursor = connection.cursor()
	currentID= req.REQUEST.get('currentID', 'None')
	sql = "select count(*) from blog_duiju where banZhuangID = %s" % currentID
	cursor.execute(sql)
	djid = str(int(cursor.fetchone()[0]) + 1)


	liuju = False
	if req.REQUEST.get('cb_lz', 'None') != 'None':
		liuju = True

	currentWin = list()
	fuToA = calcFu(req, 'A')
	fanToA = calcFan(req, 'A')
	pointToA, tempWin = calcPoint(req, fuToA, fanToA, 'A')
	fPointA = calcFPoint(req, pointToA, 'A', currentWin, djid, cursor)
	if tempWin != '':
		currentWin.append(tempWin)

	fuToB = calcFu(req, 'B')
	fanToB = calcFan(req, 'B')
	pointToB, tempWin = calcPoint(req, fuToB, fanToB, 'B')
	fPointB = calcFPoint(req, pointToB, 'B', currentWin, djid, cursor)
	if tempWin != '':
		currentWin.append(tempWin)

	fuToC = calcFu(req, 'C')
	fanToC = calcFan(req, 'C')
	pointToC, tempWin = calcPoint(req, fuToC, fanToC, 'C')
	fPointC = calcFPoint(req, pointToC, 'C', currentWin, djid, cursor)
	if tempWin != '':
		currentWin.append(tempWin)

	fuToD = calcFu(req, 'D')
	fanToD = calcFan(req, 'D')
	pointToD, tempWin = calcPoint(req, fuToD, fanToD, 'D')
	fPointD = calcFPoint(req, pointToD, 'D', currentWin, djid, cursor)
	if tempWin != '':
		currentWin.append(tempWin)

	Atq, Btq, Ctq, Dtq = convenient_zm(req)
	#False if req.REQUEST.get('cb_A_3', 'None') == 'None' else True,

	currentID = req.REQUEST.get('currentID', 'None')
	bz = models.BanZhuang.objects.get(banZhuangID=currentID)

	lianZhuangShu = 0
	changkuang = 1 #稍后在改，自动判断现在是什么场合如果这局连庄数等于0，而这局没人赢则不变，有人赢判断是否相同否则不变，如果不等于0，在判断是否相同
	if int(djid) > 1:
		sjData = models.DuiJu.objects.get(banZhuangID=currentID ,duiJuID=str(int(djid)-1))
		lianZhuangShu = sjData.lianZhuangShu
		changkuang = sjData.changkuang
		if IsLianZhuang(sjData):
			lianZhuangShu += 1
		if ShangJuNotZhuangWin(sjData):
			changkuang += 1
			
			if ShangJuWinNotMe(req, sjData):
				lianZhuangShu = 0

	models.DuiJu(duiJuID=djid,
			     banZhuangID=req.REQUEST.get('currentID', ''),
			     changkuang=changkuang,
			     liuju=liuju,
			     lianZhuangShu=int(lianZhuangShu),
			     playerAname=bz.playerA,
			     playerAcurrentPoint=pointToA,
			     playerAcurrentFanShu=fanToA,
			     playerAcurrentFuShu=fuToA,
			     playerAfinishPoint=fPointA,
			     playerAhl=False if req.REQUEST.get('cb_A_0', 'None') == 'None' else True,
			     playerAzm=False if req.REQUEST.get('cb_A_1', 'None') == 'None' else True,
			     playerAfc=False if req.REQUEST.get('cb_A_2', 'None') == 'None' else True,
			     playerAtq=Atq,
			     playerAlz=False if req.REQUEST.get('cb_A_4', 'None') == 'None' else True,
			     playerAzj=False if req.REQUEST.get('cb_A_8', 'None') == 'None' else True,
			     playerAfl=False if req.REQUEST.get('cb_A_6', 'None') == 'None' else True,
			     playerAtp=False if req.REQUEST.get('cb_A_7', 'None') == 'None' else True,
			     playerBname=bz.playerB,
			     playerBcurrentPoint=pointToB,
			     playerBcurrentFanShu=fanToB,
			     playerBcurrentFuShu=fuToB,
			     playerBfinishPoint=fPointB,
			     playerBhl=False if req.REQUEST.get('cb_B_0', 'None') == 'None' else True,
			     playerBzm=False if req.REQUEST.get('cb_B_1', 'None') == 'None' else True,
			     playerBfc=False if req.REQUEST.get('cb_B_2', 'None') == 'None' else True,
			     playerBtq=Btq,
			     playerBlz=False if req.REQUEST.get('cb_B_4', 'None') == 'None' else True,
			     playerBzj=False if req.REQUEST.get('cb_B_8', 'None') == 'None' else True,
			     playerBtp=False if req.REQUEST.get('cb_B_7', 'None') == 'None' else True,
			     playerBfl=False if req.REQUEST.get('cb_B_6', 'None') == 'None' else True,
			     playerCname=bz.playerC,
			     playerCcurrentPoint=pointToC,
			     playerCcurrentFanShu=fanToC,
			     playerCcurrentFuShu=fuToC,
			     playerCfinishPoint=fPointC,
			 	 playerChl=False if req.REQUEST.get('cb_C_0', 'None') == 'None' else True,
			     playerCzm=False if req.REQUEST.get('cb_C_1', 'None') == 'None' else True,
			     playerCfc=False if req.REQUEST.get('cb_C_2', 'None') == 'None' else True,
			     playerCtq=Ctq,
			     playerClz=False if req.REQUEST.get('cb_C_4', 'None') == 'None' else True,
			     playerCzj=False if req.REQUEST.get('cb_C_8', 'None') == 'None' else True,
			     playerCtp=False if req.REQUEST.get('cb_C_7', 'None') == 'None' else True,
			     playerCfl=False if req.REQUEST.get('cb_C_6', 'None') == 'None' else True,
			     playerDname=bz.playerD,
			     playerDcurrentPoint=pointToD,
			     playerDcurrentFanShu=fanToD,
			     playerDcurrentFuShu=fuToD,
			     playerDfinishPoint=fPointD,
			     playerDhl=False if req.REQUEST.get('cb_D_0', 'None') == 'None' else True,
			     playerDzm=False if req.REQUEST.get('cb_D_1', 'None') == 'None' else True,
			     playerDfc=False if req.REQUEST.get('cb_D_2', 'None') == 'None' else True,
			     playerDtq=Dtq,
			     playerDlz=False if req.REQUEST.get('cb_D_4', 'None') == 'None' else True,
			     playerDzj=False if req.REQUEST.get('cb_D_8', 'None') == 'None' else True,
			     playerDtp=False if req.REQUEST.get('cb_D_7', 'None') == 'None' else True,
			     playerDfl=False if req.REQUEST.get('cb_D_6', 'None') == 'None' else True
				).save()
	
	UpdatePlayerData(req, djid)
	cursor.close()

def convenient_zm(req):
	Atq = False
	Btq = False
	Ctq = False
	Dtq = False


	if 'None' != req.REQUEST.get('cb_A_1', 'None'):
		Btq = True
		Ctq = True
		Dtq = True
	elif 'None' != req.REQUEST.get('cb_B_1', 'None'):
		Atq = True
		Ctq = True
		Dtq = True
	elif 'None' != req.REQUEST.get('cb_C_1', 'None'):
		Atq = True
		Btq = True
		Dtq = True
	elif 'None' != req.REQUEST.get('cb_D_1', 'None'):
		Atq = True
		Btq = True
		Ctq = True
		
	return Atq, Btq, Ctq, Dtq

def calcFPoint(req, point, playerName, currentWinList, djid, cursor):
	if djid == '1':
		if req.REQUEST.get('cb_' + playerName + '_8', 'None') != 'None':
			return 25000+point
		return 25000+point
	else:
		currentID = req.REQUEST.get('currentID', 'None')
		sql = "select * from blog_duiju where banZhuangID=%s and duiJuID=%d" % (currentID, (int(djid)-1))
		cursor.execute(sql)
		shangju = cursor.fetchone()

		palyerShengYuPoint = 0
		if(playerName == 'A'):
			palyerShengYuPoint = shangju[10]
		elif(playerName == 'B'):
			palyerShengYuPoint = shangju[23]
		elif(playerName == 'C'):
			palyerShengYuPoint = shangju[36]
		else:
			palyerShengYuPoint = shangju[49]
		return palyerShengYuPoint + point

def calcPoint(req, fu, fan, playerName):
	point = 0
	if fan < 5:
		point = fu*2**(fan+2)
		if point%100 > 0:
			point = ((point/100+1)*100)
		if point > 2000:
			point = 2000
	elif fan == 5:
		point = 2000
	elif fan == 6:
		point = 3000
	elif fan == 8:
		point = 4000
	elif fan == 11:
		point = 6000
	elif fan == 13:
		point = 8000

	win = True if ('None' != req.REQUEST.get('cb_'+ playerName +'_0', 'None') or 'None' != req.REQUEST.get('cb_'+ playerName +'_1', 'None')) else False
	if win:
		if 'None' != req.REQUEST.get('cb_'+ playerName +'_8', 'None'):
			point *= 6
		else:
			point *= 4
		return point, playerName
	else:
		point = sendMoney(req, 'A')
		point += sendMoney(req, 'B')
		point += sendMoney(req, 'C')
		point += sendMoney(req, 'D')

		if 'None' != req.REQUEST.get('cb_'+ playerName +'_2', 'None'):
			point *= -4
			if ('None' != req.REQUEST.get('cb_A_8', 'None') and ('None' != req.REQUEST.get('cb_A_0', 'None') or 'None' != req.REQUEST.get('cb_A_1', 'None'))) or ('None' != req.REQUEST.get('cb_B_8', 'None') and ('None' != req.REQUEST.get('cb_B_0', 'None') or 'None' != req.REQUEST.get('cb_B_1', 'None'))) or ('None' != req.REQUEST.get('cb_C_8', 'None') and ('None' != req.REQUEST.get('cb_C_0', 'None') or 'None' != req.REQUEST.get('cb_C_1', 'None'))) or ('None' != req.REQUEST.get('cb_D_8', 'None') and ('None' != req.REQUEST.get('cb_D_0', 'None') or 'None' != req.REQUEST.get('cb_D_1', 'None'))):
				point *= 1.5
			return point, ''
		else:
			if 'None' != req.REQUEST.get('cb_A_1', 'None') or 'None' != req.REQUEST.get('cb_B_1', 'None') or 'None' != req.REQUEST.get('cb_C_1', 'None') or 'None' != req.REQUEST.get('cb_D_1', 'None'):
				if 'None' != req.REQUEST.get('cb_'+ playerName +'_8', 'None'):
					return point*-2, ''
				else:
					if ('None' != req.REQUEST.get('cb_A_8', 'None') and 'None' != req.REQUEST.get('cb_A_1', 'None')) or ('None' != req.REQUEST.get('cb_B_8', 'None') and 'None' != req.REQUEST.get('cb_B_1', 'None')) or ('None' != req.REQUEST.get('cb_C_8', 'None') and 'None' != req.REQUEST.get('cb_C_1', 'None')) or ('None' != req.REQUEST.get('cb_D_8', 'None') and 'None' != req.REQUEST.get('cb_D_1', 'None')):
					   return point*-2,''
					return -point, ''
			else:
				return 0, ''

def sendMoney(req, playerName):
	fan = calcFan(req, playerName)
	fu = calcFu(req, playerName)
	point = 0
	if fan < 5:
		point = fu*2**(fan+2)
		if point%100 > 0:
			point = ((point/100+1)*100)
		if point > 2000:
			point = 2000
	elif fan == 5:
		point = 2000
	elif fan == 6:
		point = 3000
	elif fan == 8:
		point = 4000
	elif fan == 11:
		point = 6000
	elif fan == 13:
		point = 8000

	return point


def calcFan(req, playerName):
	if 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_1', 'None')):
		return 1
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_2', 'None')):
		return 2
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_3', 'None')):
		return 3
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_4', 'None')):
		return 4
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_5', 'None')):
		return 5
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_6', 'None')):
		return 6
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_8', 'None')):
		return 8
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_11', 'None')):
		return 11
	elif 'None' != (req.REQUEST.get('cb_' + playerName + '_Fan_13', 'None')):
		return 13
	else:
		return 0


def calcFu(req, palyName):
	if 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_1', 'None')):
		return 20
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_2', 'None')):
		return 25
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_3', 'None')):
		return 30
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_4', 'None')):
		return 40
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_5', 'None')):
		return 50
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_6', 'None')):
		return 60
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_7', 'None')):
		return 70
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_8', 'None')):
		return 80
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_9', 'None')):
		return 90
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_10', 'None')):
		return 100
	elif 'None' != (req.REQUEST.get('cb_' + palyName + '_Fu_11', 'None')):
		return 110
	else :
		return 0

def ShowBeiZu(select, Data):
	if (select == 1):
		return ('和了 ' if Data[11] else '') + \
			   ('自摸 ' if Data[12] else '') + \
			   ('放铳 ' if Data[13] else '') + \
			   ('躺枪 ' if Data[14] else '') + \
			   ('立直 ' if Data[15] else '') + \
			   ('庄家 ' if Data[16] else '') + \
			   ('副露 ' if Data[17] else '') + \
			   ('听牌 ' if Data[18] else '')
	elif select == 2:
		return ('和了 ' if Data[24] else '') + \
			   ('自摸 ' if Data[25] else '') + \
			   ('放铳 ' if Data[26] else '') + \
			   ('躺枪 ' if Data[27] else '') + \
			   ('立直 ' if Data[28] else '') + \
			   ('庄家 ' if Data[29] else '') + \
			   ('副露 ' if Data[30] else '') + \
			   ('听牌 ' if Data[31] else '')
	elif select == 3:
		return ('和了 ' if Data[37] else '') + \
			   ('自摸 ' if Data[38] else '') + \
			   ('放铳 ' if Data[39] else '') + \
			   ('躺枪 ' if Data[40] else '') + \
			   ('立直 ' if Data[41] else '') + \
			   ('庄家 ' if Data[42] else '') + \
			   ('副露 ' if Data[43] else '') + \
			   ('听牌 ' if Data[44] else '')
	else:
		return ('和了 ' if Data[50] else '') + \
			   ('自摸 ' if Data[51] else '') + \
			   ('放铳 ' if Data[52] else '') + \
			   ('躺枪 ' if Data[53] else '') + \
			   ('立直 ' if Data[54] else '') + \
			   ('庄家 ' if Data[55] else '') + \
			   ('副露 ' if Data[56] else '') + \
			   ('听牌 ' if Data[57] else '')

def ShowTable(req):
	currentID = req.REQUEST.get('currentID', 'None')
	if(currentID == 'None'):
		return "", 0
	sql = "select count(*) from blog_duiju where banZhuangID = %s" % currentID
	cursor = connection.cursor()
	cursor.execute(sql)
	djid = str(int(cursor.fetchone()[0]))
	if int(djid) == 0:
		return "", 0

	sql = "select * from blog_duiju where banZhuangID = %s and duiJuID =%s" % (currentID, djid)
	cursor.execute(sql)
	duiJuData = cursor.fetchone()
	DictDuijuName = {1:"东一", 2:"东二", 3:"东三", 4:"东四", \
					 5:"南一", 6:"南二", 7:"南三", 8:"南四", \
					 9:"西一", 10:"西二", 11:"西三", 12:"西四", \
					 13:"北一", 14:"北二", 15:"北三", 16:"北四"}
	djid = DictDuijuName[duiJuData[3]]

	djid += " " + str(duiJuData[5]) + "本场"
	table = ({'name':duiJuData[6], 'Fpoint':duiJuData[10], 'point':duiJuData[7], 'fan':duiJuData[8] ,'fu':duiJuData[9], 'beiju':ShowBeiZu(1, duiJuData)}, \
			 {'name':duiJuData[19], 'Fpoint':duiJuData[23], 'point':duiJuData[20], 'fan':duiJuData[21] ,'fu':duiJuData[22], 'beiju':ShowBeiZu(2, duiJuData)}, \
			 {'name':duiJuData[32], 'Fpoint':duiJuData[36], 'point':duiJuData[33], 'fan':duiJuData[34] ,'fu':duiJuData[35], 'beiju':ShowBeiZu(3, duiJuData)}, \
			 {'name':duiJuData[45], 'Fpoint':duiJuData[49], 'point':duiJuData[46], 'fan':duiJuData[47] ,'fu':duiJuData[48], 'beiju':ShowBeiZu(4, duiJuData)})
	cursor.close()
	return table, djid

def ShowTableList(req):
	currentID = req.REQUEST.get('currentID', 'None')
	sql = "select count(*) from blog_duiju where banZhuangID = %s" % currentID
	cursor = connection.cursor()
	cursor.execute(sql)
	djid = int(cursor.fetchone()[0])

	tableList = []
	for i in range(1, djid+1):
		table = []
		table.append(i)
		sql = "select * from blog_duiju where banZhuangID = %s and duiJuID =%s" % (currentID, i)
		cursor.execute(sql)	
		duiJuData = cursor.fetchone()
		dictData = ({'name':duiJuData[6], 'Fpoint':duiJuData[10], 'point':duiJuData[7], 'fan':duiJuData[8] ,'fu':duiJuData[9], 'beiju':ShowBeiZu(1, duiJuData)}, \
	   			    {'name':duiJuData[19], 'Fpoint':duiJuData[23], 'point':duiJuData[20], 'fan':duiJuData[21] ,'fu':duiJuData[22], 'beiju':ShowBeiZu(2, duiJuData)}, \
				    {'name':duiJuData[32], 'Fpoint':duiJuData[36], 'point':duiJuData[33], 'fan':duiJuData[34] ,'fu':duiJuData[35], 'beiju':ShowBeiZu(3, duiJuData)}, \
				    {'name':duiJuData[45], 'Fpoint':duiJuData[49], 'point':duiJuData[46], 'fan':duiJuData[47] ,'fu':duiJuData[48], 'beiju':ShowBeiZu(4, duiJuData)})
		table.append(dictData)
		tableList.append(tuple(table))

	cursor.close()
	return tuple(tableList)

def showHistoryDataBzID(req, text):
	content = "search BzID: " + text
	sql = "select count(*) from blog_duiju where banZhuangID like '%%%s%%'" % text
	cursor = connection.cursor()
	cursor.execute(sql)
	djid = int(cursor.fetchone()[0])
	
	sql = "select * from blog_duiju where banZhuangID like '%%%s%%'" % text
	cursor = connection.cursor()
	cursor.execute(sql)
	DuiJuAllData = cursor.fetchall()
	tableList = []
	for i in range(1, djid+1):
		table = []
		table.append(i)
		
		cursor.execute(sql)	
		duiJuData = DuiJuAllData[i-1]
		dictData = ({'name':duiJuData[6], 'Fpoint':duiJuData[10], 'point':duiJuData[7], 'fan':duiJuData[8] ,'fu':duiJuData[9], 'beiju':ShowBeiZu(1, duiJuData)}, \
	   			    {'name':duiJuData[19], 'Fpoint':duiJuData[23], 'point':duiJuData[20], 'fan':duiJuData[21] ,'fu':duiJuData[22], 'beiju':ShowBeiZu(2, duiJuData)}, \
				    {'name':duiJuData[32], 'Fpoint':duiJuData[36], 'point':duiJuData[33], 'fan':duiJuData[34] ,'fu':duiJuData[35], 'beiju':ShowBeiZu(3, duiJuData)}, \
				    {'name':duiJuData[45], 'Fpoint':duiJuData[49], 'point':duiJuData[46], 'fan':duiJuData[47] ,'fu':duiJuData[48], 'beiju':ShowBeiZu(4, duiJuData)})
		table.append(dictData)
		tableList.append(tuple(table))


	cursor.close()
	return content, tuple(tableList)


def showHistoryDataPlayerID(req, text):
	content = "search PlayerID: " + text
	sql = "select count(*) from blog_duiju where playerAname = '%s' or playerBname = '%s' or playerCname = '%s' or playerDname = '%s'" % (text, text, text, text)
	cursor = connection.cursor()
	cursor.execute(sql)
	djid = int(cursor.fetchone()[0])

	sql = "select * from blog_duiju where playerAname = '%s' or playerBname = '%s' or playerCname = '%s' or playerDname = '%s'" % (text, text, text, text)
	cursor = connection.cursor()
	cursor.execute(sql)
	DuiJuAllData = cursor.fetchall()
	tableList = []
	for i in range(1, djid+1):
		table = []
		table.append(i)
		duiJuData = DuiJuAllData[i-1]
		dictData = ({'name':duiJuData[6], 'Fpoint':duiJuData[10], 'point':duiJuData[7], 'fan':duiJuData[8] ,'fu':duiJuData[9], 'beiju':ShowBeiZu(1, duiJuData)}, \
	   			    {'name':duiJuData[19], 'Fpoint':duiJuData[23], 'point':duiJuData[20], 'fan':duiJuData[21] ,'fu':duiJuData[22], 'beiju':ShowBeiZu(2, duiJuData)}, \
				    {'name':duiJuData[32], 'Fpoint':duiJuData[36], 'point':duiJuData[33], 'fan':duiJuData[34] ,'fu':duiJuData[35], 'beiju':ShowBeiZu(3, duiJuData)}, \
				    {'name':duiJuData[45], 'Fpoint':duiJuData[49], 'point':duiJuData[46], 'fan':duiJuData[47] ,'fu':duiJuData[48], 'beiju':ShowBeiZu(4, duiJuData)})
		table.append(dictData)
		tableList.append(tuple(table))

	cursor.close()
	return content, tuple(tableList)

def showHistoryDataDate(req, text):
	content = "search Data: " + text
	sql = "select count(*) from blog_duiju where banZhuangID like '%%%s%%'" % (text)
	cursor = connection.cursor()
	cursor.execute(sql)
	djid = int(cursor.fetchone()[0])

	sql = "select * from blog_duiju where banZhuangID like '%%%s%%'" % (text)
	cursor = connection.cursor()
	cursor.execute(sql)
	DuiJuAllData = cursor.fetchall()
	tableList = []
	for i in range(1, djid+1):
		table = []
		table.append(i)
		duiJuData = DuiJuAllData[i-1]
		dictData = ({'name':duiJuData[6], 'Fpoint':duiJuData[10], 'point':duiJuData[7], 'fan':duiJuData[8] ,'fu':duiJuData[9], 'beiju':ShowBeiZu(1, duiJuData)}, \
	   			    {'name':duiJuData[19], 'Fpoint':duiJuData[23], 'point':duiJuData[20], 'fan':duiJuData[21] ,'fu':duiJuData[22], 'beiju':ShowBeiZu(2, duiJuData)}, \
				    {'name':duiJuData[32], 'Fpoint':duiJuData[36], 'point':duiJuData[33], 'fan':duiJuData[34] ,'fu':duiJuData[35], 'beiju':ShowBeiZu(3, duiJuData)}, \
				    {'name':duiJuData[45], 'Fpoint':duiJuData[49], 'point':duiJuData[46], 'fan':duiJuData[47] ,'fu':duiJuData[48], 'beiju':ShowBeiZu(4, duiJuData)})
		table.append(dictData)
		tableList.append(tuple(table))

	cursor.close()
	return content, tuple(tableList)

def ShowHistoryData(req):
	text = req.REQUEST.get('textinput_bzID', 'None')
	if text != 'None':
		return showHistoryDataBzID(req, text)
	else:
		text = req.REQUEST.get('textinput_playerID', 'None')
		if text != 'None':
			return showHistoryDataPlayerID(req, text)
		else:
			date = req.REQUEST.get('textinput_year', '') + req.REQUEST.get('textinput_mon', '') + req.REQUEST.get('textinput_day', '')
			if date != "":
				return showHistoryDataDate(req, date)

def ShowPlayerData(playerName):
	player = models.PlayerDate.objects.get(name=playerName)
	table = [{'a':'姓名：', 'b': player.name, 'c': '排名'},
			 {'a':'段位：', 'b': player.level, 'c': 'None'},
			 {'a':'PT ：', 'b': player.pt, 'c': 'None'},
			 {'a':'R值：', 'b': player.rank, 'c': 'None'},
			 {'a':'总盘数：', 'b': player.gameAllCount, 'c': 'None'},
			 {'a':'半庄总数：', 'b': player.bzAllCount, 'c': 'None'},
			 {'a':'赢的次数：', 'b': player.winAllCount, 'c': 'None'},
			 {'a':'赢的概率：', 'b': player.winAC_ratio, 'c': 'None'},
			 {'a':'输的次数：', 'b': player.loseAllCount, 'c': 'None'},
			 {'a':'输的概率：', 'b': player.lAC_ratio, 'c': 'None'},
			 {'a':'副露次数：', 'b': player.fuluAllCount, 'c': 'None'},
			 {'a':'副露概率：', 'b': player.flAC_ratio, 'c': 'None'},
			 {'a':'立直次数：', 'b': player.lizhiAllCount, 'c': 'None'},
			 {'a':'立直概率：', 'b': player.lzAC_ratio, 'c': 'None'},
			 {'a':'听牌次数：', 'b': player.tingpaiAllCount, 'c': 'None'},
			 {'a':'听牌概率：', 'b': player.tpAC_ratio, 'c': 'None'},
			 {'a':'抢老大次数：', 'b': player.top_allCount, 'c': 'None'},
			 {'a':'抢老大概率：', 'b': player.top_ratio, 'c': 'None'},
			 {'a':'当老二次数：', 'b': player.second_allCount, 'c': 'None'},
			 {'a':'当老二概率：', 'b': player.second_ratio, 'c': 'None'},
			 {'a':'安定三次数：', 'b': player.three_allCount, 'c': 'None'},
			 {'a':'安定三概率：', 'b': player.three_ratio, 'c': 'None'},
			 {'a':'苦逼四次数：', 'b': player.four_allCount, 'c': 'None'},
			 {'a':'苦逼四概率：', 'b': player.four_ratio, 'c': 'None'},
			 {'a':'做飞机次数：', 'b': player.fly_allCount, 'c': 'None'},
			 {'a':'做飞机概率：', 'b': player.fly_ratio, 'c': 'None'},
			 {'a':'平均得点：', 'b': player.avgWinPoint, 'c': 'None'},
			 {'a':'平均失点：', 'b': player.avgLosePoint, 'c': 'None'},
			 {'a':'总共得点：', 'b': player.winPoint_allCount, 'c': 'None'},
			 {'a':'总共得点：', 'b': player.losePoint_allCount, 'c': 'None'}]

	return tuple(table)

def UpdatePlayerData(req, djid):
	currentID= req.REQUEST.get('currentID', '')
	
	DJData = models.DuiJu.objects.get(duiJuID=djid, banZhuangID=currentID)
	bz = models.BanZhuang.objects.get(banZhuangID=currentID)

	UserRegTest(req, bz.playerA)
	UserRegTest(req, bz.playerB)
	UserRegTest(req, bz.playerC)
	UserRegTest(req, bz.playerD)

	playerA = models.PlayerDate.objects.get(name=bz.playerA)
	playerB = models.PlayerDate.objects.get(name=bz.playerB)
	playerC = models.PlayerDate.objects.get(name=bz.playerC)
	playerD = models.PlayerDate.objects.get(name=bz.playerD)

	playerA.gameAllCount += 1
	playerB.gameAllCount += 1
	playerC.gameAllCount += 1
	playerD.gameAllCount += 1

	if DJData.playerAcurrentPoint > 0:
		playerA.winPoint_allCount += DJData.playerAcurrentPoint
	elif DJData.playerAcurrentPoint < 0:
		playerA.losePoint_allCount += (-1*DJData.playerAcurrentPoint)

	if DJData.playerBcurrentPoint > 0:
		playerB.winPoint_allCount += DJData.playerBcurrentPoint
	elif DJData.playerBcurrentPoint < 0:
		playerB.losePoint_allCount += (-1*DJData.playerBcurrentPoint)

	if DJData.playerCcurrentPoint > 0:
		playerC.winPoint_allCount += DJData.playerCcurrentPoint
	elif DJData.playerCcurrentPoint < 0:
		playerC.losePoint_allCount += (-1*DJData.playerCcurrentPoint)

	if DJData.playerDcurrentPoint > 0:
		playerD.winPoint_allCount += DJData.playerDcurrentPoint
	elif DJData.playerDcurrentPoint < 0:
		playerD.losePoint_allCount += (-1*DJData.playerDcurrentPoint)


	if DJData.playerAhl or DJData.playerAzm:
		playerA.winAllCount += 1
	playerA.winAC_ratio = (playerA.winAllCount*1.0 / playerA.gameAllCount*1.0)*100

	if DJData.playerBhl or DJData.playerBzm:
		playerB.winAllCount += 1
	playerB.winAC_ratio = (playerB.winAllCount*1.0 / playerB.gameAllCount*1.0)*100

	if DJData.playerChl or DJData.playerCzm:
		playerC.winAllCount += 1
	playerC.winAC_ratio = (playerC.winAllCount*1.0 / playerC.gameAllCount*1.0)*100

	if DJData.playerDhl or DJData.playerDzm:
		playerD.winAllCount += 1
	playerD.winAC_ratio = (playerD.winAllCount*1.0 / playerD.gameAllCount*1.0)*100

	if DJData.playerAfc or DJData.playerAtp:
		playerA.loseAllCount += 1
	playerA.lAC_ratio = (playerA.loseAllCount*1.0 / playerA.gameAllCount*1.0)*100

	if DJData.playerBfc or DJData.playerBtp:
		playerB.loseAllCount += 1
	playerB.lAC_ratio = (playerB.loseAllCount*1.0 / playerB.gameAllCount*1.0)*100

	if DJData.playerCfc or DJData.playerCtp:
		playerC.loseAllCount += 1
	playerC.lAC_ratio = (playerC.loseAllCount*1.0 / playerC.gameAllCount*1.0)*100

	if DJData.playerDfc or DJData.playerDtp:
		playerD.loseAllCount += 1
	playerD.lAC_ratio = (playerD.loseAllCount*1.0 / playerD.gameAllCount*1.0)*100

	if DJData.playerAlz:
		playerA.lizhiAllCount += 1
	playerA.lzAC_ratio = (playerA.lizhiAllCount*1.0 / playerA.gameAllCount*1.0)*100

	if DJData.playerBlz:
		playerB.lizhiAllCount += 1
	playerB.lzAC_ratio = (playerB.lizhiAllCount*1.0 / playerB.gameAllCount*1.0)*100

	if DJData.playerClz:
		playerC.lizhiAllCount += 1
	playerC.lzAC_ratio = (playerC.lizhiAllCount*1.0 / playerC.gameAllCount*1.0)*100

	if DJData.playerDlz:
		playerD.lizhiAllCount += 1
	playerD.lzAC_ratio = (playerD.lizhiAllCount*1.0 / playerD.gameAllCount*1.0)*100

	if DJData.playerAfl:
		playerA.fuluAllCount += 1
	playerA.flAC_ratio = (playerA.fuluAllCount*1.0 / playerA.gameAllCount*1.0)*100

	if DJData.playerBfl:
		playerB.fuluAllCount += 1
	playerB.flAC_ratio = (playerB.fuluAllCount*1.0 / playerB.gameAllCount*1.0)*100

	if DJData.playerCfl:
		playerC.fuluAllCount += 1
	playerC.flAC_ratio = (playerC.fuluAllCount*1.0 / playerC.gameAllCount*1.0)*100

	if DJData.playerDfl:
		playerD.fuluAllCount += 1
	playerD.flAC_ratio = (playerD.fuluAllCount*1.0 / playerD.gameAllCount*1.0)*100

	if DJData.playerAtp:
		playerA.tingpaiAllCount += 1
	playerA.tpAC_ratio = (playerA.tingpaiAllCount*1.0 / playerA.gameAllCount*1.0)*100

	if DJData.playerBtp:
		playerB.tingpaiAllCount += 1
	playerB.tpAC_ratio = (playerB.tingpaiAllCount*1.0 / playerB.gameAllCount*1.0)*100

	if DJData.playerCtp:
		playerC.tingpaiAllCount += 1
	playerC.tpAC_ratio = (playerC.tingpaiAllCount*1.0 / playerC.gameAllCount*1.0)*100

	if DJData.playerDtp:
		playerD.tingpaiAllCount += 1
	playerD.tpAC_ratio = (playerD.tingpaiAllCount*1.0 / playerD.gameAllCount*1.0)*100

	if playerA.winAllCount != 0:
		playerA.avgWinPoint = playerA.winPoint_allCount / playerA.winAllCount
	if playerA.loseAllCount != 0:
		playerA.avgLosePoint = playerA.losePoint_allCount / playerA.loseAllCount

	if playerB.winAllCount != 0:
		playerB.avgWinPoint = playerB.winPoint_allCount / playerB.winAllCount
	if playerB.loseAllCount != 0:
		playerB.avgLosePoint = playerB.losePoint_allCount / playerB.loseAllCount

	if playerC.winAllCount != 0:
		playerC.avgWinPoint = playerC.winPoint_allCount / playerC.winAllCount
	if playerC.loseAllCount != 0:
		playerC.avgLosePoint = playerC.losePoint_allCount / playerC.loseAllCount

	if playerD.winAllCount != 0:
		playerD.avgWinPoint = playerD.winPoint_allCount / playerD.winAllCount
	if playerD.loseAllCount != 0:
		playerD.avgLosePoint = playerD.losePoint_allCount / playerD.loseAllCount

	playerA.save()
	playerB.save()
	playerC.save()
	playerD.save()

def UserRegTest(req, playerName):
	cursor = connection.cursor()
	sql = "select count(*) from blog_PlayerDate where name = '%s'" % playerName
	cursor.execute(sql)
	if int(cursor.fetchone()[0]) == 0:
		models.PlayerDate(
			name = playerName,
			level = 1,
			pt = 100,
			rank = 1500,
			gameAllCount = 0,
			bzAllCount=0,
			winAllCount=0,
			winAC_ratio=0,
			loseAllCount=0,
			lAC_ratio=0,
			fuluAllCount=0,
			flAC_ratio=0,
			lizhiAllCount=0,
			lzAC_ratio=0,
			tingpaiAllCount=0,
			tpAC_ratio=0,
			top_allCount=0,
			top_ratio=0,
			second_allCount=0,
			second_ratio=0,
			three_allCount=0,
			three_ratio=0,
			four_allCount=0,
			four_ratio=0,
			fly_allCount=0,
			fly_ratio=0,
			avgWinPoint=0,
			avgLosePoint=0,
			winPoint_allCount=0,
			losePoint_allCount=0
		).save()


def newGameOverInsertData(req):
	currentID = req.REQUEST.get('currentID','None')
	bz = models.BanZhuang.objects.get(banZhuangID=currentID)
	pA = models.PlayerDate.objects.get(name=bz.playerA)
	pB = models.PlayerDate.objects.get(name=bz.playerB)
	pC = models.PlayerDate.objects.get(name=bz.playerC)
	pD = models.PlayerDate.objects.get(name=bz.playerD)
	sql = "select count(*) from blog_duiju where banZhuangID = %s" % currentID
	cursor = connection.cursor()
	cursor.execute(sql)

	dj = models.DuiJu.objects.get(banZhuangID=currentID, duiJuID=int(cursor.fetchone()[0]))
	p1 = ''
	p2 = ''
	p3 = ''
	p4 = ''
	rankFlag = False
	rankAvg = (pA.rank + pB.rank + pC.rank+ pD.rank)/4
	if (pA.rank - pB.rank > 100 or pA.rank - pB.rank < 100) or \
	   (pA.rank - pC.rank > 100 or pA.rank - pC.rank < 100) or \
	   (pA.rank - pD.rank > 100 or pA.rank - pD.rank < 100) or \
	   (pB.rank - pC.rank > 100 or pB.rank - pC.rank < 100) or \
	   (pB.rank - pD.rank > 100 or pB.rank - pD.rank < 100) or \
	   (pC.rank - pD.rank > 100 or pC.rank - pD.rank < 100):
		rankFlag = True
	dict_p = {dj.playerAfinishPoint:pA, dj.playerBfinishPoint:pB, dj.playerCfinishPoint-1:pC, dj.playerDfinishPoint-2:pD}
	for i in range(1, 5):
		top=0
		top_play=None
		if(len(dict_p) > 1):
			top = max(tuple(dict_p))
			top_play = dict_p[top]
			del dict_p[top]
		else:
			top = list(dict_p)[0]
			top_play = dict_p[top]
		
		if i == 1:
			top_play.top_allCount += 1
			p1 = top_play.name
			top_play.pt += 30
			levelList = models.Level.objects.all().values()
			ptMax = levelList[top_play.level]
			if top_play.pt > ptMax:
				top_play.level += 1

			pTemp = 0
			if top_play.bzAllCount < 30:
				pTemp += 30
			elif top_play.bzAllCount < 50:
				pTemp += 24
			elif top_play.bzAllCount <= 80:
				pTemp += 16
			else:
				pTemp += 10

			if top_play.rank < rankAvg and rankFlag:
				pTemp *= 1.5

			top_play.rank += pTemp

		elif i == 2:
			top_play.second_allCount += 1
			p2 = top_play.name
			top_play.pt += 10

			levelList = models.Level.objects.all().values()
			ptMax = levelList[top_play.level]
			if top_play.pt > ptMax:
				top_play.level += 1

			pTemp = 0
			if top_play.bzAllCount < 30:
				pTemp += 10
			elif top_play.bzAllCount < 50:
				pTemp += 8
			elif top_play.bzAllCount <= 80:
				pTemp += 5
			else:
				pTemp += 2

			if top_play.rank < rankAvg and rankFlag:
				pTemp *= 1.5

			top_play.rank += pTemp

		elif i == 3:
			top_play.three_allCount += 1
			p3 = top_play.name

			pTemp = 0
			if top_play.bzAllCount < 30:
				pTemp += 10
			elif top_play.bzAllCount < 50:
				pTemp += 8
			elif top_play.bzAllCount <= 80:
				pTemp += 5
			else:
				pTemp += 2

			if top_play.rank > rankAvg and rankFlag:
				pTemp *= 1.5

			top_play.rank -= pTemp
		else:
			top_play.four_allCount += 1
			p4 = top_play.name
			top_play.pt -= 40

			if top_play.pt < 0:
				levelList = models.Level.objects.all().values()
				ptMax = levelList[top_play.level-1 if top_play.level > 1 else top_play.level]
				top_play.level -= 1
				top_play.pt = ptMax/2;

			pTemp = 0
			if top_play.bzAllCount < 30:
				pTemp += 30
			elif top_play.bzAllCount < 50:
				pTemp += 24
			elif top_play.bzAllCount <= 80:
				pTemp += 16
			else:
				pTemp += 10

			if top_play.rank > rankAvg and rankFlag:
				pTemp *= 1.5

			top_play.rank -= pTemp
		if top < 0:
			top_play.fly_allCount += 1
		top_play.bzAllCount += 1
		top_play.top_ratio = float(top_play.top_allCount)/top_play.bzAllCount*100
		top_play.second_ratio = float(top_play.second_allCount)/top_play.bzAllCount*100
		top_play.three_ratio = float(top_play.three_allCount)/top_play.bzAllCount*100
		top_play.four_ratio = float(top_play.four_allCount)/top_play.bzAllCount*100
		top_play.fly_ratio = float(top_play.fly_allCount)/top_play.bzAllCount*100
		top_play.save()
	
	return render_to_response('index.html', {'title':'Main',
											 'winPlayer1':p1,
											 'winPlayer2':p2, 
											 'winPlayer3':p3, 
											 'winPlayer4':p4})


def IsLianZhuang(sjData):
	if ((sjData.playerAzj and (sjData.playerAzj or sjData.playerAhl)) or (not sjData.playerAfc and not sjData.playerAtq and (sjData.playerAlz or sjData.playerAtp))) or \
	   ((sjData.playerBzj and (sjData.playerBzj or sjData.playerBhl)) or (not sjData.playerBfc and not sjData.playerBtq and (sjData.playerBlz or sjData.playerBtp))) or \
	   ((sjData.playerCzj and (sjData.playerCzj or sjData.playerChl)) or (not sjData.playerCfc and not sjData.playerCtq and (sjData.playerClz or sjData.playerCtp))) or \
	   ((sjData.playerDzj and (sjData.playerDzj or sjData.playerDhl)) or (not sjData.playerDfc and not sjData.playerDtq and (sjData.playerDlz or sjData.playerDtp))):
		return True
	return False

def ShangJuNotZhuangWin(sjData):
	if ((sjData.playerAhl or sjData.playerAzm) and sjData.playerAzj) or \
	   ((sjData.playerBhl or sjData.playerBzm) and sjData.playerBzj) or \
	   ((sjData.playerChl or sjData.playerCzm) and sjData.playerCzj) or \
	   ((sjData.playerDhl or sjData.playerDzm) and sjData.playerDzj):
		return False
	elif ((sjData.playerAtp or sjData.playerAlz) and sjData.playerAzj) or \
		 ((sjData.playerBtp or sjData.playerBlz) and sjData.playerBzj) or \
	     ((sjData.playerCtp or sjData.playerClz) and sjData.playerCzj) or \
	     ((sjData.playerDtp or sjData.playerDlz) and sjData.playerDzj):
	     return False
	else:
		return True

def ShangJuWinNotMe(req, sjData):
	if (sjData.playerAtp or sjData.playerAlz and not sjData.playerAzj and 'None' != req.REQUEST.get('cb_A_8', 'None') and ('None' != req.REQUEST.get('cb_A_0', 'None') or 'None' != req.REQUEST.get('cb_A_1', 'None')) or ('None' != req.REQUEST.get('cb_lz', 'None') and ('None' != req.REQUEST.get('cb_A_4', 'None') or 'None' != req.REQUEST.get('cb_A_7', 'None')))) or \
	   (sjData.playerBtp or sjData.playerBlz and not sjData.playerBzj and 'None' != req.REQUEST.get('cb_B_8', 'None') and ('None' != req.REQUEST.get('cb_B_0', 'None') or 'None' != req.REQUEST.get('cb_B_1', 'None')) or ('None' != req.REQUEST.get('cb_lz', 'None') and ('None' != req.REQUEST.get('cb_B_4', 'None') or 'None' != req.REQUEST.get('cb_B_7', 'None')))) or \
	   (sjData.playerCtp or sjData.playerClz and not sjData.playerCzj and 'None' != req.REQUEST.get('cb_C_8', 'None') and ('None' != req.REQUEST.get('cb_C_0', 'None') or 'None' != req.REQUEST.get('cb_C_1', 'None')) or ('None' != req.REQUEST.get('cb_lz', 'None') and ('None' != req.REQUEST.get('cb_C_4', 'None') or 'None' != req.REQUEST.get('cb_C_7', 'None')))) or \
	   (sjData.playerDtp or sjData.playerDlz and not sjData.playerDzj and 'None' != req.REQUEST.get('cb_D_8', 'None') and ('None' != req.REQUEST.get('cb_D_0', 'None') or 'None' != req.REQUEST.get('cb_D_1', 'None')) or ('None' != req.REQUEST.get('cb_lz', 'None') and ('None' != req.REQUEST.get('cb_D_4', 'None') or 'None' != req.REQUEST.get('cb_D_7', 'None')))):
		return False
	return True
 
