#!/usr/bin/python

import web

import os

import xmltodict
import time
import subprocess

render = web.template.render('templates', base='base')

MAPS_PATH = "/home/strands/.semanticMap"
TIME_TO_WAIT_FOR_MAP = 45
        
urls = (
    '/', 'MainPage',
    '/maps', 'MapsInspector', 
    '/do_scan',  'DoScan', 
    '/publish_scan/(.*)', 'PublishScan', 
    '/launch', 'LaunchNodes'
)
                          
app = web.application(urls, globals())

def find_scans():
    paths = []
    def scan_dir(arg, dirname, filenames):
        if 'room.xml' in filenames:
            paths.append(os.path.join(dirname, 'room.xml'))
    os.path.walk(MAPS_PATH, scan_dir, None)
    return paths

class MainPage(object):
    def GET(self):
        return render.main()

class MapsInspector(object):        
    def GET(self):
        scans =  find_scans()
        stamped_scans = []
        for scan in scans:
            with open(scan,"r") as f:
                data=f.read()
            p=xmltodict.parse(data)
            t = p['SemanticRoom']['RoomLogStartTime']
            scan_time_str = t
            scan_time = time.mktime(time.strptime(t,'%Y-%b-%d %H:%M:%S.%f'))
            scan_cloud = os.path.join(os.path.dirname(scan), 
                                      os.path.basename(p['SemanticRoom']['RoomCompleteCloud']['@filename']) )
            stamped_scans.append((scan_time, scan_time_str, scan_cloud))
        stamped_scans.sort(key=lambda x: x[0])
        return render.maps(stamped_scans)

class DoScan(object):
    def GET(self):
        return render.scan()
    
    
class PublishScan(object):
    def GET(self, scan_file):
        print "Doing file:", scan_file
        p = subprocess.Popen(["rosrun", "pcl_ros", "pcd_to_pointcloud", scan_file, "60"])
        time.sleep(TIME_TO_WAIT_FOR_MAP)
        p.terminate()
        retcode = p.wait()
        #"{'status':"+str(retcode)+", 'filename':"+scan_file+"}"
        return render.visualised(scan_file)

class LaunchNodes(object):
    def __init__(self):
        pass
    def GET(self):
        return "Hello"

    
if __name__ == "__main__":
    print "Metric Map Web server starting.."
    app.run()