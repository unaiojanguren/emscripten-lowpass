#include <cmath>

extern "C" {

void low_pass_filter(float* signal, int length, float alpha) {
    for (int i = 1; i < length; ++i) {
        signal[i] = alpha * signal[i] + (1 - alpha) * signal[i - 1];
    }
}

// FFT sencilla (solo magnitud, sin parte imaginaria compleja)
void compute_fft_magnitude(float* input, float* output, int n) {
    for (int k = 0; k < n; ++k) {
        float real = 0, imag = 0;
        for (int t = 0; t < n; ++t) {
            float angle = 2 * 3.14159265358979323846 * t * k / n;
            real += input[t] * cos(angle);
            imag -= input[t] * sin(angle);
        }
        output[k] = sqrt(real * real + imag * imag);
    }
}

}
