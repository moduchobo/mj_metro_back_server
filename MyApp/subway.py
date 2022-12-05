#--------------------------데이터 불러오기와서 딕셔너리로 그래프그리기-------------------------------------
import csv, re, os
from pprint import pprint as pp

station = {}

f1 = open(os.path.dirname(os.path.realpath(__file__))+'/dataset/stations_node.csv', 'r', encoding='utf-8-sig')
csv_read_node = csv.DictReader(f1)  
for col in csv_read_node: 
    snum = col['역번호'] # print(type(col['역번호'])) str
    del col['역번호']
    station.update({snum:col})
    station[snum].update({'근처역':{}})
f1.close()
f2 = open(os.path.dirname(os.path.realpath(__file__))+'/dataset/stations.csv', 'r', encoding='utf-8-sig')
csv_read_node = csv.DictReader(f2)  
for col in csv_read_node: 
    startsnum = col['출발역']
    del col['출발역']
    endsnum = col['도착역']
    del col['도착역']
    station[startsnum]['근처역'].update({endsnum:col})
    station[endsnum]['근처역'].update({startsnum:col})
# pp(station)                     
f2.close()

#  '904': {'경도': '127.007896',
#          '근처역': {'621': {'거리(미터)': '650', '비용(원)': '650', '시간(초)': '250'},
#                  '702': {'거리(미터)': '250', '비용(원)': '700', '시간(초)': '500'}},
#          '역이름': '동대문역사문화공원',
#          '위도': '37.565138',
#          '주소': '서울 중구 마른내로 162',
#          '호선': '9',
#          '환승(없다면0)': '0'}
#------------------------------------------------------------그래프 및 역 정리

#--------------------------데이터 불러오기 끝-------------------------------------

#--------------------------데이터 저장 및 클래스 작업 + 호선-------------------------------------
class S:
    def __init__(self, name, args):
        self.__s_num = name              #역번호
        self.__s_name = args['역이름']
        self.__latitude = args['위도']
        self.__longitude = args['경도']
        self.__address = args['주소']
        self.__lineNumber = [args['호선']]
        if args['환승(없다면0)']!='0':
            self.__lineNumber.append(args['환승(없다면0)'])
        self.__nearStation = args['근처역']
        self.__s_timetable = {}
        #시간표

    @property
    def s_num(self):
        return self.__s_num

    @property
    def s_name(self):
        return self.__s_name

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def address(self):
        return self.__address

    @property
    def lineNumber(self):
        return self.__lineNumber

    @property
    def nearStation(self):
        return self.__nearStation

    @property
    def s_timetable(self):
        return self.__s_timetable

    @s_timetable.setter
    def s_timetable(self, value):    # setter
        self.__s_timetable = value

    def sprint(self):
        print(self.s_num)
        print(self.s_name)
        print(self.latitude)
        print(self.longitude)
        print(self.address)
        print(self.lineNumber)
        print(self.nearStation)

    def __str__(self):
        return self.s_name


#--------------------------클래스 딕셔너리 station_class_dict -------------------------------------
station_class_dict = {}
for i,j in station.items():
    station_class_dict.update({i:S(i,j)})


#--------------------------호선 딕셔너리 끝-------------------------------------
station_lineNumber_dict = {}
for i in range(1,10):
    station_lineNumber_dict.update({str(i):[]})
for s_num, s_class in station_class_dict.items():
    if len(s_class.lineNumber)==2:
        station_lineNumber_dict[s_class.lineNumber[1]].append(s_num)
    station_lineNumber_dict[s_class.lineNumber[0]].append(s_num)
# pp(station_lineNumber_dict)

