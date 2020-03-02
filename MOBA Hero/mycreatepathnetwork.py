'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''
import sys ,pygame ,math ,numpy ,random ,time ,copy ,operator #line:19
from pygame .locals import *#line:20
from constants import *#line:22
from utils import *#line:23
from core import *#line:24
def myCreatePathNetwork (O0OO0OO000O00O000 ,OOO0O0O0000OO00O0 =None ):#line:30
	O0OOO0O0OO0000O0O =[]#line:31
	O000O0O00OO0O0O00 =[]#line:32
	OOO0O0OO000O00000 =[]#line:33
	OOOOOO0000OO0OO00 =O0OO0OO000O00O000 .getLines ()[4 :]#line:35
	O0O0O0OOO0OOO0OO0 =set (O0OO0OO000O00O000 .getLines ())#line:36
	O000OOOO00O00OO00 =O0OO0OO000O00O000 .getPoints ()#line:37
	OOOO0O0O0000000O0 =O0OO0OO000O00O000 .getObstacles ()#line:38
	O0O00O0OOO000O0O0 =len (O000OOOO00O00OO00 )#line:39
	O0OOO000O0OOO00OO ={}#line:40
	OOO00000O00O0OOOO =set ()#line:41
	for O0OO00OO000O00000 in range (O0O00O0OOO000O0O0 -2 ):#line:44
		OO00OOO0O000OO000 =O000OOOO00O00OO00 [O0OO00OO000O00000 ]#line:45
		for OO00OO0O000OOO0OO in range (O0OO00OO000O00000 +1 ,O0O00O0OOO000O0O0 -1 ):#line:46
			OOO0O0O00000O000O =O000OOOO00O00OO00 [OO00OO0O000OOO0OO ]#line:47
			if foooaa (O0OO0OO000O00O000 ,OO00OOO0O000OO000 ,OOO0O0O00000O000O ,O0O0O0OOO0OOO0OO0 )is None :#line:48
				for OOOOO000O0O0OO0OO in range (OO00OO0O000OOO0OO +1 ,O0O00O0OOO000O0O0 ):#line:49
					O00OOO00O00000O0O =O000OOOO00O00OO00 [OOOOO000O0O0OO0OO ]#line:50
					if foooaa (O0OO0OO000O00O000 ,OOO0O0O00000O000O ,O00OOO00O00000O0O ,O0O0O0OOO0OOO0OO0 )is None and foooaa (O0OO0OO000O00O000 ,O00OOO00O00000O0O ,OO00OOO0O000OO000 ,O0O0O0OOO0OOO0OO0 )is None :#line:51
						OO00000O000000O0O =(OO00OOO0O000OO000 ,OOO0O0O00000O000O ,O00OOO00O00000O0O )#line:52
						OOO0OOO0O00O0OOOO =ManualObstacle (OO00000O000000O0O )#line:53
						OO0OO00OOO000O0OO =True #line:56
						if OO0OO00OOO000O0OO :#line:57
							for O0OO0OOO0O00O00O0 in OOOO0O0O0000000O0 :#line:58
								O0OOOO0O0OOO00O00 =O0OO0OOO0O00O00O0 .getPoints ()#line:59
								if len (O0OOOO0O0OOO00O00 )>=3 :#line:60
									O00O00O00O0OO0OOO =foooab (O0OO0OOO0O00O00O0 .getPoints ())#line:61
									if foooc (O00O00O00O0OO0OOO ,OO00000O000000O0O ):#line:62
										OO0OO00OOO000O0OO =False #line:63
										break #line:64
						if OO0OO00OOO000O0OO :#line:66
							OOO00000O00O0OOOO .add (OOO0OOO0O00O0OOOO )#line:67
							for O0O0OO00O00OOO0O0 in [(OO00OOO0O000OO000 ,OOO0O0O00000O000O ),(OOO0O0O00000O000O ,O00OOO00O00000O0O ),(O00OOO00O00000O0O ,OO00OOO0O000OO000 )]:#line:69
								OOO0O00OOO0OOO000 =False #line:70
								O0OO0O0OOOOO00OOO =set (O0O0OO00O00OOO0O0 )#line:71
								for OO0OO0OO0O0OO00OO in OOOOOO0000OO0OO00 :#line:72
									if set (OO0OO0OO0O0OO00OO )==O0OO0O0OOOOO00OOO :#line:73
										OOO0O00OOO0OOO000 =True #line:74
										break #line:75
								if not OOO0O00OOO0OOO000 :#line:76
									if O0O0OO00O00OOO0O0 in O0OOO000O0OOO00OO :#line:77
										O0OOO000O0OOO00OO [O0O0OO00O00OOO0O0 ].append (OOO0OOO0O00O0OOOO )#line:78
									else :#line:79
										OOOOOO00O00000O00 =(O0O0OO00O00OOO0O0 [1 ],O0O0OO00O00OOO0O0 [0 ])#line:80
										if OOOOOO00O00000O00 in O0OOO000O0OOO00OO :#line:81
											O0OOO000O0OOO00OO [OOOOOO00O00000O00 ].append (OOO0OOO0O00O0OOOO )#line:82
										else :#line:83
											O0OOO000O0OOO00OO [O0O0OO00O00OOO0O0 ]=[OOO0OOO0O00O0OOOO ]#line:84
								O0O0O0OOO0OOO0OO0 .add (O0O0OO00O00OOO0O0 )#line:85
	O0O0O00OOOOOOO0O0 =[]#line:88
	for O0O0OO00O00OOO0O0 in O0OOO000O0OOO00OO :#line:89
		if len (O0OOO000O0OOO00OO [O0O0OO00O00OOO0O0 ])>1 :#line:90
			OOOOOO0O0O0O0OO0O =O0OOO000O0OOO00OO [O0O0OO00O00OOO0O0 ][0 ]#line:91
			OOOOOO000O0O00000 =O0OOO000O0OOO00OO [O0O0OO00O00OOO0O0 ][1 ]#line:92
			O00OOOOO00O000O00 =list (OOOOOO0O0O0O0OO0O .getPoints ())#line:93
			OOOO0OOO0O00OOO00 =list (OOOOOO000O0O00000 .getPoints ())#line:94
			OOOO00O00O0O0O0OO =OOOOOO0O0O0O0OO0O .getLines ()#line:95
			OO00OO0O00O00O00O =OOOOOO000O0O00000 .getLines ()#line:96
			O00000000000O0OO0 =len (O00OOOOO00O000O00 )#line:97
			OO0OO00OO0O000O0O =len (OOOO0OOO0O00OOO00 )#line:98
			OO0O0OOOO0OOO00O0 ,OO00O0OO0000O0O0O =fooou (O0O0OO00O00OOO0O0 ,OOOOOO0O0O0O0OO0O )#line:100
			O0OO00O0O00OO000O ,O0O0OO00OO000000O =fooou (O0O0OO00O00OOO0O0 ,OOOOOO000O0O00000 )#line:101
			if OO00O0OO0000O0O0O ==O0O0OO00OO000000O :#line:102
				OOOO0OOO0O00OOO00 .reverse ()#line:103
				O0OO00O0O00OO000O =OO0OO00OO0O000O0O -O0OO00O0O00OO000O -2 #line:104
				if O0OO00O0O00OO000O ==-1 :#line:105
					O0OO00O0O00OO000O =OO0OO00OO0O000O0O -1 #line:106
			O00OOO0OOO0OOO0O0 =None #line:109
			if OO0O0OOOO0OOO00O0 ==O00000000000O0OO0 -1 :#line:110
				O00OOO0OOO0OOO0O0 =copy .copy (O00OOOOO00O000O00 )#line:111
			else :#line:112
				O00OOO0OOO0OOO0O0 =O00OOOOO00O000O00 [OO0O0OOOO0OOO00O0 +1 :]+O00OOOOO00O000O00 [:OO0O0OOOO0OOO00O0 +1 ]#line:113
			if O0OO00O0O00OO000O ==OO0OO00OO0O000O0O -1 :#line:114
				O00OOO0OOO0OOO0O0 +=OOOO0OOO0O00OOO00 [1 :OO0OO00OO0O000O0O -1 ]#line:115
			else :#line:116
				O00OOO0OOO0OOO0O0 +=OOOO0OOO0O00OOO00 [O0OO00O0O00OO000O +2 :]+OOOO0OOO0O00OOO00 [:O0OO00O0O00OO000O ]#line:117
			if isConvex (O00OOO0OOO0OOO0O0 ):#line:119
				O0O00O00O0O0O00O0 =ManualObstacle (O00OOO0OOO0OOO0O0 )#line:120
				fooot (O0OOO000O0OOO00OO ,OOOOOO0O0O0O0OO0O ,OOOO00O00O0O0O0OO ,O0O00O00O0O0O00O0 )#line:121
				fooot (O0OOO000O0OOO00OO ,OOOOOO000O0O00000 ,OO00OO0O00O00O00O ,O0O00O00O0O0O00O0 )#line:122
				OOO00000O00O0OOOO .remove (OOOOOO0O0O0O0OO0O )#line:124
				OOO00000O00O0OOOO .remove (OOOOOO000O0O00000 )#line:125
				OOO00000O00O0OOOO .add (O0O00O00O0O0O00O0 )#line:126
				O0O0O00OOOOOOO0O0 .append (O0O0OO00O00OOO0O0 )#line:127
	for O0O0OO00O00OOO0O0 in O0O0O00OOOOOOO0O0 :#line:129
		O0OOO000O0OOO00OO .pop (O0O0OO00O00OOO0O0 )#line:130
	O00000OOOOOOO0OO0 =set ()#line:135
	O0O0OO0O00O0OOOO0 =[]#line:136
	for O000O0OO0O00O00O0 in OOO00000O00O0OOOO :#line:137
		OOO000O00O0000000 =O000O0OO0O00O00O0 .getPoints ()#line:138
		OOO0O0OO000O00000 .append (OOO000O00O0000000 )#line:139
		O0OO00OOO0O000O00 =O000O0OO0O00O00O0 .getLines ()#line:140
		OO0O0000O0OO00000 =[(O0OO0O0O0OO0O0000 [0 ],O0OO0O0O0OO0O0000 [1 ],[foooz (O0OO0O0O0OO0O0000 )]+fooow (O0OO0O0O0OO0O0000 ))for O0OO0O0O0OO0O0000 in O0OO00OOO0O000O00 if O0OO0O0O0OO0O0000 in O0OOO000O0OOO00OO or (O0OO0O0O0OO0O0000 [1 ],O0OO0O0O0OO0O0000 [0 ])in O0OOO000O0OOO00OO ]#line:145
		O00O00O00O0OO0OOO =foooab (OOO000O00O0000000 )#line:146
		OO0OOO0OO00O0OOOO =len (OOO000O00O0000000 )#line:147
		if OO0OOO0OO00O0OOOO >3 :#line:150
			for OOOO00O0O0O0OOOOO ,OOO000O000000O0O0 ,OO0OOOOOOO0000O00 in OO0O0000O0OO00000 :#line:152
				for O0OO00OO000O00000 ,O0O0OO0OOO0O0OOO0 in enumerate (OO0OOOOOOO0000O00 ):#line:154
					O0OO0O000000OO00O =(O0O0OO0OOO0O0OOO0 ,O00O00O00O0OO0OOO )#line:155
					if foooq (O0OO0O000000OO00O ,O0OO0OO000O00O000 ,O0OO0OO000O00O000 .agent ):#line:156
						O0O0OO0O00O0OOOO0 .append (O0OO0O000000OO00O )#line:158
						O00000OOOOOOO0OO0 .add (O0O0OO0OOO0O0OOO0 )#line:159
						O00000OOOOOOO0OO0 .add (O00O00O00O0OO0OOO )#line:160
						'''
						if i > 0:
							path2 = (point1, pointTries1[0])
							allEdges.append(path2)
							nodeSet.add(point1)
							nodeSet.add(pointTries1[0])
						if j > 0:
							path2 = (point2, pointTries2[0])
							allEdges.append(path2)
							nodeSet.add(point2)
							nodeSet.add(pointTries2[0])
						'''#line:174
						break #line:175
		for O0OOO000O0O000O00 ,OO00O0O000OO0OO0O ,OO0OO00OOO000O0O0 in OO0O0000O0OO00000 :#line:178
			for O0O00O0OOOOO00OO0 ,OOO0000000OOO000O ,O00OO0OO00OOOOOO0 in OO0O0000O0OO00000 :#line:179
				if OO0OO00OOO000O0O0 !=O00OO0OO00OOOOOO0 :#line:181
					O000000O0OOOO000O =False #line:182
					for O0OO00OO000O00000 ,OO0OO000OOOO0O0O0 in enumerate (OO0OO00OOO000O0O0 ):#line:184
						if not O000000O0OOOO000O :#line:185
							for OO00OO0O000OOO0OO ,OOOOO0OO00OOOO000 in enumerate (O00OO0OO00OOOOOO0 ):#line:187
								if not O000000O0OOOO000O :#line:188
									O0OO0O000000OO00O =(OO0OO000OOOO0O0O0 ,OOOOO0OO00OOOO000 )#line:189
									if foooq (O0OO0O000000OO00O ,O0OO0OO000O00O000 ,O0OO0OO000O00O000 .agent )and (O0OOO000O0O000O00 ==O0O00O0OOOOO00OO0 or O0OOO000O0O000O00 ==OOO0000000OOO000O or OO00O0O000OO0OO0O ==O0O00O0OOOOO00OO0 or OO00O0O000OO0OO0O ==OOO0000000OOO000O ):#line:191
										O0O0OO0O00O0OOOO0 .append (O0OO0O000000OO00O )#line:192
										O00000OOOOOOO0OO0 .add (OO0OO000OOOO0O0O0 )#line:193
										O00000OOOOOOO0OO0 .add (OOOOO0OO00OOOO000 )#line:194
										O000000O0OOOO000O =True #line:195
										if O0OO00OO000O00000 >0 :#line:198
											O0OOOO00OO0OOOO0O =(OO0OO000OOOO0O0O0 ,OO0OO00OOO000O0O0 [0 ])#line:199
											O0O0OO0O00O0OOOO0 .append (O0OOOO00OO0OOOO0O )#line:200
											O00000OOOOOOO0OO0 .add (OO0OO000OOOO0O0O0 )#line:201
											O00000OOOOOOO0OO0 .add (OO0OO00OOO000O0O0 [0 ])#line:202
										if OO00OO0O000OOO0OO >0 :#line:203
											O0OOOO00OO0OOOO0O =(OOOOO0OO00OOOO000 ,O00OO0OO00OOOOOO0 [0 ])#line:204
											O0O0OO0O00O0OOOO0 .append (O0OOOO00OO0OOOO0O )#line:205
											O00000OOOOOOO0OO0 .add (OOOOO0OO00OOOO000 )#line:206
											O00000OOOOOOO0OO0 .add (O00OO0OO00OOOOOO0 [0 ])#line:207
		'''
		validPoints = [foooz(line) for line in lines if line in lineDict or (line[1], line[0]) in lineDict]
		centroid = foooab(polygonPoints)
		validLength = len(validPoints)
		polygonLength = len(polygonPoints)
		for i in range(validLength):
			path = (validPoints[i], centroid)
			if polygonLength > 3 and foooq(path, world, world.agent):
				# Route borders through the centroid in higher order polygons.
				allEdges.append(path)
				nodeSet.add(validPoints[i])
				nodeSet.add(centroid)
			else:
				# Link borders directly in triangles or if the centroid is unusable.
				for j in range(validLength):
					if i != j:
						path = (validPoints[i], validPoints[j])
						if foooq(path, world, world.agent):
							allEdges.append(path)
							nodeSet.add(validPoints[i])
							nodeSet.add(validPoints[j])
		'''#line:233
	O0O000OO0OO0O0OOO =findClosestUnobstructed (O0OO0OO000O00O000 .agent .position ,O00000OOOOOOO0OO0 ,O0OO0OO000O00O000 .getLines ())#line:237
	O00OO00OOOO00O0O0 =set ([O0O000OO0OO0O0OOO ])#line:238
	O00000OOOOOOO0OO0 .clear ()#line:239
	while len (O00OO00OOOO00O0O0 )>0 :#line:240
		O000O0O00O0OO00OO =set ()#line:241
		for OOO0000O000000OOO in O00OO00OOOO00O0O0 :#line:242
			O00O000OO0O0OO00O =[]#line:243
			for OO000O0O000O0000O in O0O0OO0O00O0OOOO0 :#line:244
				OO000O0OOO0OOOO00 =False #line:245
				if OO000O0O000O0000O [0 ]==OOO0000O000000OOO :#line:246
					O000O0O00O0OO00OO .add (OO000O0O000O0000O [1 ])#line:247
					OO000O0OOO0OOOO00 =True #line:248
				elif OO000O0O000O0000O [1 ]==OOO0000O000000OOO :#line:249
					O000O0O00O0OO00OO .add (OO000O0O000O0000O [0 ])#line:250
					OO000O0OOO0OOOO00 =True #line:251
				if OO000O0OOO0OOOO00 :#line:252
					O000O0O00OO0O0O00 .append (OO000O0O000O0000O )#line:253
					O00O000OO0O0OO00O .append (OO000O0O000O0000O )#line:254
			for OO000O0O000O0000O in O00O000OO0O0OO00O :#line:255
				O0O0OO0O00O0OOOO0 .remove (OO000O0O000O0000O )#line:256
		O00000OOOOOOO0OO0 .update (O00OO00OOOO00O0O0 )#line:257
		O00OO00OOOO00O0O0 =O000O0O00O0OO00OO #line:258
	O0OOO0O0OO0000O0O =list (O00000OOOOOOO0OO0 )#line:260
	return O0OOO0O0OO0000O0O ,O000O0O00OO0O0O00 ,OOO0O0OO000O00000 #line:262
