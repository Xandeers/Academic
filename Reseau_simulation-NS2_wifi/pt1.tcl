# instantiation du simulateur
set ns [new Simulator]

# associer les couleurs pour NAM
$ns color 1 green
$ns color 2 red
$ns color 3 blue

# instantiation du fichier de traces
set file1 [open out.tr w]
$ns trace-all $file1

# instantiation du fichier de traces pour NAM
set file2 [open out.nam w]
$ns namtrace-all $file2

# procedure pour lancer automatiquement le visualisateur NAM a la fin de la simulation
proc finish {} {
global ns file1 file2
$ns flush-trace
close $file1
close $file2
exec nam out.nam &
exit 0
} 

#instanciation des noeuds

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]


# instantiation d’une ligne de communication full duplex entre les noeuds n0 et n2
$ns duplex-link $n0 $n2 1Mb 10ms DropTail


# instantiation d’une ligne de communication full duplex entre les noeuds n2 et n1
$ns duplex-link $n2 $n1 1Mb 10ms DropTail


# instantiation d’une ligne de communication full duplex entre les noeuds n2 et n3
$ns duplex-link $n2 $n3 1Mb 10ms DropTail
$ns queue-limit $n2 $n3 10
$ns queue-limit $n3 $n2 10


# instantiation d’une ligne de communication full duplex entre les noeuds n3 et n4
$ns duplex-link $n3 $n4 1Mb 50ms DropTail

#declaration flux tcp entre noeud n0 et n3
set tcp [new Agent/TCP]
$ns attach-agent $n0 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink
$ns connect $tcp $sink
$tcp set fid_ 1 #identifie ce flux

set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp
$ftp0 set packetSize_ 1000


#declaration du flux tcp entre les noeud n1 et n4
set tcp1 [new Agent/TCP]
$ns attach-agent $n1 $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 2 #identifie le deuxieme flux 

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set packetSize_ 1000

# scenario de debut et de fin de generation des paquets par ftp

$ns at 0.0 "$ftp0 start"
$ns at 5.0 "$ftp0 stop"
$ns at 0.0 "$ftp1 start"
$ns at 10.0 "$ftp1 stop"

# la simulation va durer 11 secondes de temps simule
$ns at 11.0 "finish"
# debut de la simulation
$ns run

