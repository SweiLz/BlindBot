# from BlindBot.gps import GPS
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map, icons
from dynaconf import FlaskDynaconf
import googlemaps
import math

app = Flask(__name__, template_folder="templates")
GoogleMaps(app, key="AIzaSyB_x-KSdYGw4AOXM95Tx6V0JGAFFUnhOVY")
# gps = GPS("/dev/ttyS0")


@app.route("/")
def mapview():
    # data_lat, data_lon = gps.read_GPS()
    data_lat, data_lon = (13.6483427, 100.4767505)
    movingmap = Map(
        identifier="movingmap",
        varname="movingmap",
        # style=(
        #     "height:600ox;"
        # ),
        lat=data_lat,
        lng=data_lon,
        markers=[
            {
                'lat': data_lat,
                'lng': data_lon
            }
        ],
        zoom=18
    )

    movingmarkers = [
        {'lat': 13.6485062, 'lng': 100.4765653},
        {'lat': 13.6489503, 'lng': 100.476647},
        {'lat': 13.6490773, 'lng': 100.4759503},
        {'lat': 13.6512976, 'lng': 100.4762667},
        {'lat': 13.6512955, 'lng': 100.4763166},
        {'lat': 13.6513551, 'lng': 100.4763059}
    ]

    return render_template(
        'example.html',
        movingmap=movingmap,
        movingmarkers=movingmarkers,
        GOOGLEMAPS_KEY=request.args.get('apikey')
    )


