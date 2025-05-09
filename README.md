# Emscripten Low-pass Filter

This project demonstrates how to use [Emscripten](https://emscripten.org/) to compile a low-pass filter written in C++ to WebAssembly, and run it efficiently in the browser.

The demo includes a real-time signal filtering example, enhanced with a responsive UI and interactive charts.

---

## 🚀 What it does

- Implements a **low-pass filter in C++** to remove noise from a digital signal.
- Compiles the C++ code to **WebAssembly** using Emscripten.
- Loads the `.wasm` module in the browser via **JavaScript**.
- **Filters a sine wave** in real-time and displays both the original and filtered signals using a Chart.js line graph.
- Includes a **clean, modern UI** with smooth styling.

---

## 🛠 How to run

### 1. Install Emscripten SDK

    ```bash
    git clone https://github.com/emscripten-core/emsdk.git
    cd emsdk
    ./emsdk install latest
    ./emsdk activate latest
    source ./emsdk_env.sh


### 2. Compile:

emcc lowpass.cpp -s WASM=1 -o lowpass.js -s EXPORTED_FUNCTIONS='["_low_pass_filter","_high_pass_filter","_moving_average_filter","_compute_fft_magnitude","_malloc","_free"]' -s EXPORTED_RUNTIME_METHODS='["cwrap","ccall","HEAPF32"]'


### 3. Run server
     python3 -m http.server

### 4. Open Browser
    http://localhost:8000/index.html