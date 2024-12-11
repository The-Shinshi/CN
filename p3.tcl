# Create a new simulator instance
set ns [new Simulator]

# Open trace files for output
set mytrace [open out.tr w]
$ns trace-all $mytrace

set myNAM [open out.nam w]
$ns namtrace-all $myNAM

# Create nodes with colors and labels
set n0 [$ns node]
$n0 color "magenta"
$n0 label "src1"

set n1 [$ns node]
set n2 [$ns node]
$n2 color "magenta"
$n2 label "src2"

set n3 [$ns node]
$n3 color "blue"
$n3 label "dest2"

set n4 [$ns node]
set n5 [$ns node]
$n5 color "blue"
$n5 label "dest1"

# Create LAN and duplex links using valid MAC type
$ns make-lan "$n0 $n1 $n2 $n3 $n4" 100Mbps 100ms LL Queue/DropTail Mac/802_3
$ns duplex-link $n4 $n5 1Mbps 1ms DropTail

# Set up TCP agents and applications for src1
set tcp0 [new Agent/TCP]
$ns attach-agent $n0 $tcp0

set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0
$ftp0 set packetSize_ 500
$ftp0 set interval_ 0.0001

# Set up TCP sink for dest1
set sink5 [new Agent/TCPSink]
$ns attach-agent $n5 $sink5
$ns connect $tcp0 $sink5 

# Set up TCP agents and applications for src2
set tcp2 [new Agent/TCP]
$ns attach-agent $n2 $tcp2

set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set packetSize_ 600
$ftp2 set interval_ 0.001

# Set up TCP sink for dest2
set sink3 [new Agent/TCPSink]
$ns attach-agent $n3 $sink3
$ns connect $tcp2 $sink3  

# Open files for tracing congestion window (cwnd)
proc finish {} {
    global ns mytrace myNAM
    # Flush and close trace files
    $ns flush-trace
    close $mytrace
    close $myNAM
    
    # Launch NAM to visualize the simulation
    exec nam example3.nam & 
    exit 0
}

# Schedule FTP start and stop events for src1 and src2
$ns at 0.1 "$ftp0 start"
$ns at 5.0 "$ftp0 stop"
$ns at 7.0 "$ftp0 start"

$ns at 0.2 "$ftp2 start"
$ns at 8.2 "$ftp2 stop"
$ns at 14.0 "$ftp0 stop"

$ns at 10.0 "$ftp2 start"
$ns at 15.0 "$ftp2 stop"

# Schedule finish event to end the simulation
$ns at 16.0 "finish" 

# Run the simulation
$ns run
