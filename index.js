const runFilter = async () => {
  const length = 50;
  const alpha = 0.1;
  const input = new Float32Array(length).map((_, i) => Math.sin(i * 0.3) + 0.2 * Math.random());

  await Module.ready;

  const buffer = Module._malloc(input.length * input.BYTES_PER_ELEMENT);
  Module.HEAPF32.set(input, buffer / input.BYTES_PER_ELEMENT);

  const filter = Module.cwrap("low_pass_filter", null, ["number", "number", "number"]);
  filter(buffer, length, alpha);

  const result = new Float32Array(Module.HEAPF32.buffer, buffer, length);
  Module._free(buffer);

  // Muestra el resultado en texto
  document.getElementById("output").textContent = "Filtered signal: [" + Array.from(result).map(n => n.toFixed(2)).join(", ") + "]";

  // Dibuja la gráfica
  const ctx = document.getElementById("chart").getContext("2d");
  if (window.chart && typeof window.chart.destroy === "function") {
    window.chart.destroy();
  }
  
  window.chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [...Array(length).keys()],
      datasets: [
        {
          label: 'Original',
          data: input,
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          fill: false
        },
        {
          label: 'Filtered',
          data: result,
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          fill: false
        }
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
};

