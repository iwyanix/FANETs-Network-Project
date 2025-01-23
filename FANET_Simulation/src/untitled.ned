//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//
package fanet;

import inet.node.adhoc.AdhocHost;

import inet.mobility.single.RandomWaypointMobility;

import inet.node.inet.Router;

network FANET {

submodules:

uav[10]: AdhocHost {

@display(“p=100,100;i=block/circle”);

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
