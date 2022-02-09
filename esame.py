import numpy

class ExamException(Exception): 
        pass

class CSVTimeSeriesFile:

    def __init__(self, name): #inizializzo il nome del file
        self.name = name 
    
    def verifica(self):
        try:
            file=open(self.name, 'r') #apro il file
            file.readline() #verifico che sia leggibile
            return 1
        except Exception as errore:
            return errore  #altrimenti ritorno il tipo di errore
            


    def data_valida(riga):
        #inizializzo una lista dove inserisco i valori da togliere, che sono quelli diversi dalla data
        #nota: se avessi tolto gli elementi nell'except, avrebbe iterato n volte in meno, per n uguale agli elementi non corretti e non avrebbe iterato l'intera riga 
        listaNera=[] 
        for item in riga:
            for i in listaNera:
                if(i in riga): #potevo anche risparmiarmi questo if
                    riga.remove(i)
            try: #verifico che la stringa si possa splittare e in tal caso verifico che sia del tipo anno-mese
                data=item.split("-")
                anno=int(data[0]) 
                mese=int(data[1])
                if(anno==float(data[0]) and mese == float(data[1])):
                    if(mese>0 and mese<13 and anno>0):
                        #nota: tengo tutta la data anche se è di tipo anno-mese-giorno oppure anno-mese-qualsiasi variabile, tanto ho ottenuto la data che volevo e l'errore non si propagherà e il risultato sarà sempre lo stesso
                        return list(riga) #tutti i controlli superati
                    else:
                        listaNera.append(item)
                else:
                    listaNera.append(item)
            except:
                listaNera.append(item) #inserisco l'elemento nella lista nera

        return 0 #nota: ritorna 0 <=> len(riga)==1
                 #l'ultimo elemento della lista non viene tolto, ma non mi interessa

    def passeggeri_validi(riga):
        #stessa logica della funzione data, solo che tolgo sia gli elementi precedenti sia quelli dopo, quindi voglio solo un formato di tipo anno-data, passeggeri
            listaNera=[]
            conta=0
            for item in riga:
                for i in listaNera:
                    if(i in riga):
                        riga.remove(i)
                if(conta!=0): #se l'elemento preso in considerazione non è la data
                    try:
                        passeggeri=int(item)
                        if(passeggeri == float(item) and passeggeri>0):
                            conta2=0 #stessa cosa di prima, solo che tengo anche il valore n-esimo
                            for scarto in riga:
                                if(conta2>1):
                                    riga.remove(scarto) #rimuovo tutti gli elementi successivi, indipendentemente dal loro tipo
                                conta2+=1
                            return riga
                        else:
                            listaNera.append(item)
                    except:
                        listaNera.append(item)
                conta+=1


            return 0


    def get_data(self):
        ok=CSVTimeSeriesFile.verifica(self)
        if(ok!=1): 
            raise ExamException("impossibile aprire il file: {}".format(ok))

        lista = [] #inizializzo una lista 
        file = open(self.name, 'r')

        for line in file:
            
            if("," in line): #se la riga si può splittare
                riga=line.split(',') #splitto le righe
                riga[-1] = riga[-1].strip() #pulisco la riga precedente (tolgo i \n e gli spazi vuoti)
                riga=CSVTimeSeriesFile.data_valida(riga)

                verifica=True
                if(riga==0 or len(riga)<2): #nota: sono equivalenti
                    verifica=False
                if(verifica):
                    ris=CSVTimeSeriesFile.passeggeri_validi(riga)
                    if(ris==0 or len(ris)!=2):
                        verifica=False

                if(verifica and len(lista)==0): #1 iterazione, non ho bisogno di verificare se è ordinato o meno
                    lista.append(ris)

                elif(verifica): #lista non vuota e verifico che sia ordinato
                    try:
                        data=ris[0].split("-") #splitto la data
                        anno=int(data[0])
                        mese=int(data[1])
                    except:
                        verifica=False
                    if(verifica):
                        for i in lista:                                                
                            m=numpy.array_split(i,2) #libreria che splitta un array in n pos, in questo caso 2
                            s=m[0] #metto s uguale alla data
                            trova=s[0].split("-") #nota: s è un array con un solo elemento

                            anno0=int(trova[0]) 
                            if(anno0>anno): #anno non ordinato
                                verifica=False

                            mese0=int(trova[1])
                            if(anno0==anno and mese0>=mese): #mese non ordinato
                                verifica=False
                                                            
                        if(verifica):
                            lista.append(ris)
                        else:
                            raise ExamException("elemento non ordinato")
            
        return lista
        




def calcolatore(lista_mesi, lista_valori):
    lista=[]
    for j in reversed(range(1,13)): #inceve di fare (-a+b)+(-b+c)...
                                    #faccio semplicemente (c-b)+(b-a)
        conta=0                     #tipo funzione ricorsviva da n
        somma=0
        val1=0
        val2=0
        verifica=True
        for i in reversed(range(0, len(lista_mesi))):
            try:
                if(lista_mesi[i]==j):
                    if(conta==0): #prima iterazione
                        somma=lista_valori[i]
                        conta+=1
                    else:
                        val1=lista_valori[i]#a
                        somma+=val2-val1 #b-a
                        val2=val1#nuovo valore di b 
                        conta+=1
            except: #se non è presente il mese j
                verifica=False


        if(conta>1): #se ci sono almento due iterazioni
            somma=somma/(conta-1)
            lista.append(somma)
        else:
            lista.append(0)


    copia=[]
    for i in range(0,12): #inizializzo un array di dim 12 con tutti valori nulli
        copia.append(0)

    for i in range(0,12):
        copia [11-i] = lista[i]  #inverto i valori dato che li ho invertiti prima

    return copia


def compute_avg_monthly_difference(time_series, first_year, last_year):
    try:#verifico che siano dei numeri
        anno1=int(first_year)
        anno2=int(last_year)
    except Exception as errore:
        raise ExamException("erroe nell'inserimento dell'anno: {}".format(errore))

    if(anno1==float(first_year) and anno2==float(last_year)):#verifico che siano dei numeri interi
        if(anno1>0 and anno2>0): #verifico che siano positivi
            if(anno1>anno2):
                anno1,anno2=anno2,anno1 #scambio variabili nel caso in cui l'intervallo è corretto ma gli estremi sono invertiti
            
            lista=time_series #per scrivere meno :)
            anni=[]
            mesi=[]
            valori=[]
            for i in lista:                 
                m=numpy.array_split(i,2) #splitto la lista
                s=m[0] #data
                k=m[1] #passeggeri
                trova=s[0].split("-")
                if(anno1 <= int(trova[0]) and int(trova[0])<=anno2): #da mettere apposto
                    anni.append(int(trova[0]))
                    mesi.append(int(trova[1]))
                    valori.append(int(k[0]))
            
            if(anno1 in anni and anno2 in anni): #se l'intervallo è compreso
                return(calcolatore(mesi,valori))
            else:
                raise ExamException("errore, intervallo non presente nel file")
            
        
        else:
            raise ExamException("erroe nell'inserimento dell'anno")
    else:
        raise ExamException("erroe nell'inserimento dell'anno")





time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series=time_series_file.get_data()
first_year=1950
last_year=1954
compute_avg_monthly_difference(time_series, first_year, last_year)