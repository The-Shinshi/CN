import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point


def main():
    ns.core.LogComponentEnable("Ping", ns.core.LOG_LEVEL_INFO)

    # Create nodes
    nodes = ns.network.NodeContainer()
    nodes.Create(7)

    # Set up point-to-point links
    p2p = ns.point_to_point.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.network.DataRateValue(
        ns.network.DataRate("1Mbps")))
    p2p.SetChannelAttribute(
        "Delay", ns.core.TimeValue(ns.core.MilliSeconds(10)))

    devices = []
    for i in range(1, 7):
        if i == 1:
            p2p.SetChannelAttribute(
                "Delay", ns.core.TimeValue(ns.core.MilliSeconds(120)))
        devices.append(p2p.Install(nodes.Get(0), nodes.Get(i)))

    # Set up internet stack
    stack = ns.internet.InternetStackHelper()
    stack.Install(nodes)

    # Assign IP addresses
    address = ns.internet.Ipv4AddressHelper()
    interfaces = []
    for i in range(1, 7):
        address.SetBase(ns.network.Ipv4Address(
            f"10.1.{i}.0"), ns.network.Ipv4Mask("255.255.255.0"))
        interfaces.append(address.Assign(devices[i - 1]))

    # Create and install Ping applications
    ping_apps = []
    for i in range(1, 7):
        ping = ns.applications.V4PingHelper(interfaces[i - 1].GetAddress(1))
        ping_apps.append(ping.Install(nodes.Get(i)))
        ping_apps[-1].SetStartTime(ns.core.Seconds(0.1 * i))
        ping_apps[-1].SetStopTime(ns.core.Seconds(2.0))

    # Set queue limits
    queue_limits = [3, 1, 1]
    for i in range(4, 7):
        p2p.SetQueue("ns3::DropTailQueue", "MaxSize", ns.network.QueueSizeValue(
            ns.network.QueueSize(f"{queue_limits[i - 4]}p")))
        p2p.Install(nodes.Get(0), nodes.Get(i))

    # Run simulation
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()


if __name__ == "__main__":
    main()
