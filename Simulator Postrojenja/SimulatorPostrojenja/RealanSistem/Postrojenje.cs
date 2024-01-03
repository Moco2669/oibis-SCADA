using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace SimulatorPostrojenja.RealanSistem
{
    public class Postrojenje
    {
        public static ConcurrentDictionary<ushort, Uredjaj> sviUredjaji;

        private Thread simulatorThread;
        private static int pomeraj = 0;

        static int Pomeraj
        {
            get { return pomeraj; }
            set { if (value >= -5 && value <= 6) pomeraj = value; }
        }
        
        public Postrojenje()
        {
            sviUredjaji = new ConcurrentDictionary<ushort, Uredjaj>();
            sviUredjaji.GetOrAdd(2000, new Uredjaj(TipUredjaja.ANALOG_INPUT, 250, 0, 700));
            sviUredjaji.GetOrAdd(1000, new Uredjaj(TipUredjaja.DIGITAL_OUTPUT, 1, 0, 1));

            simulatorThread = new Thread(simulate);
            simulatorThread.Start();
        }

        private void simulate()
        {
            while (true)
            {
                if (sviUredjaji[1000].Vrednost == 1)
                {
                    --Pomeraj;
                }
                else
                {
                    ++Pomeraj;
                }
                sviUredjaji[2000].PokusajZapisVrednosti((ushort)(sviUredjaji[2000].Vrednost + Pomeraj));
                //Console.Clear();
                foreach (KeyValuePair<ushort, Uredjaj> uredjaj in sviUredjaji)
                {
                    Console.WriteLine("Adresa: " + uredjaj.Key + ", Uredjaj: " + uredjaj.Value.TipUredjaja + ", Vrednost: " + uredjaj.Value.Vrednost);
                }
                Thread.Sleep(1000);
            }
        }
    }
}
