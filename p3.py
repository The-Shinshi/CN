import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point
import ns.csma


def main():
    # Create nodes
    nodes = ns.network.NodeContainer()
    nodes.Create(6)

    # Set up CSMA (Ethernet) channel
    csma = ns.csma.CsmaHelper()
    csma.SetChannelAttribute("DataRate", ns.network.DataRateValue(
        ns.network.DataRate("100Mbps")))
    csma.SetChannelAttribute(
        "Delay", ns.core.TimeValue(ns.core.MilliSeconds(100)))

    devices = csma.Install(nodes)

    # Set up point-to-point link
    p2p = ns.point_to_point.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.network.DataRateValue(
        ns.network.DataRate("1Mbps")))
    p2p.SetChannelAttribute(
        "Delay", ns.core.TimeValue(ns.core.MilliSeconds(1)))
    devices_p2p = p2p.Install(nodes.Get(4), nodes.Get(5))

    # Set up internet stack
    stack = ns.internet.InternetStackHelper()
    stack.Install(nodes)

    # Assign IP addresses
    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                    ns.network.Ipv4Mask("255.255.255.0"))
    interfaces = address.Assign(devices)
    address.SetBase(ns.network.Ipv4Address("10.1.2.0"),
                    ns.network.Ipv4Mask("255.255.255.0"))
    interfaces_p2p = address.Assign(devices_p2p)

    # Create TCP applications
    tcp0 = ns.applications.BulkSendHelper("ns3::TcpSocketFactory", ns.network.Address(
        ns.network.InetSocketAddress(interfaces_p2p.GetAddress(1), 9)))
    tcp0.SetAttribute("MaxBytes", ns.core.UintegerValue(0))
    app_tcp0 = tcp0.Install(nodes.Get(0))
    app_tcp0.Start(ns.core.Seconds(0.1))
    app_tcp0.Stop(ns.core.Seconds(14.0))

    tcp2 = ns.applications.BulkSendHelper("ns3::TcpSocketFactory", ns.network.Address(
        ns.network.InetSocketAddress(interfaces.GetAddress(3), 9)))
    tcp2.SetAttribute("MaxBytes", ns.core.UintegerValue(0))
    app_tcp2 = tcp2.Install(nodes.Get(2))
    app_tcp2.Start(ns.core.Seconds(0.2))
    app_tcp2.Stop(ns.core.Seconds(15.0))

    # Create sink applications
    sink_tcp0 = ns.applications.PacketSinkHelper(
        "ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 9))
    app_sink_tcp0 = sink_tcp0.Install(nodes.Get(5))
    app_sink_tcp0.Start(ns.core.Seconds(0.0))
    app_sink_tcp0.Stop(ns.core.Seconds(16.0))

    sink_tcp2 = ns.applications.PacketSinkHelper(
        "ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 9))
    app_sink_tcp2 = sink_tcp2.Install(nodes.Get(3))
    app_sink_tcp2.Start(ns.core.Seconds(0.0))
    app_sink_tcp2.Stop(ns.core.Seconds(16.0))

    # Enable tracing for congestion window
    tcp = ns.internet.TcpSocketFactory()
    sink_tcp0_path = "/NodeList/{0}/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow".format(
        nodes.Get(0).GetId())
    sink_tcp2_path = "/NodeList/{0}/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow".format(
        nodes.Get(2).GetId())
    ns.core.Config.Connect(sink_tcp0_path, ns.core.MakeCallback(trace_cwnd))
    ns.core.Config.Connect(sink_tcp2_path, ns.core.MakeCallback(trace_cwnd))

    # Run simulation
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()


def trace_cwnd(cwnd):
    print(f"CWND: {cwnd}")


if __name__ == "__main__":
    main()