def foooac (O0OOOOO00000OOOOO ,OO0OO000O00O0O0OO ):#line:265
	for O00O0O00O00000O0O in OO0OO000O00O0O0OO :#line:266
		O0OOO00O00OO0OOO0 =foooab (O00O0O00O00000O0O .getPoints ())#line:267
		drawCross (O0OOOOO00000OOOOO .debug ,O0OOO00O00OO0OOO0 ,(255 ,0 ,0 ))#line:268
def foooab (OO00OOOO0OO0OOOOO ):#line:271
	O0OO00000000OO0O0 =O0O00O0000O00OO0O =0 #line:272
	OO0OO00O0000O00O0 =len (OO00OOOO0OO0OOOOO )#line:273
	for OOO0000000OO00OOO in OO00OOOO0OO0OOOOO :#line:274
		O0OO00000000OO0O0 +=OOO0000000OO00OOO [0 ]#line:275
		O0O00O0000O00OO0O +=OOO0000000OO00OOO [1 ]#line:276
	OO0O000O000OO000O =(O0OO00000000OO0O0 /OO0OO00O0000O00O0 ,O0O00O0000O00OO0O /OO0OO00O0000O00O0 )#line:277
	return OO0O000O000OO000O #line:278
def foooaa (O0OO0OOO00OO00OOO ,OO000OOO0OO0O000O ,OOO00000OO0000OO0 ,O0OO0O0O00O0O0O0O ):#line:281
	for O000OOOOOO0OO0O0O in O0OO0OOO00OO00OOO .getObstacles ():#line:283
		OO0000OO0OO0O0OO0 =O000OOOOOO0OO0O0O .getPoints ()#line:284
		OO0O0OOO000OO000O =len (OO0000OO0OO0O0OO0 )#line:285
		OOO000O000OOO00O0 =-1 #line:286
		for O0O0OOOO0OO00OOO0 in range (OO0O0OOO000OO000O ):#line:287
			if OO0000OO0OO0O0OO0 [O0O0OOOO0OO00OOO0 ]==OO000OOO0OO0O000O or OO0000OO0OO0O0OO0 [O0O0OOOO0OO00OOO0 ]==OOO00000OO0000OO0 :#line:289
				if OOO000O000OOO00O0 ==-1 :#line:290
					OOO000O000OOO00O0 =O0O0OOOO0OO00OOO0 #line:291
				else :#line:292
					O00O0O0000000O000 =O0O0OOOO0OO00OOO0 -OOO000O000OOO00O0 #line:293
					if O00O0O0000000O000 >1 and O00O0O0000000O000 <OO0O0OOO000OO000O -1 :#line:294
						OO00O000O000O0O00 =foooy (OO000OOO0OO0O000O ,OOO00000OO0000OO0 )#line:295
						if O000OOOOOO0OO0O0O .pointInside (OO00O000O000O0O00 ):#line:296
							return OO00O000O000O0O00 #line:297
						else :#line:298
							OOO0000O000O0O000 =O000OOOOOO0OO0O0O .getLines ()#line:300
							for O00O0O0OO00OO00OO in OOO0000O000O0O000 :#line:301
								OO000OO000O0O0OOO =True #line:302
								for OOO0OO0O0O0000000 in O00O0O0OO00OO00OO :#line:303
									if OOO0OO0O0O0000000 ==OO000OOO0OO0O000O or OOO0OO0O0O0000000 ==OOO00000OO0000OO0 :#line:304
										OO000OO000O0O0OOO =False #line:305
										break #line:306
								if OO000OO000O0O0OOO :#line:307
									O000OO0O0O0OO00O0 =foooi (OO000OOO0OO0O000O ,OOO00000OO0000OO0 ,O00O0O0OO00OO00OO )#line:308
									if O000OO0O0O0OO00O0 !=None :#line:309
										return O000OO0O0O0OO00O0 #line:310
	return foooh (OO000OOO0OO0O000O ,OOO00000OO0000OO0 ,fooov ([OO000OOO0OO0O000O ,OOO00000OO0000OO0 ],O0OO0O0O00O0O0O0O ))#line:311
