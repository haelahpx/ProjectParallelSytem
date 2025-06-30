export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    // tambahkan ini:
    future: {
        removeDeprecatedGapUtilities: true,
        purgeLayersByDefault: true,
    },
    // tambahkan ini juga untuk nonaktifkan lightningcss
    experimental: {
        optimizeUniversalDefaults: true,
    }
}
