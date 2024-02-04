import numpy # Numpy
import csv # Lesen von CSV-Dateien
from types import SimpleNamespace # Einfacher Zugang fuer Objekte wie padc0.LC1  
from scipy.interpolate import InterpolatedUnivariateSpline # Fuer Zeitableitungen


# Klasse, um die CSV-Dateien zu laden
class CSVFile:
	# Hilfsfunktion, die Anhand des Spaltennamens die numerischen Daten der Spalte zurueckgibt
	def get_column_data(self,name):
		index=self.name_to_column[name] # Name zu Spaltenindex
		return self.numdata[:,index] # Gebe diese Spalte wieder
		
	# Konstruktor: Lade die CSV-Datei
	def __init__(self,filename):
		self.column_names=None # Namen der Spalten (erste nicht-leere Zeile)
		self.units=None # Einheiten der Spalten (zweite nicht-leere Zeile)
		self.numdata=[] # Numerische Daten
		with open(filename, newline='') as csvfile: # Lade die Datei
			csvdata = csv.reader(csvfile, delimiter=',', quotechar='|') # Lade es als CSV-Datei
			
			for row in csvdata: # Gehe über alle Zeilen
				if len(row)==0:
					continue # Ignoriere leere Zeilen
				if self.column_names is None:
					self.column_names=row # Erste nicht leere Zeile sind die Spaltennamen
				elif self.units is None:
					self.units=row # Zweite Zeile sind die Einheiten
				else:
					# Alles andere sind numerische Daten, die zu floats konvertiert werden
					self.numdata.append(list(map(float,row)))
					
		self.numdata=numpy.array(self.numdata) # Konvertiere die numerischen Daten zu numpy

		# Anhand der Spaltennamen erstellen wir nun ein dict, was in der Methode get_column_data benutzt wird
		self.name_to_column={name:index for index,name in enumerate(self.column_names)}
		
		# Spalte die numerischen Daten nach dem Spaltennamen auf
		self.t=self.get_column_data("t")
		self.padc0=SimpleNamespace()
		self.padc0.LC1=self.get_column_data("padc0.LC1")
		self.padc0.LC2=self.get_column_data("padc0.LC2")		
		self.padc1=SimpleNamespace()
		self.padc1.LC1=self.get_column_data("padc1.LC1")
		self.padc1.LC2=self.get_column_data("padc1.LC2")		
		self.cls1A=SimpleNamespace()
		self.cls1A.Pitch=self.get_column_data("cls1A.Pitch")-0.02618*180/numpy.pi # Korrigiere den Pitch anhand des gegebenen Offsets
		self.cls1A.Roll=self.get_column_data("cls1A.Roll")+0.00698*180/numpy.pi # Und den Roll anhand des gegebenen Offsets
		self.cls1A.PitchRate=self.get_column_data("cls1A.PitchRate")
		self.cls1A.RollRate=self.get_column_data("cls1A.RollRate")
		self.cls1A.AccX=self.get_column_data("cls1A.AccX")
		self.cls1A.AccZ=self.get_column_data("cls1A.AccZ")
		self.cls1B=SimpleNamespace()
		self.cls1B.Pitch=self.get_column_data("cls1B.Pitch")
		self.cls1B.Roll=self.get_column_data("cls1B.Roll")
		self.cls1B.PitchRate=self.get_column_data("cls1B.PitchRate")
		self.cls1B.RollRate=self.get_column_data("cls1B.RollRate")
		self.cls1B.AccX=self.get_column_data("cls1B.AccX")
		self.cls1B.AccZ=self.get_column_data("cls1B.AccZ")		
		self.Sum=self.get_column_data("Sum")
		
		# Berechne Hilfsgroessen fuer die Modellierung
		self.alpha=self.cls1B.Pitch # Winkel des Hebearms
		self.beta=self.cls1A.Roll-self.cls1B.Pitch # Winkel der Containeraufhaengung relativ zum Hebearm
		self.dot_alpha=self.cls1B.PitchRate # Zeitableitungen der Winkel
		self.dot_beta=self.cls1A.RollRate-self.cls1B.PitchRate 

		# Zweite Zeitableitungen -> Winkelbeschleunigungen -> Sollten laut Newton wichtig fuer die Gewichtssensoren sein		
		self.ddot_alpha=InterpolatedUnivariateSpline(self.t,self.dot_alpha,k=3).derivative()(self.t)
		self.ddot_beta=InterpolatedUnivariateSpline(self.t,self.dot_beta,k=3).derivative()(self.t)

	

# Lade eien CSV-Datei			
csv_file=CSVFile("../csv_data/leer_3 huebe.CSV")
#csv_file=CSVFile("../csv_data/1t_3_huebe.CSV")
#csv_file=CSVFile("../csv_data/1t_3_huebe_2.CSV")
#csv_file=CSVFile("../csv_data/2t_3_huebe.CSV")


# Plotten der Daten
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(csv_file.t,csv_file.padc0.LC1)
ax.legend()
ax.set(xlabel='time (s)')
ax.grid()
plt.show()