def foooz (O00O00OOOO0O0O0O0 ):#line:314
	return foooy (O00O00OOOO0O0O0O0 [0 ],O00O00OOOO0O0O0O0 [1 ])#line:315
def foooy (O0000O0O00O000OO0 ,O0000OO00O0O0O000 ):#line:318
	return ((O0000O0O00O000OO0 [0 ]+O0000OO00O0O0O000 [0 ])/2 ,(O0000O0O00O000OO0 [1 ]+O0000OO00O0O0O000 [1 ])/2 )#line:319
def fooox (O00O00OOOOO0O0OOO ,OO0O00OOOO0O0000O ):#line:322
	return [(O00O00OOOOO0O0OOO [0 ]+(OO0O00OOOO0O0000O [0 ]-O00O00OOOOO0O0OOO [0 ])*.25 ,O00O00OOOOO0O0OOO [1 ]+(OO0O00OOOO0O0000O [1 ]-O00O00OOOOO0O0OOO [1 ])*.25 ),(O00O00OOOOO0O0OOO [0 ]+(OO0O00OOOO0O0000O [0 ]-O00O00OOOOO0O0OOO [0 ])*.75 ,O00O00OOOOO0O0OOO [1 ]+(OO0O00OOOO0O0000O [1 ]-O00O00OOOOO0O0OOO [1 ])*.75 )]#line:323
