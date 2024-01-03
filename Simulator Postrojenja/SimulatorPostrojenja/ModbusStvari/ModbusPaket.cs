using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace SimulatorPostrojenja.ModbusStvari
{
    public class ModbusPaket
    {
        private ushort transactionId;
        private ushort protocolId;
        private ushort length;
        private byte unitId;
        private byte functionCode;
        private byte[] data;

        public ModbusPaket(byte[] paketSaNeta)
        {
            transactionId = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(paketSaNeta, 0));
            protocolId = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(paketSaNeta, 2));
            length = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(paketSaNeta, 4));
            unitId = paketSaNeta[6];
            functionCode = paketSaNeta[7];
            data = new byte[paketSaNeta.Length - 8];
            Buffer.BlockCopy(paketSaNeta, 8, data, 0, paketSaNeta.Length - 8);
        }

        public ModbusPaket(ModbusPaket mbp)
        {
            transactionId = mbp.transactionId;
            protocolId = mbp.protocolId;
            length = mbp.length;
            unitId = mbp.unitId;
            functionCode = mbp.functionCode;
            data = mbp.data;
        }

        public byte[] BajtoviIzPaketa()
        {
            byte[] bajtovi = new byte[length + 6];
            Buffer.BlockCopy(BitConverter.GetBytes(transactionId), 0, bajtovi, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(protocolId), 0, bajtovi, 2, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(length), 0, bajtovi, 4, 2);
            bajtovi[6] = unitId;
            bajtovi[7] = functionCode;
            Buffer.BlockCopy(data, 0, bajtovi, 8, length - 1);
            return bajtovi;
        }

        public byte[] pakujException(TipGreske kodGreske)
        {
            byte[] odgovor = new byte[9];
            Length = 3;
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)TransactionId)), 0, odgovor, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)ProtocolId)), 0, odgovor, 2, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)Length)), 0, odgovor, 4, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(UnitId), 0, odgovor, 6, 1);
            Buffer.BlockCopy(BitConverter.GetBytes(FunctionCode + 0x80), 0, odgovor, 7, 1);
            Buffer.BlockCopy(BitConverter.GetBytes((byte)kodGreske), 0, odgovor, 8, 1);
            return odgovor;
        }

        public byte FunctionCode
        {
            get { return functionCode; }
        }
        public byte[] Data
        {
            get { return data; }
        }
        public ushort Length
        {
            get { return length; }
            set { length = value; }
        }
        public ushort TransactionId
        {
            get { return transactionId; }
        }
        public ushort ProtocolId
        {
            get { return protocolId; }
        }
        public ushort UnitId
        {
            get { return unitId; }
        }
    }
}