def parseRoutes(raw_data):
    f1_data = raw_data[0]['legs'][0]['steps']
    for f2_data in f1_data:
        print(f2_data['end_location'], ',')
        # print("\n")
    # print(raw_data[0]['legs'][0]['distance'])


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5050, debug=True, use_reloader=True)
    # gmaps = googlemaps.Client(key="AIzaSyB_x-KSdYGw4AOXM95Tx6V0JGAFFUnhOVY")
    # geocode_result = gmaps.geocode("Anman Technology Co.,Ltd.")
    # print(geocode_result)
    # geocode_result = gmaps.geocode("7-ELEVEN 133/2 ถนนพุทธบูชา 37")
    # print(geocode_result)

    loc_anman = (13.6483427, 100.4767505)
    loc_7Eleven = (13.6513509, 100.4762813)

    # routes = gmaps.directions(
    #     loc_anman, loc_7Eleven, mode="walking", language="th", units="metric", region="th")
    routes = [{'bounds': {'northeast': {'lat': 13.6513551, 'lng': 100.4767715}, 'southwest': {'lat': 13.6484114, 'lng': 100.4759503}}, 'copyrights': 'Map data ©2020', 'legs': [{'distance': {'text': '0.4 กม.', 'value': 426}, 'duration': {'text': '5 นาที', 'value': 326}, 'end_address': '139 ถนน พุทธบูชา แขวง บางมด เขตทุ่งครุ กรุงเทพมหานคร 10400 ประเทศไทย', 'end_location': {'lat': 13.6513551, 'lng': 100.4763059}, 'start_address': '55/62, 32 ถนน พุทธบูชา แขวง บางมด เขตทุ่งครุ กรุงเทพมหานคร 10140 ประเทศไทย', 'start_location': {'lat': 13.6484114, 'lng': 100.4767715}, 'steps': [{'distance': {'text': '20 ม.', 'value': 20}, 'duration': {'text': '1 นาที', 'value': 16}, 'end_location': {'lat': 13.6485062, 'lng': 100.4765653}, 'html_instructions': 'มุ่งไปทางทิศ <b>ตะวันตก</b><div style="font-size:0.9em">ถนนที่จำกัดการใช้งาน</div>', 'polyline': {'points': 'quhrAyjgdRGZCLGA'}, 'start_location': {'lat': 13.6484114, 'lng': 100.4767715}, 'travel_mode': 'WALKING'}, {'distance': {'text': '46 ม.', 'value': 46}, 'duration': {'text': '1 นาที', 'value': 35}, 'end_location': {'lat': 13.6489503, 'lng': 100.476647}, 'html_instructions': 'เลี้ยว<b>ขวา</b> ไปยัง <b>ซอย พุทธบูชา 32</b><div style="font-size:0.9em">ถนนที่จำกัดการใช้งาน</div>', 'maneuver': 'turn-right', 'polyline': {'points': 'evhrAqigdR_@Ge@GCBMC'}, 'start_location': {'lat': 13.6485062, 'lng': 100.4765653}, 'travel_mode': 'WALKING'}, {'distance': {'text': '84 ม.', 'value': 84}, 'duration': {'text': '1 นาที', 'value': 63}, 'end_location': {'lat': 13.6490773, 'lng': 100.4759503}, 'html_instructions': 'เลี้ยว<b>ซ้าย</b> ไปยัง <b>ซอย พุทธบูชา 32</b><div style="font-size:0.9em">ถนนที่จำกัดการใช้งาน</div>', 'maneuver': 'turn-left',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'polyline': {'points': '}xhrAajgdRCJK~@I~@'}, 'start_location': {'lat': 13.6489503, 'lng': 100.476647}, 'travel_mode': 'WALKING'}, {'distance': {'text': '0.3 กม.', 'value': 254}, 'duration': {'text': '3 นาที', 'value': 185}, 'end_location': {'lat': 13.6512976, 'lng': 100.4762667}, 'html_instructions': 'เลี้ยว<b>ขวา</b> เข้าสู่ <b>ซอย พุทธบูชา 32</b>', 'maneuver': 'turn-right', 'polyline': {'points': 'wyhrAuegdRUAgAEE?MCm@SoBk@WEKAMAa@BgAHANM??G'}, 'start_location': {'lat': 13.6490773, 'lng': 100.4759503}, 'travel_mode': 'WALKING'}, {'distance': {'text': '10 ม.', 'value': 10}, 'duration': {'text': '1 นาที', 'value': 19}, 'end_location': {'lat': 13.6512955, 'lng': 100.4763166}, 'html_instructions': 'เลี้ยว<b>ขวา</b> เข้าสู่ <b>ถนน พุทธบูชา</b>', 'maneuver': 'turn-right', 'polyline': {'points': 'sgirAuggdR?I'}, 'start_location': {'lat': 13.6512976, 'lng': 100.4762667}, 'travel_mode': 'WALKING'}, {'distance': {'text': '12 ม.', 'value': 12}, 'duration': {'text': '1 นาที', 'value': 8}, 'end_location': {'lat': 13.6513551, 'lng': 100.4763059}, 'html_instructions': 'เลี้ยว<b>ซ้าย</b> เข้าสู่ <b>ซอย พุทธบูชา 37</b>/<wbr/><b>ซอย สงบสุข</b><div style="font-size:0.9em">ปลายทางจะอยู่ทางซ้าย</div>', 'maneuver': 'turn-left', 'polyline': {'points': 'sgirA_hgdRK@'}, 'start_location': {'lat': 13.6512955, 'lng': 100.4763166}, 'travel_mode': 'WALKING'}], 'traffic_speed_entry': [], 'via_waypoint': []}], 'overview_polyline': {'points': 'quhrAyjgdRKh@g@Ie@GCBMCCJU~B}AGSC}C_Ac@Go@@gAHANM??G?IK@'}, 'summary': 'ซอย พุทธบูชา 32', 'warnings': ['เส้นทางเดินเท้าเป็นฟีเจอร์เบต้า ใช้ความระมัดระวัง – เส้นทางนี้อาจไม่มีทางเดินเท้าหรือบาทวิถี'], 'waypoint_order': []}]
    # parseRoutes(routes)

    list_waypoint = [
        {'lat': 13.6485062, 'lng': 100.4765653},
        {'lat': 13.6489503, 'lng': 100.476647},
        {'lat': 13.6490773, 'lng': 100.4759503},
        {'lat': 13.6512976, 'lng': 100.4762667},
        {'lat': 13.6512955, 'lng': 100.4763166},
        {'lat': 13.6513551, 'lng': 100.4763059},
    ]
'''
    # pointA = (13.6485062, 100.4765653)
    pointA = (13.6489503, 100.476647)
    pointB = (13.6490773, 100.4759503)

    lat1, lon1 = math.radians(pointA[0]), math.radians(pointA[1])
    lat2, lon2 = math.radians(pointB[0]), math.radians(pointB[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = 6373 * c
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1) * \
        math.cos(lat2)*math.cos(dlon)
    brng = math.degrees(math.atan2(y, x))
    compass_bearing = (brng + 360) % 360

    print(dist, compass_bearing)

    compass_now = 10
    compass_diff = math.radians(compass_bearing - compass_now)
    turn = math.atan2(math.sin(compass_diff), math.cos(compass_diff))
    print(math.degrees(turn))'''

