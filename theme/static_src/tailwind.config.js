/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        // Rutas para que Tailwind encuentre tus clases en los archivos de Django
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                "primary": "#E67E22",
                "primary-hover": "#D35400",
                "warm-cream": "#FDF5E6",
                "charcoal": "#1A1A1A",
                "dark-bg": "#121212",
                "dark-card": "#1E1E1E",
                "background-light": "#FFFFFF",
                "soft-gray": "#F4F2F0",
                "text-main": "#181411",
                "text-sub": "#887463"
            },
            fontFamily: {
                "display": ["Inter", "sans-serif"],
                "serif": ["Noto Serif", "serif"],
                "logo": ["Playfair Display", "serif"]
            },
            borderRadius: {
                "DEFAULT": "0.5rem",
                "lg": "1.25rem",
                "xl": "1.5rem",
                "full": "9999px"
            },
            boxShadow: {
                "soft": "0 10px 30px rgba(0,0,0,0.05)",
                "lift": "0 15px 35px rgba(0,0,0,0.1)",
                "button-lift": "0 10px 20px -5px rgba(230, 126, 34, 0.4)",
                "orange-glow": "0 0 15px rgba(230, 126, 34, 0.2)"
            },
            keyframes: {
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(40px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            },
            animation: {
                'fade-in-up': 'fadeInUp 1s ease-out forwards',
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}