using SimulatorPostrojenja.ModbusStvari;
using SimulatorPostrojenja.RealanSistem;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace SimulatorPostrojenja.Obradjivaci
{
    public class IzvrsilacFunkcije
    {   
        public IzvrsilacFunkcije()
        {

        }

        public byte[] napraviResponse(ModbusPaket mbp)
        {
            if (mbp.FunctionCode >= 1 && mbp.FunctionCode <= 4)
            {
                ModbusReadRequest mbrq = new ModbusReadRequest(mbp);
                if (mbp.FunctionCode == 1 || mbp.FunctionCode == 2)
                {
                    return procitajDigital(mbrq);
                }
                else return procitajAnalog(mbrq);
            }
            else if (mbp.FunctionCode == 5 || mbp.FunctionCode == 6)
            {
                ModbusWriteRequest mbwq = new ModbusWriteRequest(mbp);
                if (mbp.FunctionCode == 5)
                {
                    return zapisiDigital(mbwq);
                }
                else return zapisiAnalog(mbwq);
            }
            else return mbp.pakujException(TipGreske.ILLEGAL_FUNCTION);
        }

        byte[] procitajDigital(ModbusReadRequest mbrq)
        {
            if(mbrq.QuantityToRead > 2000 || mbrq.QuantityToRead < 1)
            {
                return mbrq.pakujException(TipGreske.ILLEGAL_DATA_ACCESS);
            }
            List<ushort> vrednosti = new List<ushort>();
            for (int i = 0; i < mbrq.QuantityToRead; ++i)
            {
                if (!Postrojenje.sviUredjaji.ContainsKey((ushort)(mbrq.StartingAddress + i)))
                {
                    return mbrq.pakujException(TipGreske.ILLEGAL_DATA_ACCESS);
                }
                Uredjaj u = Postrojenje.sviUredjaji[(ushort)(mbrq.StartingAddress + i)];
                if (u.TipUredjaja != TipUredjaja.DIGITAL_INPUT && u.TipUredjaja != TipUredjaja.DIGITAL_OUTPUT)
                {
                    return mbrq.pakujException(TipGreske.ILLEGAL_FUNCTION);
                }
                vrednosti.Add(u.Vrednost);
            }
            return mbrq.pakujDigitalRead(vrednosti);
        }

        byte[] procitajAnalog(ModbusReadRequest mbrq)
        {
            if (mbrq.QuantityToRead > 125 || mbrq.QuantityToRead < 1)
            {
                return mbrq.pakujException(TipGreske.ILLEGAL_DATA_ACCESS);
            }
            List<ushort> vrednosti = new List<ushort>();
            for (int i = 0; i < mbrq.QuantityToRead; ++i)
            {
                if (!Postrojenje.sviUredjaji.ContainsKey((ushort)(mbrq.StartingAddress + i)))
                {
                    return mbrq.pakujException(TipGreske.ILLEGAL_DATA_ACCESS);
                }
                Uredjaj u = Postrojenje.sviUredjaji[(ushort)(mbrq.StartingAddress + i)];
                if(u.TipUredjaja != TipUredjaja.ANALOG_INPUT && u.TipUredjaja != TipUredjaja.ANALOG_OUTPUT)
                {
                    return mbrq.pakujException(TipGreske.ILLEGAL_FUNCTION);
                }
                vrednosti.Add(u.Vrednost);
            }
            //odgovor
            return mbrq.pakujAnalogRead(vrednosti);
        }

        byte[] zapisiDigital(ModbusWriteRequest mbwq)
        {
            if(mbwq.OutputValue != 0xFF00 && mbwq.OutputValue != 0x0000)
            {
                return mbwq.pakujException(TipGreske.ILLEGAL_DATA_VALUE);
            }
            if (!Postrojenje.sviUredjaji.ContainsKey(mbwq.OutputAddress))
            {
                return mbwq.pakujException(TipGreske.ILLEGAL_DATA_ACCESS);
            }
            if(Postrojenje.sviUredjaji[mbwq.OutputAddress].TipUredjaja != TipUredjaja.DIGITAL_OUTPUT)
            {
                return mbwq.pakujException(TipGreske.ILLEGAL_FUNCTION);
            }
            if (Postrojenje.sviUredjaji[mbwq.OutputAddress].PokusajZapisVrednosti(mbwq.OutputValue == 0 ? (ushort)0 : (ushort)1))
            {
                return mbwq.pakujDigitalWrite();
            }
            return mbwq.pakujException(TipGreske.ILLEGAL_DATA_VALUE);
        }

        byte[] zapisiAnalog(ModbusWriteRequest mbwq)
        {
            if (!Postrojenje.sviUredjaji.ContainsKey(mbwq.OutputAddress))
            {
                return mbwq.pakujException(TipGreske.ILLEGAL_DATA_ACCESS);
            }
            if (Postrojenje.sviUredjaji[mbwq.OutputAddress].TipUredjaja != TipUredjaja.ANALOG_OUTPUT)
            {
                return mbwq.pakujException(TipGreske.ILLEGAL_FUNCTION);
            }
            if (Postrojenje.sviUredjaji[mbwq.OutputAddress].PokusajZapisVrednosti(mbwq.OutputValue))
            {
                return mbwq.pakujAnalogWrite();
            }
            return mbwq.pakujException(TipGreske.ILLEGAL_DATA_VALUE);
        }
    }
}