def fooow (O00OO000OOO0O00OO ):#line:325
	return fooox (O00OO000OOO0O00OO [0 ],O00OO000OOO0O00OO [1 ])#line:326
def fooov (OO0OOO0OOOO00000O ,OOOOOO00OOO0OO0OO ):#line:329
	OO00O0O0000O0O000 =[]#line:330
	for O00O0O000O000O00O in OOOOOO00OOO0OO0OO :#line:331
		for O00OOO0O0000OOO0O in OO0OOO0OOOO00000O :#line:332
			O0O0O00O00O000000 =True #line:333
			for O000O0OOO0O0O0OO0 in O00O0O000O000O00O :#line:334
				if O00OOO0O0000OOO0O ==O000O0OOO0O0O0OO0 :#line:335
					O0O0O00O00O000000 =False #line:336
					break #line:337
			if O0O0O00O00O000000 :#line:338
				OO0OO00OO000O0O0O =foooi (O00OOO0O0000OOO0O ,(-10 ,-10 ),O00O0O000O000O00O )#line:339
				if OO0OO00OO000O0O0O !=None :#line:340
					for O00OO0O0000OO00OO in range (2 ):#line:341
						if (foooj (O00OOO0O0000OOO0O [O00OO0O0000OO00OO ],OO0OO00OO000O0O0O [O00OO0O0000OO00OO ],OO0OO00OO000O0O0O [O00OO0O0000OO00OO ])):#line:342
							O0O0O00O00O000000 =False #line:343
							break #line:344
			if not O0O0O00O00O000000 :#line:345
				break #line:346
		if O0O0O00O00O000000 :#line:347
			OO00O0O0000O0O000 .append (O00O0O000O000O00O )#line:348
	return OO00O0O0000O0O000 #line:349
