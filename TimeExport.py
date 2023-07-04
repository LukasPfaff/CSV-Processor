import csv
import glob
import os

def process_csv(input_file):
    output_folder = 'out'
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, os.path.basename(input_file))
    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(input_file, 'r') as csv_file, open(output_file, 'w') as txt_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)  # Skip the header row if present

        header_section = '[Allgemein]\nZiel=LODAS\nBeraterNr=1706\nMandantenNr=xxxxx\nDatumsformat=TTMMJJJJ\n[Satzbeschreibung]\n1;u_lod_bwd_buchung_standard;abrechnung_zeitraum#bwd;bs_nr#bwd;pnr#bwd;la_eigene#bwd;bs_wert_butab#bwd;\n[Bewegungsdaten]'
        txt_file.write(header_section + '\n')

        for row in csv_reader:
            txt_file.write('1;' + row[7].replace('.','') + ';1;'+ row[6] + ';' + row[3] + ';' +row[14] + ';' + '\n')

# Example usage
input_folder = 'Zeiterfassung'

csv_files = glob.glob(os.path.join(input_folder, '*.csv'))

for csv_file in csv_files:
    process_csv(csv_file)