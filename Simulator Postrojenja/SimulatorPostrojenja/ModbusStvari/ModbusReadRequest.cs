using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace SimulatorPostrojenja.ModbusStvari
{
    public class ModbusReadRequest : ModbusPaket
    {
        ushort startingAddress;
        ushort quantityToRead;

        public ModbusReadRequest(ModbusPaket mbp) : base(mbp)
        {
            startingAddress = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(base.Data, 0));
            quantityToRead = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(base.Data, 2));
        }

        public byte[] pakujAnalogRead(List<ushort> vrednosti)
        {
            base.Length = (ushort)(3 + vrednosti.Count * 2);
            byte[] odgovor = new byte[6 + base.Length];
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.TransactionId)), 0, odgovor, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.ProtocolId)), 0, odgovor, 2, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.Length)), 0, odgovor, 4, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(base.UnitId), 0, odgovor, 6, 1);
            Buffer.BlockCopy(BitConverter.GetBytes(base.FunctionCode), 0, odgovor, 7, 1);
            Buffer.BlockCopy(BitConverter.GetBytes((byte)(vrednosti.Count * 2)), 0, odgovor, 8, 1);
            for(int i=0; i<vrednosti.Count; ++i)
            {
                Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)vrednosti[i])), 0, odgovor, 9 + i, 2);
            }
            return odgovor;
        }
        public byte[] pakujDigitalRead(List<ushort> vrednosti)
        {
            byte velicinaNiza = (byte)((vrednosti.Count % 8) != 0 ? ((vrednosti.Count / 8) + 1) : (vrednosti.Count / 8));
            base.Length = (ushort)(3 + velicinaNiza);
            byte[] odgovor = new byte[6 + base.Length];
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.TransactionId)), 0, odgovor, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.ProtocolId)), 0, odgovor, 2, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.Length)), 0, odgovor, 4, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(base.UnitId), 0, odgovor, 6, 1);
            Buffer.BlockCopy(BitConverter.GetBytes(base.FunctionCode), 0, odgovor, 7, 1);
            Buffer.BlockCopy(BitConverter.GetBytes((byte)(velicinaNiza)), 0, odgovor, 8, 1);
            for(int j=0; j<velicinaNiza; ++j)
            {
                for(int i=0; i<8 && (j*8 + i)<vrednosti.Count; ++i)
                {
                    odgovor[9 + j] = (byte)((odgovor[9 + j] << 1) + vrednosti[i +(j*8)]);
                }
            }
            return odgovor;
        }

        public ushort StartingAddress
        {
            get { return startingAddress; }
        }
        public ushort QuantityToRead
        {
            get { return quantityToRead; }
        }
    }
}
