import sys
import os

# Add the project root to the python path
sys.path.append('/home/ast/Desktop/my repo/cognitive_os')

from core.sentinel import VRAMSentinel

class MockSentinel(VRAMSentinel):
    def __init__(self, vram, ram, mac_mem, npu, apu):
        super().__init__()
        self.mock_vram = vram
        self.mock_ram = ram
        self.mock_mac = mac_mem
        self.mock_npu = npu
        self.mock_apu = apu

    def get_free_vram(self): return self.mock_vram
    def get_free_ram(self): return self.mock_ram
    def get_mac_unified_memory(self): return self.mock_mac
    def has_npu(self): return self.mock_npu
    def has_integrated_gpu(self): return self.mock_apu

def test_scenario(name, vram, ram, mac_mem, npu, apu):
    sentinel = MockSentinel(vram, ram, mac_mem, npu, apu)
    
    print(f"\\n{'='*60}")
    print(f" SCENARIO: {name}")
    print(f"{'='*60}")
    print(f" Hardware : RAM={ram}MB, VRAM={vram if vram != 'HARDWARE_NOT_NVIDIA' else '0'}MB, MAC={mac_mem}, NPU={npu}, APU={apu}")
    
    profile = sentinel.dynamic_allocation_profile()
    slow_evicted = sentinel.should_evict_slow_brain()
    fast_evicted = sentinel.should_evict_fast_brain()
    
    slow_loc = "System RAM (CPU)" if slow_evicted else "GPU VRAM"
    fast_loc = "System RAM (CPU)" if fast_evicted else "GPU VRAM"
    if mac_mem != "NOT_MAC" or apu:
        slow_loc = "Shared Unified Memory"
        fast_loc = "Shared Unified Memory"
        
    if npu:
        slow_loc = "System RAM (CPU)" if slow_evicted else "NPU"
        fast_loc = "System RAM (CPU)" if fast_evicted else "NPU"
        
    if vram == 'HARDWARE_NOT_NVIDIA' and mac_mem == 'NOT_MAC' and not apu and not npu:
        slow_loc = "System RAM (CPU)"
        fast_loc = "System RAM (CPU)"

    print(f" [Slow Brain (Thinker)] -> {slow_loc}")
    print(f" [Fast Brain (Swarm)]   -> {fast_loc}")
    print(f" [Swarm Parallel Size]  -> {profile['fast_brain_swarm_size']} Concurrent AI Threads")
    print(f" [Max Chunk Size]       -> {profile['chunk_size']} Tokens per AI Thread")

if __name__ == '__main__':
    # 1. User's Gaming Laptop (VRAM < RAM)
    test_scenario("Consumer Gaming Laptop (VRAM < RAM)", vram=8000, ram=32000, mac_mem="NOT_MAC", npu=False, apu=False)
    
    # 2. Inverted Architecture (VRAM > RAM)
    test_scenario("Inverted Architecture (VRAM > RAM)", vram=24000, ram=8000, mac_mem="NOT_MAC", npu=False, apu=False)
    
    # 3. Dead GPU (< 2000MB VRAM)
    test_scenario("Dead GPU / Critically Low VRAM", vram=1500, ram=16000, mac_mem="NOT_MAC", npu=False, apu=False)
    
    # 4. Apple Mac Studio
    test_scenario("Apple Mac Studio (Unified Memory)", vram="HARDWARE_NOT_NVIDIA", ram=8000, mac_mem=64000, npu=False, apu=False)
    
    # 5. Integrated APU
    test_scenario("Integrated APU (Shared Memory)", vram="HARDWARE_NOT_NVIDIA", ram=16000, mac_mem="NOT_MAC", npu=False, apu=True)
    
    # 6. Copilot+ PC (NPU Present)
    test_scenario("Modern Copilot+ PC (NPU Present)", vram="HARDWARE_NOT_NVIDIA", ram=16000, mac_mem="NOT_MAC", npu=True, apu=False)
    
    # 7. Pure CPU Fallback (No GPU, No NPU)
    test_scenario("Basic Dell Laptop (Pure CPU Fallback)", vram="HARDWARE_NOT_NVIDIA", ram=8000, mac_mem="NOT_MAC", npu=False, apu=False)
