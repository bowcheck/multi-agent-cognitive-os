from core.sentinel import VRAMSentinel

sentinel = VRAMSentinel()

print("=========================================================")
print("  COGNITIVE OS: HETEROGENEOUS HARDWARE ALLOCATION TEST   ")
print("=========================================================\n")

# 1. Simulating the user's HP Omen
print("--- SCENARIO 1: Your HP OMEN 17 (8GB NVIDIA RTX 3070 Ti) ---")
sentinel.get_free_vram = lambda: 8000
sentinel.get_mac_unified_memory = lambda: "NOT_MAC"
sentinel.has_npu = lambda: False
sentinel.has_integrated_gpu = lambda: False
profile1 = sentinel.dynamic_allocation_profile()
print(f"OS Decision -> Chunk Size: {profile1['chunk_size']} chars | Parallel Fast Brains: {profile1['fast_brain_swarm_size']}\n")

# 2. Simulating a Mac Studio
print("--- SCENARIO 2: Apple Mac Studio (64GB Unified Memory) ---")
sentinel.get_free_vram = lambda: "HARDWARE_NOT_NVIDIA"
sentinel.get_mac_unified_memory = lambda: 64000
sentinel.has_npu = lambda: False
sentinel.has_integrated_gpu = lambda: False
profile2 = sentinel.dynamic_allocation_profile()
print(f"OS Decision -> Chunk Size: {profile2['chunk_size']} chars | Parallel Fast Brains: {profile2['fast_brain_swarm_size']}\n")

# 3. Simulating a Copilot+ NPU
print("--- SCENARIO 3: Brand new Intel Core Ultra Laptop (with NPU) ---")
sentinel.get_free_vram = lambda: "HARDWARE_NOT_NVIDIA"
sentinel.get_mac_unified_memory = lambda: "NOT_MAC"
sentinel.has_npu = lambda: True
sentinel.has_integrated_gpu = lambda: False
profile3 = sentinel.dynamic_allocation_profile()
print(f"OS Decision -> Chunk Size: {profile3['chunk_size']} chars | Parallel Fast Brains: {profile3['fast_brain_swarm_size']}\n")

# 4. Simulating an old laptop
print("--- SCENARIO 4: 10-year-old Dell Laptop (Pure CPU, No GPU) ---")
sentinel.get_free_vram = lambda: "HARDWARE_NOT_NVIDIA"
sentinel.get_mac_unified_memory = lambda: "NOT_MAC"
sentinel.has_npu = lambda: False
sentinel.has_integrated_gpu = lambda: False
profile4 = sentinel.dynamic_allocation_profile()
print(f"OS Decision -> Chunk Size: {profile4['chunk_size']} chars | Parallel Fast Brains: {profile4['fast_brain_swarm_size']}\n")
