# ESP8266 Smart Weather Clock License Keygen

## How It Works

The Smart Weather Clock (aka Small TV) validates devices using a license key derived from the device's MAC address. The algorithm uses a progressive CRC-8 calculation with a predefined template to generate a unique 12-character hexadecimal license key.

## Algorithm Details

| Component | Value | Purpose |
|-----------|-------|---------|
| **CRC Polynomial** | `0x07` (x⁸ + x² + x + 1) | Bit diffusion algorithm |
| **Initial CRC** | `0xCD` | Starting value for CRC calculation |
| **Template Array** | `[0x19, 0x56, 0xAD, 0xC0, 0xB3, 0xF3]` | Salt/initial state |

### Algorithm Steps

1. **Initialize** a 6-byte working array with template: `[0x19, 0x56, 0xAD, 0xC0, 0xB3, 0xF3]`

2. **For each position** `i` from 0 to 5:
   - Replace `working_array[i]` with `MAC[i]`
   - Calculate CRC-8 over the entire 6-byte working array
   - Store CRC result as `license[i]`

### Step-by-Step Example

For MAC `40:91:51:64:39:CF`:

| Step | Working Array | CRC Result | License Byte |
|------|--------------|------------|--------------|
| 1 | `[40, 56, AD, C0, B3, F3]` | `0xB4` | B4 |
| 2 | `[40, 91, AD, C0, B3, F3]` | `0xC2` | C2 |
| 3 | `[40, 91, 51, C0, B3, F3]` | `0x29` | 29 |
| 4 | `[40, 91, 51, 64, B3, F3]` | `0xCA` | CA |
| 5 | `[40, 91, 51, 64, 39, F3]` | `0xFE` | FE |
| 6 | `[40, 91, 51, 64, 39, CF]` | `0x4A` | 4A |

**Final License:** `B4C229CAFE4A`

### CRC-8 Calculation

For each byte in the working array:
1. XOR with current CRC value
2. For 8 bits:
   - Shift left by 1
   - If MSB was set, XOR with polynomial `0x07`

```python
def crc8(data):
    crc = 0xCD  # Initial value
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:  # Check MSB
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc
```
Each license byte depends on all previous MAC bytes plus remaining template bytes

## Usage

```bash
# Basic usage
python3 keygen.py 40:91:51:64:39:CF
```