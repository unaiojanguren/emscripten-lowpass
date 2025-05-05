const runFilter = async () => {
  const length = 10;
  const alpha = 0.1;
  const input = new Float32Array(length).map((_, i) => Math.sin(i));
  const output = document.getElementById("output");

  await Module.ready;

  const buffer = Module._malloc(input.length * input.BYTES_PER_ELEMENT);
  Module.HEAPF32.set(input, buffer / input.BYTES_PER_ELEMENT);

  const filter = Module.cwrap("low_pass_filter", null, ["number", "number", "number"]);
  filter(buffer, length, alpha);

  const result = new Float32Array(Module.HEAPF32.buffer, buffer, length);
  output.textContent = "Filtered signal: [" + Array.from(result).join(", ") + "]";

  Module._free(buffer);
};