def fooou (OOOOOO0OOOO000OOO ,OO00O0O000000O00O ):#line:353
	O0OO0OO00OO0O0OOO =OO00O0O000000O00O .getPoints ()#line:354
	O0O0000O00OO0OO0O =len (O0OO0OO00OO0O0OOO )#line:355
	for OO0O00O0O00000000 in range (O0O0000O00OO0OO0O ):#line:356
		if O0OO0OO00OO0O0OOO [OO0O00O0O00000000 ]==OOOOOO0OOOO000OOO [0 ]:#line:357
			if O0OO0OO00OO0O0OOO [OO0O00O0O00000000 +1 ]==OOOOOO0OOOO000OOO [1 ]:#line:358
				return OO0O00O0O00000000 ,True #line:359
			else :#line:360
				return O0O0000O00OO0OO0O -1 ,False #line:361
		elif O0OO0OO00OO0O0OOO [OO0O00O0O00000000 ]==OOOOOO0OOOO000OOO [1 ]:#line:362
			if O0OO0OO00OO0O0OOO [OO0O00O0O00000000 +1 ]==OOOOOO0OOOO000OOO [0 ]:#line:363
				return OO0O00O0O00000000 ,False #line:364
			else :#line:365
				return O0O0000O00OO0OO0O -1 ,True #line:366
	return -1 ,True #line:367
def fooot (O00OO0O0OOOOO00OO ,O00O0O000O0O0OOOO ,OO0OOOOOOOO00O000 ,OO00O0OO000OO0OOO ):#line:370
	for OOOO0O00O000000OO in OO0OOOOOOOO00O000 :#line:371
		if OOOO0O00O000000OO in O00OO0O0OOOOO00OO :#line:372
			O00OO0O0OOOOO00OO [OOOO0O00O000000OO ]=[OO00O0OO000OO0OOO if O00O0O0OOO0O0O00O ==O00O0O000O0O0OOOO else O00O0O0OOO0O0O00O for O00O0O0OOO0O0O00O in O00OO0O0OOOOO00OO [OOOO0O00O000000OO ]]#line:373
		else :#line:374
			O00O0O00O0O0OO0OO =(OOOO0O00O000000OO [1 ],OOOO0O00O000000OO [0 ])#line:375
			if O00O0O00O0O0OO0OO in O00OO0O0OOOOO00OO :#line:376
				O00OO0O0OOOOO00OO [O00O0O00O0O0OO0OO ]=[OO00O0OO000OO0OOO if OOO00O0O0000000OO ==O00O0O000O0O0OOOO else OOO00O0O0000000OO for OOO00O0O0000000OO in O00OO0O0OOOOO00OO [O00O0O00O0O0OO0OO ]]#line:377
def fooos (O0O000OO00O0O0O0O ):#line:380
	OOO0OO00OO0OOOOOO =O0OO00O0000000OOO =O0O000OO00O0O0O0O [0 ][0 ]#line:381
	O00O00OO0000000OO =O0OOO00O00O0O0OO0 =O0O000OO00O0O0O0O [0 ][1 ]#line:382
	O0OO00O0OOO00O0O0 =len (O0O000OO00O0O0O0O )#line:383
	for OOOOOOO0OO000OO00 in range (1 ,O0OO00O0OOO00O0O0 ):#line:384
		OOO0OO00OO0OOOOOO =min (OOO0OO00OO0OOOOOO ,O0O000OO00O0O0O0O [OOOOOOO0OO000OO00 ][0 ])#line:385
		O0OO00O0000000OOO =max (O0OO00O0000000OOO ,O0O000OO00O0O0O0O [OOOOOOO0OO000OO00 ][0 ])#line:386
		O00O00OO0000000OO =min (O00O00OO0000000OO ,O0O000OO00O0O0O0O [OOOOOOO0OO000OO00 ][1 ])#line:387
		O0OOO00O00O0O0OO0 =max (O0OOO00O00O0O0OO0 ,O0O000OO00O0O0O0O [OOOOOOO0OO000OO00 ][1 ])#line:388
	return OOO0OO00OO0OOOOOO ,O00O00OO0000000OO ,O0OO00O0000000OOO ,O0OOO00O00O0O0OO0 #line:389
