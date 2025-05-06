#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

extern "C" {

void low_pass_filter(float* signal, int length, float alpha) {
    for (int i = 1; i < length; ++i) {
        signal[i] = alpha * signal[i] + (1 - alpha) * signal[i - 1];
    }
}

void high_pass_filter(float* signal, int length, float alpha) {
    float prev_input = signal[0];
    float prev_output = signal[0];
    for (int i = 1; i < length; ++i) {
        float current_input = signal[i];
        signal[i] = alpha * (prev_output + current_input - prev_input);
        prev_input = current_input;
        prev_output = signal[i];
    }
}

void moving_average_filter(float* signal, int length, int window_size) {
    float* temp = new float[length];
    for (int i = 0; i < length; ++i) {
        float sum = 0;
        int count = 0;
        for (int j = i - window_size / 2; j <= i + window_size / 2; ++j) {
            if (j >= 0 && j < length) {
                sum += signal[j];
                count++;
            }
        }
        temp[i] = sum / count;
    }
    for (int i = 0; i < length; ++i) signal[i] = temp[i];
    delete[] temp;
}

void compute_fft_magnitude(float* input, float* output, int n) {
    for (int k = 0; k < n; ++k) {
        float real = 0, imag = 0;
        for (int t = 0; t < n; ++t) {
            float angle = 2 * M_PI * t * k / n;
            real += input[t] * cos(angle);
            imag -= input[t] * sin(angle);
        }
        output[k] = sqrt(real * real + imag * imag);
    }
}

}
