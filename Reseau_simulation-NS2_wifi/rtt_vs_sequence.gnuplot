# rtt_vs_sequence.gnuplot

# Configuration
set terminal pngcairo size 1400,900 enhanced font 'Arial,12'
set output 'rtt_vs_sequence.png'

set title 'RTT en fonction du numéro de séquence - Flux TCP 1 et 2'
set xlabel 'Numéro de séquence'
set ylabel 'RTT (millisecondes)'
set grid xtics ytics mxtics mytics
set key top left

# Styles
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 0.8  # Flux 1
set style line 2 lc rgb '#dd181f' lt 1 lw 2 pt 9 ps 0.8  # Flux 2

# Tracé
plot 'rtt_seq_flux1.dat' using 1:2 with points ls 1 title 'Flux 1 (n0→n3)', \
     'rtt_seq_flux2.dat' using 1:2 with points ls 2 title 'Flux 2 (n1→n4)'

# Version avec lignes de tendance
set output 'rtt_seq_tendance.png'
set title 'RTT par séquence avec tendance'

# Calculer et afficher la moyenne
stats 'rtt_seq_flux1.dat' using 2 name 'f1'
stats 'rtt_seq_flux2.dat' using 2 name 'f2'

plot 'rtt_seq_flux1.dat' using 1:2 with points ls 1 title 'Flux 1', \
     f1_mean with lines ls 1 lw 3 title sprintf('Moyenne F1: %.1f ms', f1_mean), \
     'rtt_seq_flux2.dat' using 1:2 with points ls 2 title 'Flux 2', \
     f2_mean with lines ls 2 lw 3 title sprintf('Moyenne F2: %.1f ms', f2_mean)

# Version avec fenêtre glissante (moyenne mobile)
set output 'rtt_seq_moving_avg.png'
set title 'RTT avec moyenne mobile (fenêtre=10)'

# Fonction moyenne mobile
window_size = 10

plot 'rtt_seq_flux1.dat' using 1:2 with points ls 1 title 'Flux 1 (points)', \
     '' using 1:2 smooth mav(window_size) with lines ls 1 lw 3 title 'Flux 1 (moyenne mobile)', \
     'rtt_seq_flux2.dat' using 1:2 with points ls 2 title 'Flux 2 (points)', \
     '' using 1:2 smooth mav(window_size) with lines ls 2 lw 3 title 'Flux 2 (moyenne mobile)'

# Version séparée
set terminal pngcairo size 800,600
set output 'rtt_flux1_seq.png'
set title 'Flux 1: RTT par séquence'
unset key
plot 'rtt_seq_flux1.dat' using 1:2 with linespoints ls 1

set output 'rtt_flux2_seq.png'
set title 'Flux 2: RTT par séquence'
plot 'rtt_seq_flux2.dat' using 1:2 with linespoints ls 2