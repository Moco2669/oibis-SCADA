using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimulatorPostrojenja.ModbusStvari
{
    public enum TipGreske : byte
    {
        ILLEGAL_FUNCTION = 0x01, ILLEGAL_DATA_ACCESS, ILLEGAL_DATA_VALUE
    }
}