#ㅡㅡㅡ환승을 위한 호선 리스트 순서대로 sortㅡㅡㅡ
# 딕셔너리 호선에 있는 리스트를 sort 해야함
for i in station_lineNumber_dict.keys():#i는 현재 호선
    lineNum_list = station_lineNumber_dict[i]# 따라서 리스트에 도달 lineNum_list = 정리되어있지 않은 호선 리스트
    result = []
    
    for j in lineNum_list:# 리스트를 하나하나씩 검사한 후
        count = 0
        for k in station_class_dict[j].nearStation.keys():#근처에 있는 역이름 따오기
            if i in station_class_dict[k].lineNumber:
                count += 1
        if count == 1:
            result.append(j)
            break
    if not result: #모두 2개라면 즉, 순환노선이라면
        result.append(lineNum_list[0]) # 아무거나 넣기

    for l in station_class_dict[result[0]].nearStation.keys():
        if i in station_class_dict[l].lineNumber:
            result.append(l)
            break

    while sorted(lineNum_list) != sorted(result):
        for m in station_class_dict[result[-1]].nearStation.keys():
            if (i in station_class_dict[m].lineNumber) and (m not in result):
                result.append(m)
                break
    station_lineNumber_dict[i] = result

print(station_lineNumber_dict)


# 만약 1개짜리가 있다면 한개는 처음 한개는 마지막 두고
# 새로 리스트로 class에 있는 값으로 확인 후 리스트 생성
# 만약 모두 2개라면 그냥 한줄로 세운다.
# 그러고 만든 리스트를 새로 생성
#--------------------------데이터 저장 및 클래스 작업 + 호선 끝-------------------------------------