def foooq (O000OO0O00OOOO000 ,O000O00O00OO00OOO ,O0000OOO000OO0O0O ):#line:392
	O0OO0OO00O0O00000 =O0000OOO000OO0O0O .getMaxRadius ()#line:393
	O00OOO0OOO00000OO =numpy .matrix (O000OO0O00OOOO000 [0 ])#line:395
	OOO0OO0OO000000O0 =numpy .matrix (O000OO0O00OOOO000 [1 ])#line:396
	OO0OOOOO00OOO0OOO =OOO0OO0OO000000O0 -O00OOO0OOO00000OO #line:397
	O000OOO00000OOOO0 =fooop (OO0OOOOO00OOO0OOO )*O0OO0OO00O0O00000 #line:398
	OOOO0OOO0O00OOO0O =O000OOO00000OOOO0 *numpy .matrix ('0,1;-1,0')#line:399
	OO0OO00O0OO0O0O00 =[fooor (O00OOO0OOO00000OO -O000OOO00000OOOO0 +OOOO0OOO0O00OOO0O ),fooor (O00OOO0OOO00000OO -O000OOO00000OOOO0 -OOOO0OOO0O00OOO0O ),fooor (OOO0OO0OO000000O0 +O000OOO00000OOOO0 -OOOO0OOO0O00OOO0O ),fooor (OOO0OO0OO000000O0 +O000OOO00000OOOO0 +OOOO0OOO0O00OOO0O )]#line:403
	O0OO00O0OOO000000 =True #line:406
	for O0O00O0OOOOO00O00 in O000O00O00OO00OOO .obstacles :#line:407
		for O000OO0O00OOOO000 in O0O00O0OOOOO00O00 .getLines ():#line:408
			if foooi (OO0OO00O0OO0O0O00 [0 ],OO0OO00O0OO0O0O00 [3 ],O000OO0O00OOOO000 )!=None or foooi (OO0OO00O0OO0O0O00 [1 ],OO0OO00O0OO0O0O00 [2 ],O000OO0O00OOOO000 )!=None :#line:409
				O0OO00O0OOO000000 =False #line:410
				break #line:411
		if O0OO00O0OOO000000 and foooc (O0O00O0OOOOO00O00 .getPoints ()[0 ],OO0OO00O0OO0O0O00 ):#line:413
			O0OO00O0OOO000000 =False #line:414
		if not O0OO00O0OOO000000 :#line:415
			break #line:416
	return O0OO00O0OOO000000 #line:417
def fooop (OOOO0000000OOOOOO ):#line:420
	OO0O00OO00O0OOO00 =numpy .linalg .norm (OOOO0000000OOOOOO )#line:421
	if OO0O00OO00O0OOO00 ==0 :#line:422
		return OOOO0000000OOOOOO #line:423
	else :#line:424
		return OOOO0000000OOOOOO /OO0O00OO00O0OOO00 #line:425
def fooor (O0O0OO00O0O0OOOOO ):#line:428
	return O0O0OO00O0O0OOOOO .tolist ()[0 ]#line:429
def foooo (O000OO0OO0OOO0O00 ,OO00O0OO00O0O0O0O ):#line:432
	return (((OO00O0OO00O0O0O0O [0 ]-O000OO0OO0OOO0O00 [0 ])**2 )+((OO00O0OO00O0O0O0O [1 ]-O000OO0OO0OOO0O00 [1 ])**2 ))**0.5 #line:433
def fooon (OOOO0O0O00O0O000O ,O0OOO0OO0000O0O00 ):#line:436
	if (OOOO0O0O00O0O000O [0 ]!=O0OOO0OO0000O0O00 [0 ]):#line:438
		OOOO0O0OOOOO00O0O =(OOOO0O0O00O0O000O [1 ]-O0OOO0OO0000O0O00 [1 ])/float (OOOO0O0O00O0O000O [0 ]-O0OOO0OO0000O0O00 [0 ])#line:439
		return OOOO0O0OOOOO00O0O #line:440
	else :#line:441
		return None #line:442
def fooom (OOO0O0OO0OO0O00O0 ,OO0OO0OO0OO0O0OO0 ):#line:445
	return OOO0O0OO0OO0O00O0 [1 ]-(OO0OO0OO0OO0O0OO0 *OOO0O0OO0OO0O00O0 [0 ])#line:446
def foool (O0OOO000OOO0OO0O0 ,OOO0000O0O0O00OO0 ,OOO0OOOOO000OO0O0 ,OOO0000O00O00O0O0 ):#line:454
	O000OO0O0O0OOOOOO =fooon (O0OOO000OOO0OO0O0 ,OOO0000O0O0O00OO0 )#line:455
	OO000O00O00O000OO =fooon (OOO0OOOOO000OO0O0 ,OOO0000O00O00O0O0 )#line:456
	if (O000OO0O0O0OOOOOO !=OO000O00O00O000OO ):#line:459
		if (O000OO0O0O0OOOOOO is not None and OO000O00O00O000OO is not None ):#line:463
			O0O00OOOOOO0O000O =fooom (O0OOO000OOO0OO0O0 ,O000OO0O0O0OOOOOO )#line:465
			OOO0O0O0O0O0O0OO0 =fooom (OOO0OOOOO000OO0O0 ,OO000O00O00O000OO )#line:466
			O0OO0O00OOO0OO000 =(OOO0O0O0O0O0O0OO0 -O0O00OOOOOO0O000O )/float (O000OO0O0O0OOOOOO -OO000O00O00O000OO )#line:467
			O000000000000OOOO =(O000OO0O0O0OOOOOO *O0OO0O00OOO0OO000 )+O0O00OOOOOO0O000O #line:468
		else :#line:469
			if (O000OO0O0O0OOOOOO is None ):#line:471
				OOO0O0O0O0O0O0OO0 =fooom (OOO0OOOOO000OO0O0 ,OO000O00O00O000OO )#line:472
				O0OO0O00OOO0OO000 =O0OOO000OOO0OO0O0 [0 ]#line:473
				O000000000000OOOO =(OO000O00O00O000OO *O0OO0O00OOO0OO000 )+OOO0O0O0O0O0O0OO0 #line:474
			elif (OO000O00O00O000OO is None ):#line:476
				O0O00OOOOOO0O000O =fooom (O0OOO000OOO0OO0O0 ,O000OO0O0O0OOOOOO )#line:477
				O0OO0O00OOO0OO000 =OOO0OOOOO000OO0O0 [0 ]#line:478
				O000000000000OOOO =(O000OO0O0O0OOOOOO *O0OO0O00OOO0OO000 )+O0O00OOOOOO0O000O #line:479
			else :#line:480
				assert false #line:481
		return ((O0OO0O00OOO0OO000 ,O000000000000OOOO ),)#line:483
	else :#line:484
		O0O00OOOOOO0O000O ,OOO0O0O0O0O0O0OO0 =None ,None #line:489
		if O000OO0O0O0OOOOOO is not None :#line:490
			O0O00OOOOOO0O000O =fooom (O0OOO000OOO0OO0O0 ,O000OO0O0O0OOOOOO )#line:491
		if OO000O00O00O000OO is not None :#line:493
			OOO0O0O0O0O0O0OO0 =fooom (OOO0OOOOO000OO0O0 ,OO000O00O00O000OO )#line:494
		if O0O00OOOOOO0O000O ==OOO0O0O0O0O0O0OO0 :#line:497
			return O0OOO000OOO0OO0O0 ,OOO0000O0O0O00OO0 ,OOO0OOOOO000OO0O0 ,OOO0000O00O00O0O0 #line:498
		else :#line:499
			return None #line:500
