set ns [new Simulator]

set mytrace [open out.tr w]
$ns trace-all $mytrace
set myNAM [open out.nam w]
$ns namtrace-all $myNAM

proc finish {} {
    global ns mytrace myNAM
    $ns flush-trace
    close $mytrace
    close $myNAM
    puts "The number of packet drops is: [exec grep -c \"^d\" out.tr]"
    exit 0
}

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]

$ns duplex-link $n0 $n1 10Mbps 10ms DropTail
$ns duplex-link $n1 $n2 5Mbps 10ms DropTail

$ns queue-limit $n0 $n1 10
$ns queue-limit $n1 $n2 5

set tcp [new Agent/TCP]
$ns attach-agent $n0 $tcp

set sink [new Agent/TCPSink]
$ns attach-agent $n2 $sink

$ns connect $tcp $sink

set cbr [new Application/Traffic/CBR]
$cbr attach-agent $tcp
$cbr set packetSize_ 100
$cbr set rate_ 1Mb
$cbr set random_ false

$tcp set fid_ 1

$ns at 1.0 "$cbr start"
$ns at 61.0 "finish"
$ns run
