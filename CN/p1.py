import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point

# Create nodes
n0 = ns.network.Node()
n1 = ns.network.Node()
n2 = ns.network.Node()

# Create PointToPoint helpers
p2p0 = ns.point_to_point.PointToPointHelper()
p2p0.SetDeviceAttribute("DataRate", ns.core.StringValue("10Mbps"))
p2p0.SetChannelAttribute("Delay", ns.core.StringValue("10ms"))
p2p0.SetQueue("ns3::DropTailQueue", "MaxSize", ns.core.StringValue("10p"))

p2p1 = ns.point_to_point.PointToPointHelper()
p2p1.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
p2p1.SetChannelAttribute("Delay", ns.core.StringValue("10ms"))
p2p1.SetQueue("ns3::DropTailQueue", "MaxSize", ns.core.StringValue("5p"))

# Install devices and links
devices0 = p2p0.Install(n0, n1)
devices1 = p2p1.Install(n1, n2)

# Install internet stack
stack = ns.internet.InternetStackHelper()
stack.Install(n0)
stack.Install(n1)
stack.Install(n2)

# Assign IP addresses
address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))
interfaces0 = address.Assign(devices0)

address.SetBase(ns.network.Ipv4Address("10.1.2.0"),
                ns.network.Ipv4Mask("255.255.255.0"))
interfaces1 = address.Assign(devices1)

# Install applications
tcpSource = ns.applications.BulkSendHelper(
    "ns3::TcpSocketFactory", ns.network.InetSocketAddress(interfaces1.GetAddress(1), 9))
tcpSource.SetAttribute("MaxBytes", ns.core.UintegerValue(0))
sourceApps = tcpSource.Install(n0)
sourceApps.Start(ns.core.Seconds(1.0))
sourceApps.Stop(ns.core.Seconds(61.0))

tcpSink = ns.applications.PacketSinkHelper(
    "ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 9))
sinkApps = tcpSink.Install(n2)
sinkApps.Start(ns.core.Seconds(0.0))
sinkApps.Stop(ns.core.Seconds(61.0))

# Trace the number of packet drops
ns.core.Config.Connect("/NodeList/*/DeviceList/*/$ns3::PointToPointNetDevice/TxQueue/Drop",
                       ns.core.MakeCallback(lambda _: print("Packet Dropped")))

# Run the simulation
ns.core.Simulator.Run()
ns.core.Simulator.Destroy()
