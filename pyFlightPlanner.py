import folium
import sys 
import json
print(f"folium Version: {folium.__version__}")

# 위도, 경도
lat, lon = 37.504811111562, 127.025492036104
# 줌 크기
zoom_size = 12

print(sys.argv)

def open_json_mission(szfile):

    with open(szfile,"r") as json_file:    
        wpt_list = json.load(json_file)

    return wpt_list
    
def save_json_mission(szfile,wpt_list):
    
    with open(szfile,"w") as json_file:
        json.dump(wpt_list,json_file)
    

# significant digit change
def change_digits(output_name,sdigit):
    temp = []
    with open(output_name,"r") as outf:
        doc = outf.readlines()
        for line in doc:
            temp.append(line.replace('toFixed(4)',f"toFixed({sdigit})"))
            
    with open(output_name,"w") as outff:
        outff.writelines(temp)

    return True
 
def mark_mission(wpt_list):

    global mapobj
    
    loc_data = []
    id_wpt = 0
    for wpt in wpt_list:
        id_wpt = id_wpt + 1 
        folium.Marker(location = [wpt['lat'] , wpt['lon']], \
            popup = f"WPTID:{wpt['wpt_id']} \n Lat:{wpt['lat']:.6f} \n Lon:{wpt['lon']:.6f}").add_to(mapobj)
        loc_data.append([wpt['lat'], wpt['lon']])
            
            
    folium.PolyLine(locations=loc_data).add_to(mapobj)
        


def cg_mission(wpt_list):
    
    cgx = 0.0
    cgy = 0.0
    num_wpt = float(len(wpt_list))
    for wpt in wpt_list:
       cgx = cgx+ wpt['lat']/num_wpt
       cgy = cgy+ wpt['lon']/num_wpt
    
    return [cgx , cgy]
        
    # ( {'lat':36.705922,'lon':126.359999} , {'lat':36.223623,'lon':126.359999} )
    '''
def cal_distance(wpt1,wpt2)
    wpt1['lat']
    wpt2['lat']
'''

if __name__ =='__main__':
    # 구글 지도 타일 설정
    tiles = "http://mt0.google.com/vt/lyrs=s&hl=ko&x={x}&y={y}&z={z}"
    # 속성 설정
    attr = "Google"

    if len(sys.argv) >= 2 :
        wpt_list = open_json_mission(sys.argv[1])
        lat,lon = cg_mission(wpt_list)

    # 지도 객체 생성
    mapobj = folium.Map(location = [lat, lon],
                   zoom_start = zoom_size,
                   tiles = tiles,
                   attr = attr)
                   
    for id_mission in range(1,len(sys.argv)):
        wpt_list = open_json_mission(sys.argv[id_mission])
        print(wpt_list)
        
        mark_mission(wpt_list)
        
    output_name = 'map.html'
    mapobj.add_child(folium.ClickForMarker( "<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}"))
    mapobj.add_child(folium.features.ClickForLatLng(format_str='lat+","+lng' , alert= True))
    mapobj.save(output_name)
    change_digits(output_name,7)