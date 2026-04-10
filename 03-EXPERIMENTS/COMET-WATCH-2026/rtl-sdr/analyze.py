#!/usr/bin/env python3
"""
RTL-SDR Spectrogram Analyzer for Meteor Detection
Analyzes captured IQ data and creates spectrograms
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys
import os

def load_rtl_sdr_data(filename, sample_rate=250000):
    """Load raw RTL-SDR IQ data (uint8 format)."""
    # RTL-SDR outputs interleaved uint8 I/Q samples
    raw = np.fromfile(filename, dtype=np.uint8)
    
    # Convert to float32 and normalize (-1 to 1)
    iq = raw.astype(np.float32)
    iq = (iq - 127.5) / 127.5
    
    # Deinterleave into complex samples
    i = iq[0::2]
    q = iq[1::2]
    
    return i + 1j * q

def create_spectrogram(data, sample_rate=250000, nperseg=1024, noverlap=512):
    """Create spectrogram from IQ data."""
    # Compute spectrogram
    f, t, Sxx = signal.spectrogram(
        data, 
        fs=sample_rate,
        nperseg=nperseg,
        noverlap=noverlap,
        scaling='spectrum'
    )
    
    # Convert to dB
    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    
    return f, t, Sxx_db

def plot_spectrogram(f, t, Sxx_db, center_freq=143.05e6, output_file='spectrogram.png'):
    """Plot and save spectrogram."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Convert frequency to actual MHz (centered on tuned frequency)
    f_mhz = (f + center_freq) / 1e6
    t_sec = t
    
    # Plot
    im = ax.pcolormesh(t_sec, f_mhz, Sxx_db, shading='gouraud', cmap='viridis')
    ax.set_ylabel('Frequency (MHz)')
    ax.set_xlabel('Time (seconds)')
    ax.set_title(f'Spectrogram - Center: {center_freq/1e6:.3f} MHz')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Power (dB)')
    
    # Set limits to focus on interesting region
    ax.set_ylim(center_freq/1e6 - 0.1, center_freq/1e6 + 0.1)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"Spectrogram saved to: {output_file}")
    
    return fig

def detect_meteors(f, t, Sxx_db, threshold_db=-50, min_duration=0.1):
    """Simple meteor detection based on signal spikes."""
    # Find frequency bin closest to center (Graves signal)
    center_bin = len(f) // 2
    
    # Extract center frequency power over time
    center_power = Sxx_db[center_bin, :]
    
    # Detect spikes above threshold
    detections = []
    in_spike = False
    spike_start = 0
    
    for i, power in enumerate(center_power):
        if power > threshold_db and not in_spike:
            in_spike = True
            spike_start = t[i]
        elif power <= threshold_db and in_spike:
            in_spike = False
            spike_end = t[i]
            duration = spike_end - spike_start
            if duration >= min_duration:
                detections.append({
                    'time': spike_start,
                    'duration': duration,
                    'peak_power': np.max(center_power[max(0,i-10):i])
                })
    
    return detections

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze.py <capture_file.dat> [sample_rate]")
        print("Example: python3 analyze.py test.dat 250000")
        sys.exit(1)
    
    filename = sys.argv[1]
    sample_rate = int(sys.argv[2]) if len(sys.argv) > 2 else 250000
    
    print(f"Loading {filename}...")
    data = load_rtl_sdr_data(filename, sample_rate)
    print(f"Loaded {len(data)} samples ({len(data)/sample_rate:.1f} seconds)")
    
    print("Creating spectrogram...")
    f, t, Sxx_db = create_spectrogram(data, sample_rate)
    
    print("Plotting...")
    output_file = filename.replace('.dat', '_spectrogram.png')
    plot_spectrogram(f, t, Sxx_db, center_freq=143.05e6, output_file=output_file)
    
    print("Detecting meteors...")
    detections = detect_meteors(f, t, Sxx_db)
    print(f"Detected {len(detections)} potential meteors:")
    for i, det in enumerate(detections[:10]):  # Show first 10
        print(f"  {i+1}. Time: {det['time']:.2f}s, Duration: {det['duration']:.2f}s, Peak: {det['peak_power']:.1f} dB")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
