using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace SimulatorPostrojenja.ModbusStvari
{
    public class ModbusWriteRequest : ModbusPaket
    {
        ushort outputAddress;
        ushort outputValue;

        public ModbusWriteRequest(ModbusPaket mbp) : base(mbp)
        {
            outputAddress = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(mbp.Data, 0));
            outputValue = (ushort)IPAddress.NetworkToHostOrder((short)BitConverter.ToUInt16(mbp.Data, 2));
        }

        public byte[] pakujDigitalWrite()
        {
            base.Length = 6;
            byte[] odgovor = new byte[12];
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.TransactionId)), 0, odgovor, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.ProtocolId)), 0, odgovor, 2, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.Length)), 0, odgovor, 4, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(base.UnitId), 0, odgovor, 6, 1);
            Buffer.BlockCopy(BitConverter.GetBytes(base.FunctionCode), 0, odgovor, 7, 1);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)outputAddress)), 0, odgovor, 8, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)outputValue)), 0, odgovor, 10, 2);
            return odgovor;
        }
        public byte[] pakujAnalogWrite()
        {
            byte[] odgovor = new byte[12];
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.TransactionId)), 0, odgovor, 0, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.ProtocolId)), 0, odgovor, 2, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)base.Length)), 0, odgovor, 4, 2);
            Buffer.BlockCopy(BitConverter.GetBytes(base.UnitId), 0, odgovor, 6, 1);
            Buffer.BlockCopy(BitConverter.GetBytes(base.FunctionCode), 0, odgovor, 7, 1);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)outputAddress)), 0, odgovor, 8, 2);
            Buffer.BlockCopy(BitConverter.GetBytes((ushort)IPAddress.HostToNetworkOrder((short)outputValue)), 0, odgovor, 10, 2);
            return odgovor;
        }

        public ushort OutputAddress
        {
            get { return outputAddress; }
        }
        public ushort OutputValue
        {
            get { return outputValue; }
        }
    }
}
