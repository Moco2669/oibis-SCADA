using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using SimulatorPostrojenja.ModbusStvari;
using SimulatorPostrojenja.Obradjivaci;
using SimulatorPostrojenja.RealanSistem;

namespace SimulatorPostrojenja
{
    class Program
    {
        static void Main(string[] args)
        {
            Postrojenje postrojenje = new Postrojenje();
            IzvrsilacFunkcije izvrsilacFunkcije = new IzvrsilacFunkcije();

            bool connected = false; //Promenljiva koja ce da prati da li smo konektovani
            Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPAddress adresa = IPAddress.Loopback;
            IPEndPoint adresaIPort = new IPEndPoint(adresa, 25252);
            socket.Bind(adresaIPort);
            while (!connected)
            {
                try
                { 
                    socket.Listen(1);
                    Console.WriteLine("Server slusa na adresi " + socket.LocalEndPoint);
                    Socket acceptSocket = socket.Accept();
                    Console.WriteLine("Prihvacena konekcija sa " + acceptSocket.RemoteEndPoint);
                    connected = true;
                    while (connected)
                    {
                        try
                        {
                            primiPaketIVratiOdgovor(acceptSocket, izvrsilacFunkcije);
                        }
                        catch (Exception e)
                        {
                            acceptSocket.Disconnect(false);
                            Console.WriteLine(e.Message);
                            connected = false;
                        }
                    }
                }
                catch (Exception e)
                {
                    socket.Disconnect(true);
                    Console.WriteLine(e.Message);
                    connected = false;
                }
            }
        }

        static void primiPaketIVratiOdgovor(Socket acceptSocket, IzvrsilacFunkcije izvrsilacFunkcije)
        {
            byte[] mbapHeader = new byte[7];
            if(acceptSocket.Receive(mbapHeader, 7, SocketFlags.None) == 0) //Kada se gracefully zatvori konekcija, u sledecem primanju broj primljenih bajtova je 0
            {
                Exception e = new Exception("Klijent se diskonektovao.");
                throw e;
            }
            int velicinaPaketa = 0;
            unchecked
            {
                velicinaPaketa = IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(mbapHeader, 4));
            }
            if (velicinaPaketa < 3)
            {
                /*Exception e = new Exception("Nevalidna velicina paketa");
                throw e;*/
                return;
            }
            byte[] podaci = new byte[velicinaPaketa - 1];
            acceptSocket.Receive(podaci, velicinaPaketa - 1, SocketFlags.None); //minus jedan jer smo izvukli ceo heder a length polje u sebi sadrzi 1 bajt iz hedera, koji smo jelte izvukli
            byte[] ceoPaket = new byte[7 + velicinaPaketa - 1];
            Buffer.BlockCopy(mbapHeader, 0, ceoPaket, 0, 7);
            Buffer.BlockCopy(podaci, 0, ceoPaket, 7, velicinaPaketa - 1);

            ModbusPaket primljeniPaket = new ModbusPaket(ceoPaket);
            byte[] response = izvrsilacFunkcije.napraviResponse(primljeniPaket);
            if (response != null)
            {
                acceptSocket.Send(response);
            }
        }
    }
}
