#!/usr/bin/env python3
"""
Iodn - Kaijin Lab
ESP8266 Smart Weather Clock License Key Generator
Generates license keys from MAC addresses using CRC-8 algorithm
"""

import sys
import re

def calculate_license(mac_bytes):
    """
    Calculate license from MAC address using progressive CRC-8
    
    Algorithm:
    1. Start with template [0x19, 0x56, 0xAD, 0xC0, 0xB3, 0xF3]
    2. For each position i:
       - Replace template[i] with MAC[i]
       - Calculate CRC-8 over entire array
       - Store result as license[i]
    
    Args:
        mac_bytes: list of 6 bytes
    Returns:
        list of 6 license bytes
    """
    license = []
    
    # Initial template (salt) - discovered at address DAT_3ffe8723
    working_array = [0x19, 0x56, 0xAD, 0xC0, 0xB3, 0xF3]
    
    for i in range(6):
        # Progressive replacement: update position i with MAC byte
        working_array[i] = mac_bytes[i]
        
        # CRC-8 calculation with polynomial 0x07
        crc = 0xCD  # Initial CRC value
        
        # Process all 6 bytes of current state
        for j in range(6):
            crc ^= working_array[j]
            
            # Process 8 bits with polynomial 0x07
            for bit in range(8):
                if crc & 0x80:  # Check MSB
                    crc = ((crc << 1) ^ 0x07) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        
        license.append(crc)
    
    return license

def parse_mac_address(mac_str):
    """
    Parse MAC address from various formats
    
    Supported formats:
    - 40:91:51:64:39:CF
    - 40-91-51-64-39-CF
    - 409151643CF
    - 40 91 51 64 39 CF
    """
    # Remove all non-hex characters
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac_str)
    
    # Check if we have exactly 12 hex characters
    if len(mac_clean) != 12:
        raise ValueError(f"Invalid MAC address length: {len(mac_clean)} hex chars (need 12)")
    
    # Convert to bytes
    try:
        mac_bytes = [int(mac_clean[i:i+2], 16) for i in range(0, 12, 2)]
    except ValueError as e:
        raise ValueError(f"Invalid hex in MAC address: {e}")
    
    return mac_bytes

def format_mac(mac_bytes):
    """Format MAC bytes as XX:XX:XX:XX:XX:XX"""
    return ':'.join(f'{b:02X}' for b in mac_bytes)

def format_license(license_bytes):
    """Format license bytes as continuous hex string"""
    return ''.join(f'{b:02X}' for b in license_bytes)

def main():
    if len(sys.argv) < 2:
        print("ESP8266 License Key Generator")
        print("==============================")
        print("\nUsage: python3 keygen.py <MAC_ADDRESS>")
        print("\nSupported MAC formats:")
        print("  40:91:51:64:39:CF")
        print("  40-91-51-64-39-CF")
        print("  409151643CF")
        print("  40 91 51 64 39 CF")
        print("\nExample:")
        print("  python3 keygen.py 40:91:51:64:39:CF")
        print("\nAlgorithm Details:")
        print("  - Uses CRC-8 with polynomial 0x07")
        print("  - Initial template: 19:56:AD:C0:B3:F3")
        print("  - Progressive replacement with cascading effect")
        sys.exit(1)
    
    try:
        # Parse MAC address from command line
        mac_input = ' '.join(sys.argv[1:])  # Join all args in case of spaces
        mac_bytes = parse_mac_address(mac_input)
        
        # Generate license
        license_bytes = calculate_license(mac_bytes)
        
        # Display results
        print("\n" + "="*50)
        print("Small TV License Generator Results")
        print("="*50)
        print(f"Input:   {mac_input}")
        print(f"MAC:     {format_mac(mac_bytes)}")
        print(f"License: {format_license(license_bytes)}")
        print("="*50)
        
        # Also show the progression (for educational purposes)
        if '--verbose' in sys.argv or '-v' in sys.argv:
            print("\nProgression Details:")
            print("-"*50)
            working = [0x19, 0x56, 0xAD, 0xC0, 0xB3, 0xF3]
            for i in range(6):
                working[i] = mac_bytes[i]
                print(f"Step {i+1}: [{' '.join(f'{b:02X}' for b in working)}] → {license_bytes[i]:02X}")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