# [{'address_components': [{'long_name': '32', 'short_name': '32', 'types': ['street_number']}, {'long_name': 'ถนน พุทธบูชา', 'short_name': 'ถนน พุทธบูชา', 'types': ['route']}, {'long_name': 'แขวง บางมด', 'short_name': 'แขวง บางมด', 'types': ['political', 'sublocality', 'sublocality_level_2']}, {'long_name': 'เขตทุ่งครุ', 'short_name': 'เขตทุ่งครุ', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'กรุงเทพมหานคร', 'short_name': 'กรุงเทพมหานคร', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Thailand', 'short_name': 'TH', 'types': ['country', 'political']}, {'long_name': '10140', 'short_name': '10140', 'types': ['postal_code']}], 'formatted_address': '55/62, 32 ถนน พุทธบูชา แขวง บางมด เขตทุ่งครุ กรุงเทพมหานคร 10140, Thailand', 'geometry': {'location': {'lat': 13.6483427, 'lng': 100.4767505}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 13.6496916802915, 'lng': 100.4780994802915}, 'southwest': {'lat': 13.6469937197085, 'lng': 100.4754015197085}}}, 'place_id': 'ChIJVdblnjmj4jARlP5lEEZdH8k', 'plus_code': {'compound_code': 'JFXG+8P Bangkok, Thailand', 'global_code': '7P52JFXG+8P'}, 'types': ['establishment', 'point_of_interest']}, {'address_components': [{'long_name': '55', 'short_name': '55',
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'types': ['subpremise']}, {'long_name': '62', 'short_name': '62', 'types': ['street_number']}, {'long_name': 'Soi Phutthabucha 32', 'short_name': 'Soi Phutthabucha 32', 'types': ['route']}, {'long_name': 'Khwaeng Bang Mot', 'short_name': 'Khwaeng Bang Mot', 'types': ['political', 'sublocality', 'sublocality_level_2']}, {'long_name': 'Khet Thung Khru', 'short_name': 'Khet Thung Khru', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'Krung Thep Maha Nakhon', 'short_name': 'Krung Thep Maha Nakhon', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Thailand', 'short_name': 'TH', 'types': ['country', 'political']}, {'long_name': '10140', 'short_name': '10140', 'types': ['postal_code']}], 'formatted_address': '55, 62 Soi Phutthabucha 32, Khwaeng Bang Mot, Khet Thung Khru, Krung Thep Maha Nakhon 10140, Thailand', 'geometry': {'location': {'lat': 13.6503419, 'lng': 100.4765495}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 13.6516908802915, 'lng': 100.4778984802915}, 'southwest': {'lat': 13.6489929197085, 'lng': 100.4752005197085}}}, 'place_id': 'ChIJIf4nZX2j4jARYVuzK7bmeqs', 'plus_code': {'compound_code': 'MF2G+4J Bangkok, Thailand', 'global_code': '7P52MF2G+4J'}, 'types': ['establishment', 'point_of_interest']}]
# [{'address_components': [{'long_name': '133/2', 'short_name': '133/2', 'types': ['subpremise']}, {'long_name': 'ถนนพุทธบูชา 37', 'short_name': 'ถนนพุทธบูชา 37', 'types': ['route']}, {'long_name': 'แขวงบางมด', 'short_name': 'แขวงบางมด', 'types': ['political', 'sublocality', 'sublocality_level_2']}, {'long_name': 'Khet Thung Khru', 'short_name': 'Khet Thung Khru', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'Krung Thep Maha Nakhon', 'short_name': 'Krung Thep Maha Nakhon', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Thailand', 'short_name': 'TH', 'types': ['country', 'political']},
#                          {'long_name': '10140', 'short_name': '10140', 'types': ['postal_code']}], 'formatted_address': '133/2 ถนนพุทธบูชา 37 แขวงบางมด Khet Thung Khru, Krung Thep Maha Nakhon 10140, Thailand', 'geometry': {'location': {'lat': 13.6513509, 'lng': 100.4762813}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 13.6526998802915, 'lng': 100.4776302802915}, 'southwest': {'lat': 13.6500019197085, 'lng': 100.4749323197085}}}, 'place_id': 'ChIJoVcbgvui4jARbwF1Yhy26Gc', 'plus_code': {'compound_code': 'MF2G+GG Bangkok, Thailand', 'global_code': '7P52MF2G+GG'}, 'types': ['convenience_store', 'establishment', 'food', 'point_of_interest', 'store']}]
