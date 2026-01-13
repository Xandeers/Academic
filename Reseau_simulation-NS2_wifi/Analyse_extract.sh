#!/bin/bash
# extract_rtt_seq.sh

flux=$1
sortie="rtt_seq_flux${flux}.dat"

echo "# Sequence RTT(ms) Temps(s)" > "$sortie"

awk -v flux="$flux" '
BEGIN {
    print "Extraction RTT par séquence flux", flux, "..."
}

# Stocker envois DATA par séquence (prendre premier envoi seulement)
$1 == "+" && $8 == flux && $6 > 40 {
    seq = $12
    if (!(seq in send_time)) {
        send_time[seq] = $2  # Premier envoi seulement
    }
}

# Chercher ACK correspondants
$1 == "-" && $5 == "ack" && $8 == flux {
    ack_time = $2
    ack_seq = $12
    
    # Règle TCP: ACK N accuse DATA N-1
    data_seq = ack_seq - 1
    
    if (data_seq in send_time) {
        rtt_ms = (ack_time - send_time[data_seq]) * 1000
        
        if (rtt_ms > 0 && rtt_ms < 1000) {  # Filtre réaliste
            # Trier par séquence
            sequences[data_seq] = data_seq
            rtt_values[data_seq] = rtt_ms
            time_values[data_seq] = send_time[data_seq]
        }
        
        delete send_time[data_seq]
    }
}

END {
    # Trier les séquences numériquement
    n = asorti(sequences, sorted)
    
    for (i = 1; i <= n; i++) {
        seq = sorted[i]
        printf "%d %.2f %.3f\n", seq, rtt_values[seq], time_values[seq]
    }
}
' out.tr > "$sortie"

echo "Données sauvegardées dans $sortie"
echo "Séquences: $(tail -n +2 "$sortie" | wc -l)"