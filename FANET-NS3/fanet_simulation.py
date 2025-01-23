import ns.core
import ns.network
import ns.mobility
import ns.internet
import ns.wifi
import ns.applications
import ns.flow_monitor

num_uavs=10  #### Setting the UAVs count to 10
simulation_time = 20.0
data_rate= "1Mbps"
packet_size = 1024 # 1Byte

##### CREATING THE UAV NODES,

uav_nodes = ns.network.NodeContainer()
uav_nodes.Create(num_uavs)

##### Configuering how the UAVs will move

mobility = ns.mobility.MobilityHelper()
##classes of mobility
mobility.SetMobilityModel("ns3::RandomWaypointMobilityModel",
                          "Speed", ns.core.StringValue("ns3::UniformRandomVariable[Min=10|Max=20]"),
                          "Pause", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=2.0]"),
                          "PositionAllocator", ns.mobility.ListPositionAllocator())

mobility.Install(uav_nodes)

##### Setting up the Wifi in Ad-HOC mode:

wifi = ns.wifi.WifiHelper()
wifi.SetStandard(ns.wifi.WIFI_PHY_STANDARD_80211b)

wifiPhy = ns.wifi.YansWifiPhyHelper()
wifiPhy.SetChannel(ns.wifi.YansWifiChannelHelper.Default())

wifiMac = ns.wifi.NqosWifiMacHelper()
wifiMac.SetType("ns3::AdhocWifiMac")

devices = wifi.Install(wifiPhy, wifiMac, uav_nodes)

##### Setting up the IP addresses and internet stack

internet = ns.internet.InternetStackHelper()
internet.Install(uav_nodes)

ipv4 = ns.internet.Ipv4AddressHelper()
ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
interfaces = ipv4.Assign(devices)

##### Installing the routing protocols, (In this case we will use the AODV rouing protocol

aodv = ns.aodv.AodvHelper()
internet.SetRoutingHelper(aodv)

##### Adding the traffic flow between UAVs

onoff = ns.applications.OnOffHelper("ns3::UdpSocketFactory",
                                    ns.network.Address(ns.network.InetSocketAddress(interfaces.GetAddress(1), 9)))
onoff.SetAttribute("DataRate", ns.core.StringValue(data_rate))
onoff.SetAttribute("PacketSize", ns.core.UintegerValue(packet_size))

app = onoff.Install(uav_nodes.Get(0))  # Node 0 sends traffic to Node 1
app.Start(ns.core.Seconds(1.0))
app.Stop(ns.core.Seconds(simulation_time))


#####

wifiPhy.EnablePcap("fanet_simulator", devices)

## COllecting Metrics using the flow monitor, the metrics will be used for routing

flowmon_helper = ns.flow_monitor.FlowMonitorHelper()
monitor = flowmon_helper.InstallAll()
monitor.Destroy()

##### Running and stopping the simulator

ns.core.Simulator.Stop(ns.core.Seconds(simulation_time))
ns.core.Simulator.Run()


## Extracting data
flowmon_helper.SerializeToXmlFile("fanet_simulation_flowmon.xml", True, True)
ns.core.Simulator.Destroy()



