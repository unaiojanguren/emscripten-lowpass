extern "C" {
void low_pass_filter(float* signal, int length, float alpha) {
    for (int i = 1; i < length; ++i) {
        signal[i] = alpha * signal[i] + (1 - alpha) * signal[i - 1];
    }
}
}