def foook (OO0OOOO00000000O0 ,OO00OOO00O0000OOO ,O0OO00000O0O0O0O0 ,OO0O0OOO0O00OOO0O ):#line:510
	O00OOOO0OOO0000O0 =foool (OO0OOOO00000000O0 ,OO00OOO00O0000OOO ,O0OO00000O0O0O0O0 ,OO0O0OOO0O00OOO0O )#line:511
	if O00OOOO0OOO0000O0 is not None :#line:512
		O00OOOO0OOO0000O0 =O00OOOO0OOO0000O0 [0 ]#line:513
		if foooj (O00OOOO0OOO0000O0 [0 ],OO0OOOO00000000O0 [0 ],OO00OOO00O0000OOO [0 ])and foooj (O00OOOO0OOO0000O0 [1 ],OO0OOOO00000000O0 [1 ],OO00OOO00O0000OOO [1 ])and foooj (O00OOOO0OOO0000O0 [0 ],O0OO00000O0O0O0O0 [0 ],OO0O0OOO0O00OOO0O [0 ])and foooj (O00OOOO0OOO0000O0 [1 ],O0OO00000O0O0O0O0 [1 ],OO0O0OOO0O00OOO0O [1 ]):#line:514
			return O00OOOO0OOO0000O0 #line:515
	return None #line:516
def foooj (OOOO000O00O0OOO00 ,O0OO0O000OOO0OO0O ,OOO0OO0O0OO000OO0 ):#line:521
	return OOOO000O00O0OOO00 +EPSILON >=min (O0OO0O000OOO0OO0O ,OOO0OO0O0OO000OO0 )and OOOO000O00O0OOO00 -EPSILON <=max (O0OO0O000OOO0OO0O ,OOO0OO0O0OO000OO0 )#line:522
def foooi (O0O0OOOOO00O00OOO ,OO00OO00O000O0O00 ,O00OO0O00O0OOOOO0 ):#line:524
	return foook (O00OO0O00O0OOOOO0 [0 ],O00OO0O00O0OOOOO0 [1 ],O0O0OOOOO00O00OOO ,OO00OO00O000O0O00 )#line:525
def foooh (O0OO000OOO0O00O0O ,OO000000OOO000OOO ,O0O0OO0OO000O00OO ):#line:528
	for OO0OO00OO0000O00O in O0O0OO0OO000O00OO :#line:529
		O0OOO0OOO00OOO000 =foooi (O0OO000OOO0O00O0O ,OO000000OOO000OOO ,OO0OO00OO0000O00O )#line:530
		if O0OOO0OOO00OOO000 !=None :#line:531
			return O0OOO0OOO00OOO000 #line:532
	return None #line:533
def fooog (O0O0O0O0O0OO0O0O0 ,OO0OO00OOOOOO00O0 ,OO0O0O000O0OOO0OO ):#line:536
	if (O0O0O0O0O0OO0O0O0 ==OO0O0O000O0OOO0OO [0 ]and OO0OO00OOOOOO00O0 ==OO0O0O000O0OOO0OO [1 ])or (OO0OO00OOOOOO00O0 ==OO0O0O000O0OOO0OO [0 ]and O0O0O0O0O0OO0O0O0 ==OO0O0O000O0OOO0OO [1 ]):#line:538
		return O0O0O0O0O0OO0O0O0 #line:539
	if (O0O0O0O0O0OO0O0O0 ==OO0O0O000O0OOO0OO [0 ]or OO0OO00OOOOOO00O0 ==OO0O0O000O0OOO0OO [1 ])or (OO0OO00OOOOOO00O0 ==OO0O0O000O0OOO0OO [0 ]or O0O0O0O0O0OO0O0O0 ==OO0O0O000O0OOO0OO [1 ]):#line:541
		return None #line:542
	OO00OOO0OO0O00OOO =foook (OO0O0O000O0OOO0OO [0 ],OO0O0O000O0OOO0OO [1 ],O0O0O0O0O0OO0O0O0 ,OO0OO00OOOOOO00O0 )#line:544
	if OO00OOO0OO0O00OOO !=None :#line:545
		return OO00OOO0OO0O00OOO #line:546
	return None #line:547
def fooof (OOO000O00O000OOOO ,O000OOO00OOOO0O0O ,O00OO0OOOO0O00O00 ):#line:550
	for O00000O0O0OOO0O0O in O00OO0OOOO0O00O00 :#line:551
		OOO0OOOO00OOOOO00 =fooog (OOO000O00O000OOOO ,O000OOO00OOOO0O0O ,O00000O0O0OOO0O0O )#line:552
		if OOO0OOOO00OOOOO00 !=None :#line:553
			return OOO0OOOO00OOOOO00 #line:554
	return None #line:555
