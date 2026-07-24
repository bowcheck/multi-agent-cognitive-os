import subprocess
import os

class VRAMSentinel:
    def __init__(self, token_limit=2500):
        self.token_limit = token_limit

    def get_free_vram(self):
        try: # Pings the physical GPU driver to check exactly how much VRAM is left
            smi = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.free', '--format=csv,noheader,nounits'])
            return int(smi.strip())
        except:
            return "HARDWARE_NOT_NVIDIA"

    def get_free_ram(self):
        try: # Pings the physical motherboard to check System RAM
            free_out = subprocess.check_output("free -m | awk '/^Mem:/{print $7}'", shell=True)
            return int(free_out.strip())
        except:
            return 8000 

    def get_cpu_load(self):
        try: # Reads 1-minute load average
            with open('/proc/loadavg', 'r') as f:
                return float(f.read().split()[0])
        except:
            return 0.0

    def get_mac_unified_memory(self):
        try:
            # Reads Apple Silicon unified memory
            out = subprocess.check_output(['sysctl', 'hw.memsize'], stderr=subprocess.DEVNULL)
            bytes_mem = int(out.decode().split(':')[1].strip())
            return bytes_mem // (1024 * 1024) # Return in MB
        except:
            return "NOT_MAC"

    def has_npu(self):
        try:
            # Detects Neural Processing Units (Intel Core Ultra, AMD Ryzen AI, Qualcomm Snapdragon)
            out = subprocess.check_output("lspci | grep -i 'neural\\|npu\\|ai' || ls /sys/class/accel/", shell=True, stderr=subprocess.STDOUT)
            return True if out.strip() else False
        except:
            return False

    def has_integrated_gpu(self):
        try:
            # Detects Integrated GPUs (APUs) where RAM and VRAM are physically shared (Intel Iris, AMD Radeon APU)
            out = subprocess.check_output("lspci | grep -i 'vga\\|3d\\|display' | grep -i 'integrated\\|intel\\|amd'", shell=True, stderr=subprocess.STDOUT)
            return True if out.strip() else False
        except:
            return False

    def dynamic_allocation_profile(self):
        """Dynamic Heterogeneous Computing Allocator for all Silicone Types"""
        vram = self.get_free_vram()
        ram = self.get_free_ram()
        mac_mem = self.get_mac_unified_memory()
        npu_present = self.has_npu()
        apu_present = self.has_integrated_gpu()
        
        # 1. Shared Unified Memory Architectures (Apple Silicon, NPUs, APUs)
        # In these systems, the CPU, GPU, and Neural Engines all physically share the exact same DDR5/LPDDR5 RAM pool.
        # This means they are highly constrained by memory bus bandwidth, not just capacity!
        if mac_mem != "NOT_MAC" or npu_present or apu_present:
            unified_mem = mac_mem if mac_mem != "NOT_MAC" else ram
            
            c_size = int(max(1200, unified_mem * 0.20)) # NO HARDCAP
            swarm = int(max(2, unified_mem // 4000)) # NO HARDCAP
            return {"chunk_size": c_size, "fast_brain_swarm_size": swarm}
            
        # 2. Traditional Heterogeneous PC (NVIDIA / AMD Discrete GPUs)
        elif vram != "HARDWARE_NOT_NVIDIA":
            if vram < 2000:
                # VRAM is dead. Fast Brain evicted to RAM.
                return {"chunk_size": 800, "fast_brain_swarm_size": 1}
            
            # Chunk size scales linearly with VRAM limit
            c_size = int(max(1000, vram * 0.5)) # NO HARDCAP
            
            if vram >= ram:
                # INVERTED ARCHITECTURE: VRAM is the powerhouse.
                swarm = int(max(2, vram // 1200)) # NO HARDCAP
            else:
                # NORMAL ARCHITECTURE: Limit swarm to prevent RAM overhead bottlenecks
                swarm = int(max(2, vram // 1500)) # NO HARDCAP
                
            return {"chunk_size": c_size, "fast_brain_swarm_size": swarm}
            
        # 3. Universal Fallback (Pure CPU / RAM - Highly Constrained)
        else:
            return {"chunk_size": 1200, "fast_brain_swarm_size": 1}

    def should_evict_slow_brain(self):
        """
        Determines if the Slow Brain should be evicted from GPU VRAM to System RAM.
        Only True if System RAM is significantly higher than VRAM.
        False for Unified Memory (Mac), APUs (Shared RAM), NPUs, and massive A100 GPUs.
        """
        vram = self.get_free_vram()
        ram = self.get_free_ram()
        mac_mem = self.get_mac_unified_memory()
        npu_present = self.has_npu()
        apu_present = self.has_integrated_gpu()
        
        if mac_mem != "NOT_MAC": return False
        if apu_present: return False
        
        if npu_present:
            # NPUs are incredible at small, rapid parallel inferencing (Fast Brains).
            # But they lack the heavy cache architecture needed for massive 16,000+ contexts.
            # We explicitly evict the Slow Brain to the CPU to keep the NPU dedicated 100% to the Swarm!
            return True
        
        if vram != "HARDWARE_NOT_NVIDIA":
            # User specifically requested: If VRAM is higher than RAM (reversed) or the same, DO NOT EVICT!
            if vram >= ram:
                return False
            elif vram > 24000:
                return False # Massive VRAM, no need to evict
            else:
                return True # RAM > VRAM (e.g. 32GB RAM, 8GB VRAM). Evict to save VRAM for the Swarm!
                
        return False

    def should_evict_fast_brain(self):
        """
        Determines if the Fast Brain MUST be evicted to System RAM.
        This ONLY happens on Pure CPU systems, or Discrete GPUs with critically low VRAM (<2000MB)
        where the Fast Brain physically cannot fit in the GPU.
        """
        vram = self.get_free_vram()
        mac_mem = self.get_mac_unified_memory()
        npu_present = self.has_npu()
        apu_present = self.has_integrated_gpu()
        
        if mac_mem != "NOT_MAC": return False
        if apu_present: return False
        if npu_present: return False
        
        if vram != "HARDWARE_NOT_NVIDIA":
            if vram < 2000:
                return True # VRAM is critically low. Force Fast Brain to CPU.
            else:
                return False
                
        # Pure CPU system without GPU
        return True

    def check_input_safety(self, text_length):
        ram = self.get_free_ram()
        vram = self.get_free_vram()
        cpu_load = self.get_cpu_load()
        
        if cpu_load > 15.0:
            return False, "PHYSICAL_CPU_OVERLOADED"
        if ram < 1000:
            return False, "PHYSICAL_RAM_LOW_SLOW_BRAIN_CHOKING"
        if vram != "HARDWARE_NOT_NVIDIA" and vram < 2000:
            return False, "PHYSICAL_VRAM_LOW_FAST_BRAIN_CHOKING"
        if text_length > self.token_limit:
            return False, "TOKEN_DENSITY_HIGH"
            
        return True, "SAFE"

class TCPStitcher:
    @staticmethod
    def stitch(results_list):
        # Programmatic mathematical sorting (NO LLM REQUIRED)
        results_list.sort(key=lambda x: x[0])
        return "\n".join([r[1] for r in results_list])
