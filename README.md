# j8ger
An 8 bit homebuilt entertainment system

For this project i've taken inspiration from existing CPUs I read about. Mainly the 6502, 6809, BMOW1, and Gigatron. The final system should have capabilities similar to or exceeding the original NES and C64.

#### CPU:
* [Architecture Diagram](./docs/j8ger-arch.png)
* 3Mhz Clock Speed
* 8bit ALU with ADD, SUB, AND, OR, XOR
* 1MB RAM (Bank Switched)
* 1 (8-bit) Accumulator
* 2 (8-bit) Index Registers
* 1 (16-bit) Address Register
* 1 (16-bit) Program Counter
* 1 (16-bit) Stack Pointer
* Compatible with 6502 Assembly ( *Mostly )

#### GPU:
* 320x240 VGA Graphics with 8 bit color
* Tiled Background:
   * Tiles: 8px/8px
   * 40x30 tiles
   * Each tile can have up to 16 colors from a palette
   * Each tile can choose from 1 of 8 palettes
   * Smooth scrolling
* Sprites:
   * Sprites: 8px/8px
   * 256 Sprites per screen
   * Sprites can have up to 16 colors from a palette
   * Each sprite can choose from 1 of 8 palettes
   * All sprites can move on each frame
* Possible framebuffer mode for full resolution graphics