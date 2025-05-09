const runFilter = async () => {
  const length = 64;
  const alpha = parseFloat(document.getElementById("alpha").value);

  document.getElementById("alphaValue").textContent = alpha.toFixed(2);

  const input = new Float32Array(length).map((_, i) => Math.sin(i * 0.3) + 0.2 * Math.random());

  await Module.ready;

  const bytes = input.length * input.BYTES_PER_ELEMENT;
  const inputPtr = Module._malloc(bytes);
  const filteredPtr = Module._malloc(bytes);
  const fftOrigPtr = Module._malloc(bytes);
  const fftFiltPtr = Module._malloc(bytes);

  Module.HEAPF32.set(input, inputPtr / input.BYTES_PER_ELEMENT);
  Module.HEAPF32.set(input, filteredPtr / input.BYTES_PER_ELEMENT);

  const selectedFilter = document.getElementById("filterType").value;

  const lowpass = Module.cwrap("low_pass_filter", null, ["number", "number", "number"]);
  const highpass = Module.cwrap("high_pass_filter", null, ["number", "number", "number"]);
  const moving = Module.cwrap("moving_average_filter", null, ["number", "number", "number"]);
  const fft = Module.cwrap("compute_fft_magnitude", null, ["number", "number", "number"]);

  if (selectedFilter === "low") {
    lowpass(filteredPtr, length, alpha);
  } else if (selectedFilter === "high") {
    highpass(filteredPtr, length, alpha);
  } else if (selectedFilter === "moving") {
    moving(filteredPtr, length, alpha);  // usando alpha como window size temporal
  }

  fft(inputPtr, fftOrigPtr, length);
  fft(filteredPtr, fftFiltPtr, length);

  const filtered = new Float32Array(Module.HEAPF32.buffer, filteredPtr, length);
  const fftOrig = new Float32Array(Module.HEAPF32.buffer, fftOrigPtr, length);
  const fftFilt = new Float32Array(Module.HEAPF32.buffer, fftFiltPtr, length);

  Module._free(inputPtr);
  Module._free(filteredPtr);
  Module._free(fftOrigPtr);
  Module._free(fftFiltPtr);

  if (window.timeChart?.destroy) window.timeChart.destroy();
  if (window.fftChart?.destroy) window.fftChart.destroy();

  const ctx1 = document.getElementById("timeChart").getContext("2d");
  window.timeChart = new Chart(ctx1, {
    type: 'line',
    data: {
      labels: [...Array(length).keys()],
      datasets: [
        { label: "Original", data: input, borderColor: "rgba(255,99,132,1)", fill: false },
        { label: "Filtered", data: filtered, borderColor: "rgba(54,162,235,1)", fill: false }
      ]
    },
    options: {
      responsive: false,
      scales: {
        x: { title: { display: true, text: 'Sample Index' } },
        y: { title: { display: true, text: 'Value' } }
      }
    }
  });

  const ctx2 = document.getElementById("fftChart").getContext("2d");
  window.fftChart = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: [...Array(length).keys()],
      datasets: [
        { label: "Original Spectrum", data: fftOrig, backgroundColor: "rgba(255, 99, 132, 0.5)" },
        { label: "Filtered Spectrum", data: fftFilt, backgroundColor: "rgba(54, 162, 235, 0.5)" }
      ]
    },
    options: {
      responsive: false,
      scales: {
        x: { title: { display: true, text: 'Frequency Bin' } },
        y: { title: { display: true, text: 'Magnitude' } }
      }
    }
  });
};
