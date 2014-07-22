This provides a GUI for triggering metric mapping actions and visualising
previously captured maps using RViz.

It depends on several ROS nodes being launched *on bobl*:

1. roslaunch openni_wrapper main.launch camera:=head_xtion 
2. rosrun scitos_ptu ptu_action_server_metric_map.py
3. roslaunch cloud_merge cloud_merge.launch
4. roslaunch semantic_map semantic_map.launch
5. roslaunch strands_webtools webtools.launch 

On *bob*, the usual map, localisation and datacentre. 

Finally, the GUI can be launched:

```
metric_map_gui.py 8090
```

Then point the web browser at http://bobl:8090

To change the metric map storage location (when on a different floor):

```
change_map_link.sh unique_floor_name
```

