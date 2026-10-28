<table>
  <tr><td><strong>Rewritten NCCL backend becomes the default</strong>, with a flight recorder that dumps on hangs and <code>TORCH_DIST_USE_NCCL2=0</code> or <code>nccl-legacy</code> as rollback paths</td></tr>
  <tr><td><strong>One-sided transports for <code>torch.distributed</code></strong>, with a NIXL backend and CUDA-graph-capturable transfers</td></tr>
  <tr><td><strong>FSDP2 and pipelining gain finer memory and communication control</strong>, with fp32 for precision-sensitive parameters, CUDA-graph-captured gradient accumulation, and gradient reduction overlapped with compute</td></tr>
  <tr><td><strong>Faster 4-bit (NVFP4) LLM decoding on NVIDIA Blackwell GPUs</strong> through fewer, better-overlapped kernel launches in NVGEMM</td></tr>
  <tr><td><strong>Apple Silicon gains FP8 and faster decode</strong>, with <code>float8_e4m3fn</code> and <code>_scaled_mm</code>, a new <code>grouped_mm</code> with a decode fast path (1.32–1.34x tokens/s on MoE decode), and public <code>torch.mps.Stream</code> APIs</td></tr>
  <tr><td><strong>Broader platform support</strong> with FlyDSL kernels on AMD gfx950, Tensor Data Mover support for gfx1250 (MI450), ROCm 10.0 wheels, simpler SYCL kernel authoring and multi-GPU profiling on Intel GPUs, CUDA 13.2 as the default wheel with CUDA 13.4 alongside it, and <code>torch.compile</code> on Python 3.15</td></tr>
</table>