def foooe (O0000O0O0O0O0O0O0 ,O00O0O0O00OO0OO00 ):#line:559
	OO0O00O00OO0000OO =foooo (O0000O0O0O0O0O0O0 [1 ],O0000O0O0O0O0O0O0 [0 ])**2.0 #line:560
	if OO0O00O00OO0000OO ==0.0 :#line:561
		return foooo (O00O0O0O00OO0OO00 ,O0000O0O0O0O0O0O0 [0 ])#line:562
	O00O000O0O000000O =(O00O0O0O00OO0OO00 [0 ]-O0000O0O0O0O0O0O0 [0 ][0 ],O00O0O0O00OO0OO00 [1 ]-O0000O0O0O0O0O0O0 [0 ][1 ])#line:566
	OOOO00O00000O0O0O =(O0000O0O0O0O0O0O0 [1 ][0 ]-O0000O0O0O0O0O0O0 [0 ][0 ],O0000O0O0O0O0O0O0 [1 ][1 ]-O0000O0O0O0O0O0O0 [0 ][1 ])#line:567
	OO0OO0O00OO0O00O0 =dotProduct (O00O000O0O000000O ,OOOO00O00000O0O0O )/OO0O00O00OO0000OO #line:568
	if OO0OO0O00OO0O00O0 <0.0 :#line:569
		return foooo (O00O0O0O00OO0OO00 ,O0000O0O0O0O0O0O0 [0 ])#line:570
	elif OO0OO0O00OO0O00O0 >1.0 :#line:571
		return foooo (O00O0O0O00OO0OO00 ,O0000O0O0O0O0O0O0 [1 ])#line:572
	O000OO00OOO000OO0 =(O0000O0O0O0O0O0O0 [0 ][0 ]+(OO0OO0O00OO0O00O0 *(O0000O0O0O0O0O0O0 [1 ][0 ]-O0000O0O0O0O0O0O0 [0 ][0 ])),O0000O0O0O0O0O0O0 [0 ][1 ]+(OO0OO0O00OO0O00O0 *(O0000O0O0O0O0O0O0 [1 ][1 ]-O0000O0O0O0O0O0O0 [0 ][1 ])))#line:573
	return foooo (O00O0O0O00OO0OO00 ,O000OO00OOO000OO0 )#line:574
def foood (OO0OO0OOOOOO0OO0O ,OOO0OO000OOO0OO00 ):#line:577
	O0O0OO00OO0O0O0OO =0 #line:578
	O000O0000O0O0O0O0 ={}#line:579
	for O0O0OOO00O0OOO000 in OOO0OO000OOO0OO00 :#line:580
		O00000O00O0OOOO0O =(-10 ,SCREEN [1 ]/2.0 )#line:581
		OOOOOO00OOOOOO0O0 =foooi (OO0OO0OOOOOO0OO0O ,O00000O00O0OOOO0O ,O0O0OOO00O0OOO000 )#line:582
		if OOOOOO00OOOOOO0O0 !=None :#line:583
			if foooa (OOOOOO00OOOOOO0O0 ,OO0OO0OOOOOO0OO0O ):#line:584
				return True #line:585
			OOOO000OOO00O000O =None #line:588
			if foooa (OOOOOO00OOOOOO0O0 ,O0O0OOO00O0OOO000 [0 ]):#line:589
				OOOO000OOO00O000O =(O0O0OOO00O0OOO000 [0 ],O0O0OOO00O0OOO000 [1 ])#line:590
			elif foooa (OOOOOO00OOOOOO0O0 ,O0O0OOO00O0OOO000 [1 ]):#line:591
				OOOO000OOO00O000O =(O0O0OOO00O0OOO000 [1 ],O0O0OOO00O0OOO000 [0 ])#line:592
			if OOOO000OOO00O000O is not None :#line:593
				if OOOO000OOO00O000O [0 ]in O000O0000O0O0O0O0 :#line:594
					if foook (OO0OO0OOOOOO0OO0O ,O00000O00O0OOOO0O ,O000O0000O0O0O0O0 [OOOO000OOO00O000O [0 ]],OOOO000OOO00O000O [1 ])is not None :#line:597
						continue #line:598
				else :#line:599
					O000O0000O0O0O0O0 [OOOO000OOO00O000O [0 ]]=OOOO000OOO00O000O [1 ]#line:600
			O0O0OO00OO0O0O0OO =O0O0OO00OO0O0O0OO +1 #line:601
	return O0O0OO00OO0O0O0OO %2 ==1 #line:602
def foooc (O00OO0O0OO00O0OOO ,O00OOO0O000O0O00O ):#line:605
	O00OOOO00OOO00000 =[]#line:606
	O0OOO0OO000OOO0O0 =None #line:607
	for O00OO0OOO00000OO0 in O00OOO0O000O0O00O :#line:608
		if O0OOO0OO000OOO0O0 !=None :#line:609
			O00OOOO00OOO00000 .append ((O0OOO0OO000OOO0O0 ,O00OO0OOO00000OO0 ))#line:610
		O0OOO0OO000OOO0O0 =O00OO0OOO00000OO0 #line:611
	O00OOOO00OOO00000 .append ((O00OOO0O000O0O00O [len (O00OOO0O000O0O00O )-1 ],O00OOO0O000O0O00O [0 ]))#line:612
	return foood (O00OO0O0OO00O0OOO ,O00OOOO00OOO00000 )#line:613
def fooob (OO0O000O00OO0O00O ,OOO00OO000O0OOO0O ):#line:616
	return abs (OO0O000O00OO0O00O -OOO00OO000O0OOO0O )<EPSILON #line:617
def foooa (OOO000O0O000OO0O0 ,OO00O000O0O0OOO00 ):#line:620
	return fooob (OOO000O0O000OO0O0 [0 ],OO00O000O0O0OOO00 [0 ])and fooob (OOO000O0O000OO0O0 [1 ],OO00O000O0O0OOO00 [1 ])#line:621
