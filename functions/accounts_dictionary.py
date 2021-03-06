def accounts_dict():
    return {
        'Direct Materials': {
            'Additives': {
                'Kjøp Tilsettingsmaterialer': 4022,
                'Kjøp Andre tilsettingsstoffer': 4031,
                'Kjøp Silica': 4030,
            },
            'Aggregates': {
                'Kjøp Pukk': 4021,
                'Kjøp Sand': 4020,
                'Kjøp Tilslag for overflatesjikt': 4025,
            },
            'Cement': {
                'Kjøp Sement rapid': 4011,
                'Kjøp Sement standard': 4010,
            },
            'Details': {
                'Kjøp Innstøpingsgods': 4230,
                'Kjøp Montasjedeler 1': 4250,
                'Kjøp Innstøpte løftedetaljer': 4220,
                'Montasjedeler til lager': 4545,
                'Kjøp Stål til formbygging': 4320,
            },
            'Insulation': {
                'Kjøp Isolasjon': 4210,
                'Brannisolering': 4636,
            },
            'Other (form oil, etc)': {
                'Kjøp HD-propper': 4217,
                'Kjøp Formolje': 4310,
                'Kjøp Andre hjelpematerialer': 4330,
            },
            'Prestessing Strand': {
                'Kjøp Spennarmering': 4150,
            },
            'Reinforcement': {
                'Kjøp Slakkarmering': 4160,
                'Kjøp Armeringsnett': 4170,
                'kjøp Kapp og bøy': 4161,
                'Vedl.hold prod.bygninger': 6580,
                'Kjøp Stål til formbygging': 4320,
            },
            'Wooden goods': {
                'Kjøp Finer/Trematerialer formbygg.': 4315,
                'Kjøp Trematerialer underlag': 4316,
            },
        },
        'Indirect Materials': {
            'Maintenance & Repair': {
                'Verneutstyr': 6025,
                'Vedl.hold HD-maskiner/utstyr': 6550,
                'Vedl.hold traverskraner': 6520,
                'Vedl.hold blandestasjoner': 6530,
                'Arbeidsklær': 6020,
                'Vedl.hold el-anlegg': 6582,
                'Kjøp Former til spesielle prosjek.': 4321,
                'Elektroder, sveisetråder': 6410,
                'Forbruksart./Småanskaffelser': 6425,
                'Annet større verktøy': 6451,
                'Håndverktøy': 6452,
                'Vedl.hold annet prod.utstyr': 6570,
                'Vedl.hold arbeidsmaskiner': 6595,
                'Leie av maskiner og utstyr produksjon, korttidsleie': 6350,
                'Løfteutstyr': 6460,
                'Vedl.hold VVS-anlegg': 6583,
                'Kappe- og slipeskiver': 6412,
                'Driftsrekvisita': 6420,
                'Vedl.hold conveyer/halvportal': 6540,
                'Vedl.hold former': 6566,
                'Leasing/Leie trucker': 6340,
                'Kjøp Diamantsagblad': 4325,
                'Vedl.hold spennutstyr': 6562,
                'Rens arbeidsklær': 6030,
                'Fabrikkinventar': 6480,
                'Spennhylser': 6411,
                'Vedl.hold løfteutstyr': 6560,
                'Montasjeverktøy': 6470,
                'Vedl.hold fabrikkinventar': 6510,
                'El. verktøy': 6450,
                'Service/Vedlh.avtale Trucker': 6594,
                'Vedl.hold transportbaner': 6531,
                'Vedl.hold montasjeutstyr': 6575,
                'Vedl.hold vibrasjonsutstyr': 6565,
                'Diverse utgifter': 7698,
            },
            'Human Resources & Finance': {
                'Travel': {
                    'Reise- og oppholdsutgifter': 7020,
                    'Reise-og opphold produksjon': 5086,
                    'Representasjon fradr.berettiget': 7715,
                },
                'Insurance, Warranties & Bank': {
                    'OTP timelønnede': 5081,
                    'AFP - dir. lønn': 5425,
                    'Personalforsikringer': 7520,
                    'Skadeforsikringer': 7510,
                    'AFP - ind.lønn': 5475,
                    'Bankomk og kortgebyr': 7770,
                    'Garantiprovisjoner': 8180,
                    'Etterskuddsrenter lever.': 8140,
                    'Rentekostnader leasing': 8135,
                    'Overf. lønn andre avd. dir': 5018,
                    'Avgiftsfrie godtgjørelser': 5091,
                    'LO/NHO-ordningen - ind. lønn': 5470,
                    'Diverse utgifter': 7690,
                    'Øvrige rentekostnader': 8150,
                },
                'Other (beverage, celebrations etc.)': {
                    'Øvrige velferdstiltak': 7190,
                    'Interne møtekostnader': 7030,
                    'Valgfrie arrangement': 7183,
                    'Treningsavgift': 7191,
                    'Jubileer/Gaver fradragsber.': 7180,
                    'Hytteleie': 7185,
                    'Kantineutstyr': 6016,
                    'Service/vedlh. drikkeautomater': 6018,
                    'Leasing/leie drikkeautomater': 6017,
                    'Bedriftsidrett': 7120,
                    'Yrkesskade pers/utstyr': 7115,
                },
                'Car Leasing': {
                    'Leasingleie firmabiler': 7013,
                    'Driftsutg. person-og varebiler (husk bær': 7010,
                    'Vedlikehold Firmabiler': 7011,
                    'Bompenger og parkering': 7025,
                    'Driftsutgifter varebiler': 4590,
                    'Vedlikehold Varebiler': 4591,
                    'Leasingleie Varebiler': 4593,
                    'Forsikring og avgifter Firmabiler': 7012,
                    'Forsikring og avgifter Varebiler': 4592,
                },
                'Healthcare': {
                    'Bedriftshelsetjenester': 7110,
                },
                'Recruitment & Development': {
                    'Rekrutteringskostnader': 7170,
                    'Kursavgifter': 7090,
                    'Gaver ikke fradragsber.': 7730,
                    'Utg. ved friv. opplæring': 7660,
                    'Diverse utgifter': 7690,
                    'Øresavrunding': 7691,
                },
                'Temp Staf Factories': {
                    'Innleide timer': 5085,
                    'Innleide timer ind.lønn': 5184,
                },
                'Reorganizing Costs': {
                    'Leasing och hyra omorganisering': 7698,
                    'Diverse utgifter omorganisering': 7699,
                },
                'Energy': {
                    'Elektrisk kraft - ordinær': 4370,
                    'Bioenergi': 4377,
                    'Fyringsolje': 4375,
                    'Naturgass': 4376,
                    'Elektrisk kraft - adm.bygg': 6110,
                    'Diesel til arb.maskiner': 6125,
                    'Elektrisk kraft - tilfeldig': 4371,
                },
                'Waste Management': {
                    'Avfallshåndtering': 6255,
                    'Slamsuging': 6257,
                    'Utgifter ved miljøtiltak': 6259,
                },
                'Security': {
                    'Vakthold': 6230,
                },
                'Cleaning': {
                    'Renhold': 6240,
                },
                'Building Maintenance': {
                    'Vedl.hold prod.bygninger': 6580,
                    'Andre eiendomsutgifter': 6265,
                    'Vedl.hold utendørs-anlegg': 6590,
                    'Vedl.hold adm.bygninger': 6610,
                },
                'Office Consumables': {
                    'Kontorrekvisita': 6720,
                    'Kontorutstyr': 6710,
                    'Porto': 6790,
                    'Kop.papir tegninger': 6721,
                },
                'Public Taxes': {
                    'OTP månedslønnede': 7540,
                    'Eiendomsavgifter': 6250,
                    'Festeavgifter': 6380,
                    'Diverse utgifter': 7690,
                    'Andre driftsinntekter avg.fri': 3861,
                },
                'Rent': {
                    'Leie av lokaler': 6210,
                    'Andre lokalkostnader': 6219,
                    'Leie bolig ansatte': 6040,
                },
                'Cafeteria, Food': {
                    'Kantinedrift': 6015,
                    'Mat v/overtid': 6010,
                },
            },
            'IT, Marketing, Consultants': {
                'IT & Communication': {
                    'Vedlikeholdsavtaler Edb': 6880,
                    'Mobiltelefonutg.': 6780,
                    'Vedl.hold printere (inkl serviceavtaler': 6780,
                    'LO/NHO-ordningen dir. lønn': 5420,
                    'Hardware-anskaffelser': 6885,
                    'Leasingkostnader Edb': 6875,
                    'Mobiltelefoner m.utstyr': 6715,
                    'Telefonutgifter': 6770,
                    'Konsulenttjenester Edb': 6890,
                    'Opplæring/Kurs Edb': 6895,
                    'Software-anskaffelser': 6886,
                    'Telefonutg. ansatte': 6775,
                    'Annet vedlikehold Edb': 6881,
                    'Kommun.utstyr (ikke mobil)': 6716,
                    'Linjekostnader Edb': 6870,
                },
                'Consultant Services': {
                    'Fees exceptional for general support services': 7775,
                    'Diverse honorar': 7220,
                    'Konsulenttjenester extern': 7229,
                    'Advokathonorar': 7215,
                    'Revisjonshonorar': 7210,
                    'Konsulenttj./Ark.hon./Prosj.le': 4650,
                    'Diverse utgifter': 7690,
                },
                'Marketing': {
                    'Reklameannonser': 7310,
                    'Aviser, Tidsskrift, abon.m.': 6760,
                    'Sponsorstøtte': 7314,
                    'Reklamemateriell': 7315,
                    'Reklameannonser på interne': 7312,
                    'Diverse markedsføring': 7350,
                    'Trykksaker': 6750,
                    'Byggeplasskilt': 7316,
                    'WEB vedlikehold www.spenncon.no': 7335,
                },
                'Logistics & Transportation': {
                    'Diverse fraktkostnader': 4475,
                    'Frakt båt': 4440,
                    'Utgifter ved mellomlagring': 4445,
                    'Frakt': 4860,
                    'Speditør/Varetaxi': 4450,
                    'Containerleie': 6355,
                },
            },
        },
        'Logistics': {
            'Element Transportation': {
                'Frakt leide biler': 4420,
                'Ventetid ved transport': 4465,
            },
            'Stock Yard (handling & loading)': {
                'Interntransport': 6256,
                'Kranbanetjenester': 4460,
            },
        },
        'Projects': {
            'Subcontractors': {
                'Montasje ved utenforstående': 4510,
                'Stålarbeider ved andre': 4620,
                'Elementkjøp': 4630,
                'Montasje ved utenforstående - timebasert': 4509,
                'Tilleggsarb. v/utenforstående': 4512,
                'Diverse fremmedytelser': 4640,
                'Montasjedeler 1': 4550,
                'Montasjeutg. - materialer': 4530,
                'Hjelpemateriell montasje': 4531,
                'Fuging': 4611,
                'Underentreprenører': 4610,
                'Reise-og opphold v/montasje': 4540,
                'Ståldeler': 4555,
                'Fugemateriell': 4525,
                'Leie øvrig montasjeutstyr': 4516,
            },
            'Services': {
                'Leie-konstuktører-eksterne': 4905,
                'Innleide timer CES': 5084,
            },
            'Rental Equipment': {
                'Leie av krantjenester': 4511,
                'Leie av lift': 4515,
                'Rigg (4502)': 4502,
                'Driftsutgifter mobilkraner': 4580,
            },
            'Assemby Materials': {
                'Betong ved montasje': 4520,
                'Kjøp Ferdigbetong': 4095,
            },
        },
    }
