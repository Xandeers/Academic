#!/bin/bash
# calcul_rtt_stats.sh

flux=$1
debut=$2
fin=$3

awk -v flux="$flux" -v debut="$debut" -v fin="$fin" '
BEGIN {
    print "=== CALCUL STATISTIQUES RTT flux", flux, "==="
    count = 0
}

# Même algorithme que précédent
$1=="+" && $8==flux && $6>40 {
    data_time[$12] = $2
}

$1=="-" && $5=="ack" && $8==flux {
    ack_time = $2
    for(seq in data_time) {
        if(data_time[seq] < ack_time && !acked[seq]) {
            rtt = (ack_time - data_time[seq]) * 1000  # en ms
            rtt_values[++count] = rtt
            printf "RTT %3d: %.2f ms\n", count, rtt
            acked[seq] = 1
            break
        }
    }
}

END {
    if (count == 0) {
        print "Aucune mesure RTT"
        exit
    }
    
    print ""
    print "=== STATISTIQUES ==="
    
    # Calculs
    sum = 0
    sum_sq = 0
    min = 999999
    max = 0
    
    for(i=1; i<=count; i++) {
        val = rtt_values[i]
        sum += val
        sum_sq += val * val
        if(val < min) min = val
        if(val > max) max = val
    }
    
    mean = sum / count
    variance = (sum_sq / count) - (mean * mean)
    stddev = sqrt(variance)
    
    # Affichage
    printf "Nombre mesures: %d\n", count
    printf "RTT minimum:    %.2f ms\n", min
    printf "RTT maximum:    %.2f ms\n", max  
    printf "RTT moyen:      %.2f ms\n", mean
    printf "Écart-type:     %.2f ms (jitter)\n", stddev
    printf "Coeff variation: %.1f%%\n", (stddev/mean)*100
    
    # Analyse
    print ""
    print "=== INTERPRÉTATION ==="
    if (stddev > mean * 0.5) {
        print "  Forte variation (jitter élevé)"
        print "   → Réseau instable ou congestion"
    } else if (stddev > mean * 0.2) {
        print "  Variation modérée"
    } else {
        print " Variation faible (réseau stable)"
    }
    
    if (max > mean * 2) {
        print "  RTT maximum très élevé"
        print "   → Possibles délais de file d attente"
    }
}
' out.tr