#--------------------------지하철 시간표-------------------------------------
import copy
timeTable = []
f3 = open(os.path.dirname(os.path.realpath(__file__))+'/dataset/station_timetable.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f3)
for line in rdr:
    temp = []
    for i in line:
        temp.append(re.sub(r'[^0-9]', '', i))
    timeTable.append(temp)
f3.close()

station_timeTable_dict = {}
# print(timeTable)

for i in timeTable: # 호선 딕셔너리 시작점에 있는 역에 넣을 시간표를 만든다. 시간표는 호선:{'front':[시간(초)],'back':[시간(초)]} 호선은 1~9까지
    station_timeTable_dict.update({i[0]:{}})
    front = []
    back = []
    temp_count = 0
    temp_time = 0
    for j in range(1,len(i)):
        if i[j]=='':
            break
        if j%2 == 1: # 시간
            temp_time += int(i[j])*60*60 #초로 바꾸기
        else: #분
            for k in range(int(len(i[j]) / 2)):
                if temp_count == 0:
                    front.append(int(i[j][k*2:k*2+2])*60 + temp_time)
                    temp_count = 1
                else:
                    back.append(int(i[j][k*2:k*2+2])*60 + temp_time)
                    temp_count = 0

    station_timeTable_dict[i[0]].update({'front':front})
    station_timeTable_dict[i[0]].update({'back':back})
    
# print(station_timeTable_dict)

# print(station_timeTable_dict['9'])
# print(station_lineNumber_dict)
for lineNum, linelist in station_lineNumber_dict.items():#직접 맨 처음 역에 넣기
    station_class_dict[linelist[0]].s_timetable.update({lineNum:station_timeTable_dict[lineNum]})
for lineNum, linelist in station_lineNumber_dict.items():
    print(station_class_dict[linelist[0]].s_timetable.keys())

# print(station_class_dict['107'].s_timetable['3'])

# '1': ['101'], '2': ['101'], '3': ['107'], '4': ['104'], '5': ['109'], '6': ['116'], '7': ['202'], '8': ['113'], '9': ['112']
for lineNum, linelist in station_lineNumber_dict.items(): # 다른 역들 계산해서 넣기 front = 숫자 높은거로 가는거 101 - 102 - 103
    # front back 선택도 만들기 
    isFront = True
    temp_var1 = 0
    temp_var2 = 0 
    for i in linelist:
        if int(i)//100 == int(lineNum):
            if temp_var1 !=0 and temp_var2 != 0:
                if int(temp_var1) < int(temp_var2):
                    isFront = True
                else:
                    isFront = False
            if temp_var1 == 0:
                temp_var1 = i
            elif temp_var2 == 0:
                temp_var2 = i


    temp_list = linelist[0]
    for i in linelist[1:]:
        temp_table = copy.deepcopy(station_class_dict[temp_list].s_timetable[lineNum])
        temp_time_plus = int(station_class_dict[temp_list].nearStation[i]['시간(초)']) + 60
        temp_count = 0
        for k, v in temp_table.items():
            if isFront:
                if k=='front':
                    for j in range(len(v)):
                        v[j] += temp_time_plus
                else:
                    for j in range(len(v)):
                        v[j] -= temp_time_plus
            else:
                if k=='front':
                    for j in range(len(v)):
                        v[j] -= temp_time_plus
                else:
                    for j in range(len(v)):
                        v[j] += temp_time_plus
        station_class_dict[i].s_timetable.update({lineNum:temp_table})
        temp_list = i

# start = '101'
# end = '103'
# h='1'
# print(start+'front', station_class_dict[start].s_timetable[h]['front'][:5])
# print(end+'front', station_class_dict[end].s_timetable[h]['front'][:5])
# print(start+'back', station_class_dict[start].s_timetable[h]['back'][:5])
# print(end+'back', station_class_dict[end].s_timetable[h]['back'][:5])
# print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
# start = '107'
# end = '308'
# h='3'
# print(start+'front', station_class_dict[start].s_timetable[h]['front'][:5])
# print(end+'front', station_class_dict[end].s_timetable[h]['front'][:5])
# print(start+'back', station_class_dict[start].s_timetable[h]['back'][:5])
# print(end+'back', station_class_dict[end].s_timetable[h]['back'][:5])

# print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
# start = '101'
# end = '103'
# h='1'
# print(start+'front', station_class_dict[start].s_timetable[h]['front'][:5])
# print(end+'front', station_class_dict[end].s_timetable[h]['front'][:5])
# print(start+'back', station_class_dict[start].s_timetable[h]['back'][:5])
# print(end+'back', station_class_dict[end].s_timetable[h]['back'][:5])
# print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
# print(station_class_dict['103'].s_timetable['1'])

# back 빼는거 만들기
# 순환 억까 청산하기


# {'이쪽인가':{'door_open':[],'door_close':[]},
# '저쪽인가':{'door_open':[],'door_close':[]}}





#--------------------------지하철 시간표 끝-------------------------------------

#--------------------------다익스트라-------------------------------------

import heapq  # 우선순위 큐 구현을 위함
import copy


def dijkstra(start, end): # distance+money+time dmt_num => str 문자임
    dmt_num = {'비용(원)':'money','거리(미터)':'distance', '시간(초)':'time'}
    result = {}
    for dmt in dmt_num.keys():
        distances = {node: {'min_value':float('inf'), 'route':[]} for node in station_class_dict}  # start로 부터의 최소 거리값 구해야 하므로 가장 큰 값인 무한대inf를 넣어두고 각 루트를 표현한 route에 출발역인 start를 넣는다.
        distances[start]['min_value'] = 0  # 시작 값은 0이어야 함
        queue = []
        heapq.heappush(queue, [distances[start]['min_value'], start, []])  # 시작 노드부터 탐색 시작 하기 위함. #[시작 0, 시작노드이름, 시작 루트]
        while queue:  # queue에 남아 있는 노드가 없으면 끝
            current_distance, current_destination, current_route = heapq.heappop(queue)  # 탐색 할 노드, 거리를 가져옴.
            distances[current_destination]['route'] = copy.deepcopy(current_route)
            distances[current_destination]['route'].append(current_destination)
            if current_destination == end: # 만약 여기서 current_destination이 목적지라면 break 거기까지가 목적지임 
                break
            if distances[current_destination]['min_value'] < current_distance:  # 기존에 있는 거리보다 길다면, 볼 필요도 없음
                continue
            for new_destination, new_distanceitem in station_class_dict[current_destination].nearStation.items(): #111111111111111111111111111graph[current_destination]
                new_distance = new_distanceitem[dmt]#22222222222222222222dmt_num
                if dmt == '시간(초)':
                    distance = current_distance + int(new_distance) + 60  # 해당 노드를 거쳐 갈 때 거리 , 전철 정차 시간 1분
                else:
                    distance = current_distance + int(new_distance)  # 해당 노드를 거쳐 갈 때 거리 , 비용과 거리는 정차 시간 관여X
                if distance < distances[new_destination]['min_value']:  # 알고 있는 거리 보다 작으면 갱신
                    distances[new_destination]['min_value'] = distance
                    heapq.heappush(queue, [distance, new_destination, distances[current_destination]['route']])  # 다음 인접 거리를 계산 하기 위해 큐에 삽입 - 방금 계산한 거리와 새로운 목적지
        result[dmt_num[dmt]] = distances[end]
    return result
    # start부터 end까지 걸리는 숫자와 길(루트) 반환 {'min_value': 1540, 'route': ['101', '101', '123', '305', '306', '307', '401']}
# print(d(station, '비용(원)', '104', '116'))
# print('zz',dijkstra('104', '116'))
# print(dijkstra(station, '거리(미터)', '104', '116'))
# print(dijkstra(station, '시간(초)', '104', '116'))


#--------------------------환승-------------------------------------
def evaluate(args):  #검증
    money = [0]
    distance = [0]
    time = [0]
    dmt_num = {'비용(원)':money,'거리(미터)':distance, '시간(초)':time}
    i1=0
    i2=0
    for i in args: 
        if i1==0 and i2==0:
            i1 = i
        elif i2==0:
            i2 = i
            for dmt, var in dmt_num.items():
                if dmt == '시간(초)':
                    var[0]+=int(station_class_dict[i1].nearStation[i2][dmt])+60
                else:
                    var[0]+=int(station_class_dict[i1].nearStation[i2][dmt])
        elif i1!=0 and i2!=0:
            i1 = i2
            i2 = i
            for dmt, var in dmt_num.items():
                if dmt == '시간(초)':
                    var[0]+=int(station_class_dict[i1].nearStation[i2][dmt])+60
                else:
                    var[0]+=int(station_class_dict[i1].nearStation[i2][dmt])
    return {'money':money[0],'distance':distance[0],'time':time[0]}

def divide_route(route): #루트를 프론트에 보내기 위해 환승 정보와 루트를 나눈다
    result_route = []
    temp_route = [route[0]]
    temp_hosun = ''
    for lineNum, linelist in station_lineNumber_dict.items(): # 시작과 끝 역의 호선이 같다면 호선 번호를 hosun에 넣어라
        if (route[0] in linelist) and (route[1] in linelist):
            temp_hosun = lineNum
    start_route = ''
    next_route = route[0]
    
    for r in route[1:]:
        start_route = next_route
        next_route = r

        if start_route == next_route:#경유지
            result_route.append((temp_route,temp_hosun))
            temp_route = [next_route]
        else:
            for lineNum, linelist in station_lineNumber_dict.items(): # 같은 호선 찾기
                if (start_route in linelist) and (next_route in linelist):
                    #같은것이 lineNum 한개밖에 없음
                    if temp_hosun == lineNum: # 환승하는게 아님
                        temp_route.append(next_route)
                    else: #환승이라면
                        result_route.append((temp_route,temp_hosun))
                        temp_route=[start_route]
                        temp_route.append(next_route)
                    temp_hosun = lineNum
                    break
    result_route.append((temp_route,temp_hosun))

    return result_route

# a = divide_route(['101', '102', '103', '104','401','307','306'])
# print(a)
# print(a[0][0])
# print(a[1][1])
    

def transfer(start,end): # 최소환승
    hosun = []
    result = {'transfer':{'route':'', 'money':'', 'distance':'','time':''}}
    for lineNum, linelist in station_lineNumber_dict.items(): # 시작과 끝 역의 호선이 같다면 호선 번호를 hosun에 넣어라
        if (start in linelist) and (end in linelist):
            hosun.append(lineNum)
    result0 = []
    if hosun: # 호선에 들어있는게 있다면
        while hosun:
            line = station_lineNumber_dict[hosun.pop()] #호선 번호를 딕셔너리에서 찾는다면 순서가 정렬된 역 호선이나옴
            for i in [-1,1]: # 라인을 앞으로 한번 뒤로 한번
                result1 = []
                indexing = line.index(start)
                while line[indexing]!=end:
                    result1.append(line[indexing])
                    indexing += i
                    if indexing == len(line): # 오류 방지 (-는 상관없음)
                        indexing = 0
                result1.append(line[indexing])
                result0.append(result1)

    else: #없다면 다른 호선이므로 다익스트라 해서 가장 작은 애 리턴
        d_result =  dijkstra(start, end)
        temp_result = {'money':0, 'distance':0,'time':0}
        for i in temp_result.keys():
            d_route = divide_route(d_result[i]['route'])
            temp_transfer = 0
            temp_hosun = d_route[0][1]
            for j in d_route:
                if temp_hosun != j[1]:
                    temp_transfer += 1
                    temp_hosun = j[1]
            temp_result[i] = temp_transfer
        result['transfer']['route'] = d_result[min(temp_result, key=temp_result.get)]['route']
        for i in temp_result.keys():
            result['transfer'][i] = d_result[i]['min_value']
        return result

    #모든 루트 리스트에서 가장 시간이 짧은 리스트를 반환한다. 이때 검증에서 오류가 났다면 같은 호선이지만 순환 노선이 아닌 루트이므로 잘못되었다 따라서 예외 처리(2중 3중은 무조건 오류 1개, 4중은 오류 없음)
    try:
        result['transfer'].update(evaluate(result0[0]))
        result['transfer']['route'] = result0[0]
    except:
        result['transfer'].update(evaluate(result0[1]))
        result['transfer']['route'] = result0[1]
    for elist in result0[1:]:
        try:
            if result['transfer']['time'] > evaluate(elist)['time']:
                result['transfer'].update(evaluate(elist))
                result['transfer']['route'] = elist
        except:
            pass
    return result

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def d(start, end, *args):
    queue = [end, start]
    for i in args:
        queue.insert(1,i)
    d_result = [] # 경유지를 위한 순서대로 리스트 구현
    temp_queue = queue.pop()
    result=dijkstra(temp_queue, queue[-1]) # 결과 dict 생성
    result.update(transfer(temp_queue, queue[-1]))
    for i in range(len(args)): #경유지 있을때만 실행 = 경유지 추가
        temp_queue = queue.pop()
        d_result.append(dijkstra(temp_queue, queue[-1]))
        d_result[-1].update(transfer(temp_queue, queue[-1]))
    dmt = ['distance','money','time']
    for i in d_result: #경유지 있을때만 실행 = 루트 합치면서 정리
        for j in dmt:
            result[j]['min_value'] += i[j]['min_value'] # 최소 비용 등 거리 추가 거리는 int 임
            result[j]['route'].extend(i[j]['route']) # 경유지 한개 빼고 구현
        for j in result['transfer'].keys():
            if j == 'route':
                result['transfer'][j].extend(i['transfer'][j])
            else:
                result['transfer'][j] += i['transfer'][j]

    for r in result.keys():
        result[r]['route'] = divide_route(result[r]['route'])
        
        
        
        i1 = ''
        i2 = result[r]['route'][0][1]
        transfer_count = 0
        for i in result[r]['route'][1:]:
            i1 = i2
            i2 = i[1]
            if i1 == i2:
                continue
            transfer_count += 1
        result[r]['transfer_count'] = transfer_count
    return result

# d('101','103','105')
# pp(d('101','105','107'))
# pp(d('601','614')) # 109, 122 돈, 601 614 시간, 116 121
# pp(d('109','122')) # 109, 122 돈, 601 614 시간, 116 121
# {'distance': {'min_value': 3300,
#               'route': [(['101', '102', '103', '104', '105', '106', '107'], '1'),
#                         (['107', '106', '105'], '1')],
#               'transfer_count': 0},
#  'money': {'min_value': 2480,
#            'route': [(['101', '102', '103', '104', '105', '106', '107'], '1'),
#                      (['107', '106', '105'], '1')],
#            'transfer_count': 0},
#  'time': {'min_value': 3420,
#           'route': [(['101', '102', '103', '104', '105', '106', '107'], '1'),
#                     (['107', '106', '105'], '1')],
#           'transfer_count': 0},
#  'transfer': {'distance': 3300,
#               'money': 2480,
#               'route': [(['101', '102', '103', '104', '105', '106', '107'], '1'),
#                         (['107', '106', '105'], '1')],
#               'time': 3420,
#               'transfer_count': 0}}
