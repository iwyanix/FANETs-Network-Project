//Having an issue with setting up the INET Framework 
package fanet;

import inet.node.adhoc.AdhocHost;

import inet.mobility.single.RandomWaypointMobility;

import inet.node.inet.Router;

network FANET {

submodules:
// I chose 10 uavs as a start, this value can be modified
uav[10]: AdhocHost {

@display(“p=100,100;i=block/circle”);
// Using RrandomWayPoint for setting up the UAVs, not realistic but there are other realistic models, like Gaus's
mobility.typename = “RandomWaypointMobility”;

mobility.initialX = uniform(0, 1000);

mobility.initialY = uniform(0, 1000);

}

gcs: Router {

@display(“p=500,500;i=block/router”);

}

connections:

for i=0..9 {

uav[i].pppg++ <–> gcs.pppg++;

}

}


// All the values in this .ned file are completely randomly chosen
